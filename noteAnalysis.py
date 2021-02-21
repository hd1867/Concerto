import numpy as np
from scipy.io import wavfile

C = 0
Db = 1
D = 2
Eb = 3
E = 4
F = 5
Gb = 6
G = 7
Ab = 8
A = 9
Bb = 10
B = 11

NOTES = [16.35, 17.32, 18.35, 19.45, 20.60, 23.12,
         23.12, 24.50, 25.96, 27.50, 29.14, 30.87]

OCTAVE_RANGES = [NOTES[B],
                 NOTES[B]*2,
                 NOTES[B]*(2**2),
                 NOTES[B]*(2**3),
                 NOTES[B]*(2**4),
                 NOTES[B]*(2**5),
                 NOTES[B]*(2**6),
                 NOTES[B]*(2**7),
                 NOTES[B]*(2**8)]


def find_octave(freq):
    
    if freq < NOTES[B]:
        return 0
    
    for i in range(8):
        if freq > OCTAVE_RANGES[i] and freq < OCTAVE_RANGES[i + 1]:
            return i + 1
        

def find_note(freq):
    
    octave = find_octave(freq)
    
    for i in range(12):
        if freq > NOTES[i]*(2**octave) - 2**octave and freq < NOTES[i]*(2**octave) + 2**octave:
            return i, octave


def spectral_properties(y: np.ndarray, fs: int) -> dict:
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    spec = np.abs(spec)
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    sd = np.sqrt(np.sum(amp * ((freq - mean) ** 2)))
    amp_cumsum = np.cumsum(amp)
    median = freq[len(amp_cumsum[amp_cumsum <= 0.5]) + 1]
    mode = freq[amp.argmax()]
    Q25 = freq[len(amp_cumsum[amp_cumsum <= 0.25]) + 1]
    Q75 = freq[len(amp_cumsum[amp_cumsum <= 0.75]) + 1]
    IQR = Q75 - Q25
    z = amp - amp.mean()
    w = amp.std()
    skew = ((z ** 3).sum() / (len(spec) - 1)) / w ** 3
    kurt = ((z ** 4).sum() / (len(spec) - 1)) / w ** 4

    result_d = {
        'mean': mean,
        'sd': sd,
        'median': median,
        'mode': mode,
        'Q25': Q25,
        'Q75': Q75,
        'IQR': IQR,
        'skew': skew,
        'kurt': kurt
    }

    return result_d


def list_frequencies(wave, Fs, granularity=1.0):
    frequencies = []

    for i in range(int((len(wave)/Fs)/granularity) - 1):
        cursor = wave[int(Fs*granularity*i):int(Fs*granularity*(i + 1))]
        if spectral_properties(cursor, Fs)['mode'] == 0:
            frequencies.append(spectral_properties(cursor, Fs)['median'])

        else:
            frequencies.append(spectral_properties(cursor, Fs)['mode'])
    
    frequencies.append(spectral_properties(wave[(int((len(wave)/Fs)/granularity) - 1):], Fs)['mode'])    
            
    return frequencies


def list_notes(data, fs, bpm=60):
    
    bps = bpm/60
    frequencies = list_frequencies(data, fs, granularity=1/bps)

    notes = []
    for freq in frequencies:
        notes.append(find_note(freq))
        
    return notes
    

fs, data = wavfile.read('1k.wav')

print(list_notes(data, fs, bpm=80))
