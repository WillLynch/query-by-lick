__author__ = 'Wilfred'

import mido
import sys
import pygame
import mainwindow
import mido
from PyQt5 import QtGui, QtWidgets, QtCore
from datetime import timedelta
from pygame import midi, time
from mido.midifiles import MidiTrack, MidiFile, Message, MetaMessage

recording = False
MIDI_DIR = 'midi/'

class MidiCaptureThread(QtCore.QThread):
    def __init__(self, midiInput, noteList):
        QtCore.QThread.__init__(self)
        self.inst = midi.Input(midiInput)
        self.noteList = noteList

    def run(self):
        while(recording):
            if self.inst.poll():
                midi_events = self.inst.read(10)
                for note in midi_events:
                    if note[0][2] > 0: # filter out notes with velocity 0
                        self.noteList.append(midi_events[0])
                        time.wait(10)
        self.inst.close()


class QueryByLickMainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(QueryByLickMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.recordButton.clicked.connect(self.record)
        self.stopRecordButton.clicked.connect(self.stopRecord)
        self.midiDevice = 1
        self.recorder = None
        self.noteList = []
        self.numberOfLicks = 0;
        self.recordingTimer = QtCore.QTimer(self)
        self.recordingTimer.setInterval(1000)
        self.recordingTimer.timeout.connect(self.displayTime)
        self.recordTime = timedelta()
        self.recordTimeLabel.setText(str(self.recordTime))
        self.tempo = 0

        # populate midi input device list
        for i in range( pygame.midi.get_count() ):
            if pygame.midi.get_device_info(i)[2] == 1:
                self.midiInputSelector.addItem(str(pygame.midi.get_device_info(i)[1]))
        self.midiInputSelector.currentIndexChanged.connect(self.selectMidiDevice)

    def selectMidiDevice(self):
        self.midiDevice = self.midiInputSelector.currentIndex()

    def displayTime(self):
        self.recordTimeLabel.setText(str(self.recordTime))
        self.recordTime += timedelta(seconds=1)

    def record(self):
        global recording
        try:
            self.tempo = int(self.tempoEdit.text())
            self.recordingTimer.start()
            self.recordTimeLabel.setText(str(self.recordTime))
            recording = True
            self.recorder = MidiCaptureThread(self.midiDevice, self.noteList)
            self.recorder.start()
        except Exception:
            QtWidgets.QMessageBox.about(self, 'Error','Input can only be a number')
            pass

    def stopRecord(self):
        global recording
        self.recordingTimer.stop()
        self.recordTime = timedelta()
        recording = False
        self.recorder.quit()
        self.recordTimeLabel.setText(str(self.recordTime))
        self.writeNoteListToMidiFile()

    def writeNoteListToMidiFile(self):
        with MidiFile() as mid:
            track = MidiTrack()
            mid.tracks.append(track)
            track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.tempo)))
            if self.noteList[0][0][0] == 144:
                track.append(Message('note_on', note=self.noteList[0][0][1], velocity=self.noteList[0][0][2], time=0))
            for i in range(1, len(self.noteList)):
                noteEvent = self.noteList[i]
                lastEvent = self.noteList[i-1]
                if noteEvent[0][0] == 144:
                    track.append(Message('note_on', note=noteEvent[0][1], velocity=noteEvent[0][2], \
                                         time=(int(milliSecondsToTicks(noteEvent[1], mido.bpm2tempo(self.tempo), mid.ticks_per_beat))) - \
                                              int(milliSecondsToTicks(lastEvent[1], mido.bpm2tempo(self.tempo), mid.ticks_per_beat))))

                elif noteEvent[0][0] == 128:
                    track.append(Message('note_off', note=noteEvent[0][1], velocity=noteEvent[0][2], \
                                         time=(int(milliSecondsToTicks(noteEvent[1], mido.bpm2tempo(self.tempo), mid.ticks_per_beat))) - \
                                              int(milliSecondsToTicks(lastEvent[1], mido.bpm2tempo(self.tempo), mid.ticks_per_beat))))
            lickFileName = 'lick' + str(self.numberOfLicks)
            mid.save(MIDI_DIR + lickFileName + '.mid')
            self.midiFileList.addItem(lickFileName)
            self.numberOfLicks += 1
        self.noteList = []

def main():
    midi.init()
    pygame.init()

    app = QtWidgets.QApplication(sys.argv)
    form = QueryByLickMainWindow()
    form.show()
    app.exec_()

def milliSecondsToTicks(ms, tempo, ticks_per_beat):
    milliseconds_per_beat = tempo/1000
    milliseconds_per_tick = milliseconds_per_beat / float(ticks_per_beat)
    time_in_ticks = ms / milliseconds_per_tick
    return time_in_ticks

if __name__ == '__main__':
    main()