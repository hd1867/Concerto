"""
A library for turning a list of frequencies or notes into a piece of sheet music.
Created for Brickhack 7

By: Hendrick Ducasse
"""

from PIL import Image, ImageDraw, ImageFont
import shutil
import noteAnalysis
import numpy as np
from scipy.io import wavfile

#Paths of bitmaps
TREBLE_CLEF = "Assets/treble.bmp"
QUARTER_NOTE = "Assets/QNote.bmp"
UPSIDEDOWN_QUARTER_NOTE = "Assets/HighQNote.bmp"
QUARTER_REST = "Assets/QRest.bmp"
COMMON_TIME = "Assets/CTime.bmp"

#The height of each note(In Pixels)
WHOLE_STEP = 11
HALF_STEP = WHOLE_STEP/2
OCTAVE = HALF_STEP * 11
#F4 is the first note that is entirely in the staff. It is used as a reference point for all other notes
REFERENCE_NOTE = 5
REFERENCE_OCTAVE = 4

#Template Parameters(In Pixels)
RESERVED_SPACE = 50 #Space reserved at the front of the ledger for Clef and Time Signature
LEDGER_WIDTH = 625 #Total width of each ledger Line
LEDGER_HEIGHT = 47 #The height of each ledger line
LEDGER_PADDING = 65 #The space between each ledger line
NUM_LEDGERS = 8 #The number of ledgers in the template
MARGIN_HEIGHT = 35 #The space between the margin and the top of the first ledger line
MARGIN_WIDTH = 30 #The space between the margin and the beginning of each ledger line
MEASURE_WIDTH = (LEDGER_WIDTH - RESERVED_SPACE)/4 #The Width of each measure
BEAT_SPACE = MEASURE_WIDTH/4 #Assuming you're in Common time, the width each beat takes up in a measure
NOTE_WIDTH = 15
NOTE_HEIGHT = 30
MAX_NOTES_PER_PAGE = 128
"""
@initializeStaff(staffName, TEMPLATE = "Assets/template.png"(DO NOT EDIT UNLESS ABSOLUTELY NECESSARY)

This function initializes the staff based off of the template image
:returns
drawImage - The pillow DrawImage object used to edit the staff image
"""
def initializeStaff(staffName, TEMPLATE = "Assets/template.png" ):
    shutil.copyfile(TEMPLATE, staffName + ".png")
    base = Image.open(staffName + ".png")
    staff = ImageDraw.Draw(base)
    return staff, base

"""
@drawMeasureLines(staff)

This function draws measure lines on a staff using the value returned by initializeStaff 
"""
def drawMeasureLines(staff):
    for i in range(8): #For each ledger line
        for j in range(1,4): #For each measure line
            ledgerLineX = MARGIN_WIDTH + RESERVED_SPACE + MEASURE_WIDTH*j
            ledgerLineTop = (ledgerLineX , MARGIN_HEIGHT + LEDGER_HEIGHT*(i+1) + LEDGER_PADDING*i)
            ledgerLineBottom = (ledgerLineX, MARGIN_HEIGHT + LEDGER_HEIGHT*i + LEDGER_PADDING*i)
            line = (ledgerLineTop, ledgerLineBottom)
            staff.line(line, fill="black")


def addTrebleClefs(staff):
    for i in range(8):
        trebleClefX = MARGIN_WIDTH
        trebleClefY = MARGIN_HEIGHT + LEDGER_HEIGHT*i + LEDGER_PADDING*i
        trebleClefPosition = (trebleClefX, trebleClefY)
        staff.bitmap(trebleClefPosition, Image.open(TREBLE_CLEF).convert("1"), fill="black")


def addNotes(staff, notes):
    for i in range(len(notes)):
        if notes[i] == None:
            noteY = MARGIN_HEIGHT + LEDGER_HEIGHT * (i // 16) + LEDGER_PADDING * (i//16) + NOTE_HEIGHT/2
            noteX = ((i - 1) % 16) * BEAT_SPACE + BEAT_SPACE / 2 + MARGIN_WIDTH + RESERVED_SPACE - NOTE_WIDTH / 2
            notePosition = (noteX, noteY)
            staff.bitmap(notePosition, Image.open(QUARTER_REST).convert("1"), fill="black")
            continue
        note, octave = notes[i]
        octave_offset = REFERENCE_OCTAVE - octave
        note_offset = REFERENCE_NOTE - note
        noteX = ((i-1) % 16) * BEAT_SPACE + BEAT_SPACE/2 + MARGIN_WIDTH + RESERVED_SPACE - NOTE_WIDTH/2
        noteY = MARGIN_HEIGHT + LEDGER_HEIGHT * (i//16) + LEDGER_PADDING * (i//16) + HALF_STEP * note_offset

        notePosition = (noteX, noteY)

        if octave >= 5:
            staff.bitmap(notePosition, Image.open(UPSIDEDOWN_QUARTER_NOTE).convert("1"), fill="black")
        else:
            staff.bitmap(notePosition, Image.open(QUARTER_NOTE).convert("1"), fill="black")


def saveSheet(base, name):
    base.save(name)


fs, data = wavfile.read('Assets/testMelody.wav')
notes = noteAnalysis.list_notes(data[:,0], fs, 120)


staff, base = initializeStaff("test1")
saveSheet(base, "test.png")
drawMeasureLines(staff)
addTrebleClefs(staff)
addNotes(staff, notes)
saveSheet(base, "test1.png")