# code for parsing a pattern indicated by an input MIDI file and searching the Weimar Jazz Database for solos containing that pattern
# should connect with main.py to receive the tempo and input file information

import subprocess

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

# tempo variable, specified by user in GUI - CHANGE THIS
# should be expressed as float representing seconds per beat. Divide 60.0 by tempo if it is expressed in BPM
tempo = 0.500

# midiin and csvout specified by results of user input - CHANGE THIS
# invokes melconv to convert the midi input file to output
midiin = "midi/filename.mid"
csvout = "filename.csv"
subprocess.call(["melconv", "-f", "mcsv1", "-i", midiin])

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

# takes an int indicating the nth search, writes the config, and runs the search
def runSearch(n):
    cfg = "qbl_cfg.yml"
    result = "qbl_search_" + str(n)
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

# placeholder: just run search once, to exactly match the entered pattern    
runSearch(1)

# to do: figure out exactly how multiple searches should be executed (nontrivial)
# Loop through all output files and return an ordered list containing information including artist name, song, tempo, pitch, onset of lick (trivial)