# code for parsing a pattern indicated by an input MIDI file and searching the Weimar Jazz Database for solos containing that pattern
# should be imported by main.py
# first call getPattern with user-inputted tempo and input file name as parameter
# returns (or will return) list of all solos containing the lick indicated by the input MIDI file, sorted by similarity to the input lick

import subprocess

MIDI_DIR = 'midi/'
# takes an int representing a percentage and returns the inter-onset interval class corresponding to that percentage
def getIOI(onset):
    if onset < 35:
        return -2
    elif onset in range(35, 71):
        return -1
    elif onset in range(71, 141):
        return 0
    elif onset in range(141, 281):
        return 1
    elif onset > 280:
        return 2

# takes an int indicating the nth search, writes the config, and runs the search
def runSearch(ioi, pitch, notes):
    cfg = "qbl_cfg.yml"
    result = "qbl_out.csv"
    with open(cfg, 'w') as f:
        # specify current directory as read/write path, as well as which layer of search this is 
        # can be extended if user wishes to use a different directory
        f.write("dir: .\noutdir: .\noutfile: " + result + "\n\n")
        
        # length of input MIDI file is max N-gram length
        f.write("maxN: " + str(len(notes)) + "\n\n")
        
        # write trivial/static information - search all pieces by all musicians in the database
        f.write("tunes:\n\n - query:\n    conditions:\n      solo_info:\n")
        f.write("        performer: '%'\n        title: '%'\n")
        f.write("    display:\n      transcription_info: filename_sv\n    type: sv\n\n")
        
        # specify database location, since we want to search the wjazzd 
        # can be extended if user wishes to use a different location for the wjazzd
        f.write("database:\n  type: sqlite3\n  path: wjazzd.db\n  password: None\n  use: True\n\n")
        
        # make requests: begin with IOI class search, and filter based on those semitone interval patterns which match the input lick
        f.write("requests:\n -\n    transform: ioiclass-rel\n    pattern: " + str(ioi) + "\n")
        f.write("    secondary:\n      transform: interval\n      pattern: " + str(pitch) + "\n")
        f.write("      operation: match\n    display: list")
    
    subprocess.call(["melpat", "-c", cfg])

# takes as input user-specified tempo and midi input file, converts .mid to .csv, gets all the notes' information, and executes a search with that information  
def getPattern(tempo, midiin):
    # invokes melconv to convert the midi input file to output
    midiinpath = MIDI_DIR + midiin + '.mid'
    csvout = midiin + ".csv"
    subprocess.call(["melconv", "-f", "mcsv1", "-i", midiinpath])

    # starting with an empty list, append all the notes represented in the .csv file
    # the first two lines are metadata and can be ignored, every other note is represented as a list
    notes = []
    with open(csvout, 'r') as f:
        for x in f.read().splitlines():
            notes.append(x.split(';'))
        notes = notes[2:]

    # calculate intervals between successive notes, measured in semitones
    pitch = []
    for i in range(1, len(notes)):
        pitch.append(int(notes[i][5])-int(notes[i-1][5]))    

    # calculate milliseconds between onsets, and convert that millisecond value to percentage of the tempo
    # pass that value to the getIOI method to obtain IOI classes
    ioi = []
    for i in range(1, len(notes)):
        ioi.append(getIOI(int(100 * ((float(notes[i][0]) - float(notes[i-1][0])) / tempo))))
    
    # placeholder: just run search once, to exactly match the entered pattern    
    runSearch(ioi, pitch, notes)

# to do: 
#   alter pitch and/or ioi lists to allow some variation in the input licks, probably using regular expressions (nontrivial)
#   write function that looks at the output results file after an executed search and examines the patterns in the solos, sorting them by similarity to the input lick (trivial)
