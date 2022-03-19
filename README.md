# rothko
A layout system for verifying and generating beautiful layouts.

## To run app - Outdated
1. Install Python 3.
2. Install PySimpleGUI using the command `pip3 install pysimplegui`
3. CD into the directory
4. To run the code type `python3 rothko.py`

## To build app for MacOS

`pyinstaller --onefile --windowed --icon boar.icns --name RothkoViewer rothko.py`

 ## Actual command???!?!?
pyinstaller --onefile --windowed --osx-bundle-identifier com.github.spiresheep --icon boar.icns --name RothkoViewer rothko.py

## To build app for Windows
?????????

## Limitations
The layout breaks when the width is less than or equal the sum of the outline.
and border. and the borders are different colors.

It also breaks when the text is much wider than the cell it's in.

There is no way to change the name of the file the document accepts.

Solid colored sqaures blend into each other.

It expects NO OVERLAP.

## TODO - Boring Super Secret Dev Notes
1. File uploader rather than just using demo_file.txt
2. Live/Hot update
3. Cell Editor (?)