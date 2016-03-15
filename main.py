__author__ = 'Wilfred'

import mido
import sys
import pygame
import mainwindow
from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import timedelta
from pygame import midi, time
from mido.midifiles import MidiTrack, MidiFile, Message

recording = False
MIDI_DIR = 'midi/'

class MidiCaptureThread(QtCore.QThread):
    def __init__(self, instrument, noteList):
        QtCore.QThread.__init__(self)
        self.inst = instrument
        self.noteList = noteList

    def run(self):
        while(recording):
            if self.inst.poll():
                midi_events = self.inst.read(10)
                for note in midi_events:
                    if note[0][2] > 0: # filter out notes with velocity 0
                        self.noteList.append(midi_events[0])
                        time.wait(10)


class QueryByLickMainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(QueryByLickMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.recordButton.clicked.connect(self.record)
        self.stopRecordButton.clicked.connect(self.stopRecord)
        self.inp = midi.Input(1)
        self.recorder = None
        self.noteList = []
        self.numberOfLicks = 0;
        self.recordingTimer = QtCore.QTimer(self)
        self.recordingTimer.setInterval(1000)
        self.recordingTimer.timeout.connect(self.displayTime)
        self.recordTime = timedelta()
        self.tempo = 0

        # populate midi input device list
        for i in range( pygame.midi.get_count() ):
            if pygame.midi.get_device_info(i)[2] == 1:
                self.midiInputSelector.addItem(str(pygame.midi.get_device_info(i)[1]))
        self.midiInputSelector.currentIndexChanged.connect(self.selectMidiDevice)

    def selectMidiDevice(self):
        midiDevice = self.midiInputSelector.currentIndex()
        self.inp = midi.Input(midiDevice)

    def displayTime(self):
        self.recordTimeLabel.setText(str(self.recordTime))
        self.recordTime += timedelta(seconds=1)

    def record(self):
        global recording
        self.recordingTimer.start()
        self.recordTimeLabel.setText(str(self.recordTime))
        recording = True
        self.recorder = MidiCaptureThread(self.inp, self.noteList)
        self.recorder.start()

    def stopRecord(self):
        global recording
        self.recordingTimer.stop()
        self.recordTime = timedelta()
        recording = False
        self.recordTimeLabel.setText(str(self.recordTime))
        print(self.noteList)
        #MyMidi = MidiFile3(1)
        with MidiFile() as mid:
            track = MidiTrack()
            mid.tracks.append(track)
            for noteEvent in self.noteList:

                if noteEvent[0][0] == 144:
                    track.append(Message('note_on', note=noteEvent[0][1], velocity=noteEvent[0][2], time=int(noteEvent[1]/100)))

                elif noteEvent[0][0] == 128:
                    track.append(Message('note_off', note=noteEvent[0][1], velocity=noteEvent[0][2], time=int(noteEvent[1]/100)))
            lickFileName = 'lick' + str(self.numberOfLicks)
            mid.save(MIDI_DIR + lickFileName + '.mid')
            self.midiFileList.addItem(lickFileName)
            self.numberOfLicks += 1

def main():
    midi.init()
    pygame.init()

    app = QtWidgets.QApplication(sys.argv)
    form = QueryByLickMainWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()