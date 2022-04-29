# rothko - Last updated April 28, 2022

A layout system for verifying and generating beautiful layouts.

## To run app locally
1. Install Python 3.
2. Install PySimpleGUI using the command `pip3 install pysimplegui`
3. Install SymPy using the command `pip3 install sympy`
4. `cd` into the directory
5. To run the app type `python3 rothko.py`

## To build app for MacOS
1. `pyinstaller --onefile --windowed --osx-bundle-identifier com.github.spiresheep --icon icon.icns --name RothkoViewer rothko.py`
2. Then make the resulting files executable

## To build app for Windows
1. `pyinstaller --onefile --windowed --icon icon.ico --name RothkoViewer rothko.py`

## Config File Notes/Rules

Each cell must have a unique name.

**These names cannot be used for cells:**
  **EAST, WEST, NORTH, SOUTH, MAX_WIDTH, MIN_WIDTH, canvas**

If you need to use the canvas in a constraint you can do the following:
width -> canvas_width
height -> canvas_height

Constraints can be expressed in the following way:
### Literal
eg. C.width = 100
### Property
eg. C.width = A.width
### Expression
eg. C.width = A.width + 100
eg. C.width = A.width - B.width

## Limitations
The layout breaks when the width of a mixed policy component is less than 4.

It also breaks when the text is much wider than the cell it's in.

Solid colored squares blend into each other.

## TODO - Boring Super Secret Dev Notes
1. Add names to cells without names so the app does not crash
1. Change how traversal works and make it easier to traverse across cells
1. Cell/Layout Editor
2. Improve the layout config file format. Improvements will take the form of
removing JSON chaff, adding shorthands for all the properties and more.
