# rothko - Last updated April 19, 2022

A layout system for verifying and generating beautiful layouts.

## To run dev build
1. Install Python 3.
2. Install PySimpleGUI using the command `pip3 install pysimplegui`
3. Install SymPy using the command `pip3 install pysimplegui`
4. `cd` into the directory
5. To run the code type `python3 rothko.py`

## To build app for MacOS
1. `pyinstaller --onefile --windowed --osx-bundle-identifier com.github.spiresheep --icon icon.icns --name RothkoViewer rothko.py`
2. Then make the resulting files executable

## To build app for Windows
1. `pyinstaller --onefile --windowed --icon icon.ico --name RothkoViewer rothko.py`

## Config File Notes/Rules

Reserved names: EAST, WEST, NORTH, SOUTH

Each cell should have a unique name.

The following words should not be used as cell names: viewport,leftover. They
have special meaning within the layout and using them may cause undesired behavior.

They are inteded to be used as variables for constraints.
leftover - eg. Leftover/2 - meaning give HALF the ratio to the cell
viewport - Can be thought of a supercell or superlayout that contains the layout.
Canvas.width is the width of the viewport. Eg. width = canvas.width / 2

## Limitations
The layout breaks when the width is less than or equal the sum of the outline.
and border. and the borders are different colors.

It also breaks when the text is much wider than the cell it's in.

Solid colored sqaures blend into each other.


## TODO - Boring Super Secret Dev Notes
1. Cell Editor
