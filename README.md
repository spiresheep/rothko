# rothko - Last updated April 27, 2022

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

Names that cannot be used for cells:
  EAST, WEST, NORTH, SOUTH, MAX_WIDTH, MIN_WIDTH, Canvas

Each cell must have a unique name.

~~They are to be used as variables for constraints.
leftover - eg. Leftover/2 - meaning give HALF the ratio to the cell
viewport - Can be thought of a supercell or superlayout that contains the layout.
Canvas.width is the width of the viewport. Eg. width = canvas.width / 2~~

## Limitations
The layout breaks when the width is less than or equal the sum of the outline.
and border. and the borders are different colors.

It also breaks when the text is much wider than the cell it's in.

Solid colored sqaures blend into each other.

## TODO - Boring Super Secret Dev Notes
1. Add names to cells without names so the app does not crash
1. Cell/Layout Editor
2. Improve the layout config file format. Improvements will take the form of
removing JSON chaff, adding shorthands for all the properties and more.
