Query By Lick
=============

Description
-----------

Query by Lick is an interactive search engine designed for the Weimar jazz database. It allows the user to search by
entering a musical phrase directly from a MIDI keyboard.

Dependencies
------------

* PyQt 5
* Python 3.2 or higher
* Pygame 1.9.1
* MeloPySuite
* Weimar jazz database

### PIP Dependencies
* mido


Development
-----------

I have been using QT Designer to generate the mainwindows.py file. If you make changes to this file manually, they will
be lost! If you make changes to the QueryByLick.ui file in QT Designer, run

C:\Python34\Lib\site-packages\PyQt5\pyuic5.bat -x QueryByLick.ui -o mainwindow.py

within the project directory to update the generated python code.

### TODO

* output csv files somewhere other than root directory
* display results of query in GUI


