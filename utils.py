import mingus.core.scales as scales
import rtmidi

# Note to midi conversion
notesWithSharp = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
notesWithTrueFlat = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
notesWithFlat = ["C","C#","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
notesWithFlat.reverse()

print(notesWithTrueFlat)
def midiConversion(NoteArray):
  root = 1
  rootMidi = 60
  midiNotes = []
  for note in NoteArray:
    if '#' in note:
      midiAmp = note.count('#')
      if midiAmp >= 2:
        rootMidi = (midiAmp * 12) + rootMidi

    if 'b' in note:
      midiAmp = note.count('b')
      if midiAmp >= 2:
        rootMidi = (midiAmp * 12) + rootMidi

    if note in notesWithSharp:
      midiNote = ((notesWithSharp.index(note) + 1) - root) + rootMidi
      midiNotes.append(midiNote)
      rootMidi = 60
    elif note in notesWithTrueFlat:
      midiNote = ((notesWithTrueFlat.index(note) + 1) - root) + rootMidi
      midiNotes.append(midiNote)
      rootMidi = 60
    else:
      print("The note was not recognized. Please enter a valid note.", note)
    print(midiNote)
    print("-------------------")
    print(note)
  return midiNotes

def scaleFinder(rootNote, numOfScale):
  scale = 0
  if numOfScale == 1:
    scale = scales.Chromatic(rootNote, 2).ascending()
  elif numOfScale == 2:
    scale = scales.Major(rootNote, 2).ascending()
  elif numOfScale == 3:
    scale = scales.NaturalMinor(rootNote, 2).ascending()
  elif numOfScale == 4:
    scale = 0
  elif numOfScale == 5:
    scale = 0

  return scale

def rootNoteFinder(numOfRoot):
  return notesWithFlat[numOfRoot - 1]

def chordHandler(numOfRoot, numOfScale, numOfNotes):
  rootNote = rootNoteFinder(numOfRoot)
  scale = scaleFinder(rootNote, numOfScale)

  if scale == 0:
    if rootNote:
      return [rootNote]
    else:
      return
  noteArray = []
  noteArray.append(scale[0])
  j = 0

  for i in range(numOfNotes - 1):
    j += 2
    noteArray.append(scale[j])

  return noteArray

def handOrientationFinder(hands):
  rightHand = [] 
  leftHand = []
  if hands[0]["type"] == 'Right':
    rightHand = hands[0]
  elif hands[1]["type"] == 'Right':
    rightHand = hands[1]

  if hands[0]["type"] == 'Left':
    leftHand = hands[0]
  elif hands[1]["type"] == 'Left':
    leftHand = hands[1]

  return leftHand, rightHand

def playNote(note, midiout):
  note_on = [0x90, note, 112]
  midiout.send_message(note_on)
  return

def stopNote(note, midiout):
  note_off = [0x90, note, 0]
  midiout.send_message(note_off)
  return