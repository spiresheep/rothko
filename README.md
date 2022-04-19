# rothko - Last updated April 19, 2022
A layout system for verifying and generating beautiful layouts.

## To run dev build
1. Install Python 3.
2. Install PySimpleGUI using the command `pip3 install pysimplegui`
3. CD into the directory
	@@ -14,19 +14,30 @@ A layout system for verifying and generating beautiful layouts.
## To build app for Windows
1. `pyinstaller --onefile --windowed --icon icon.ico --name RothkoViewer rothko.py`

## Config File Notes

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

It expects NO OVERLAP.

## TODO - Boring Super Secret Dev Notes
1. Live/Hot update
2. Cell Editor (?)