My submission is programmed in python 3.8.10 on the drexel tux linux servers. 

All of my code is contained within a single python script called CG_hw1.py. It can be called by using the python3 command:

    python3 CG_hw1.py -f hw1.ps -a 25 -b 50 -c 399 -d 399 -m 10 -n 100 -s 2 > test.ps

There is also a makefile that has two commands default and all:

    default - creates the executable for future runs.

    all - runs all the commands that were given in the hw.

My file contains two static functions main and hw1.

    main() - Uses argparse to parse the arguments and set defaults if need be.

    hw1(args) - Takes those arguments and does all the work to read, transform and write the lines to a new postscript file.

FileIO(path):
This is a class on lines 5 - 40 I made that is responsible for the reading and writing of the postscript files. It has two 
methods read and write.

    read() -    Uses the path available that was passed through the constructor of the FileIO class. From that file, it loops
                over every line and appends to a list all the commands after %%%BEGIN and before %%%END.

    write() -   Creates the dimensions for the file from the given arguments, then writes that to stout in the requested format.
                After that, it loops over all the lines given to it to stout as well.

Transformer(lines, args):
This class is contained through lines 42 - 86 and is responsible for calculating and returning the transformed points. It has 4 methods,
three of which are responsible for scaling (_scale), rotating (_rotate) and translating (_translate) and the last is used to set points (_set_points).

    _scale() -  Multiplies the current value of the coordinate to the scaling factor.

    _rotate() - First converts the given rotation in degree form and converts it to radians so I can utalize the math library's cosine and sine functions.
                After that, I use the formula responsible for calculating a counter-clockwise rotation and assign the coordinate values to that.

    _translate() - Adds the translation to the current coordinate values.

    _set_points(line) - Takes in a line and sets the coordinate attributes to their respective values.

    transform_lines() - Loops through all the given lines, sets the points and transforms the coordinates in the order of scale, rotate then translate.
                        Once all the values are transformed, I append those new lines to a list and loop until it's over. After, I return the new 
                        transformed lines.

Clip(lines, args):
I created a class within the lines 88 - 162 that holds the algorithm (cohen_sutherland_clipping) and two helper a functions (_find_code, _set_points) 
responsible for clipping the transformed lines to the world window. 

    _find_code(x, y) -  Takes a coordinate pair and defines a binary
                        value based on which points are out of the world window. Those codes
                        are later used to see which lines should, or shouldn't be
                        clipped, entirely kept, or removed. 

    _set_points(line) - Takes in a line and sets the coordinate attributes to their respective values.

    cohen_sutherland_clipping() -   If a line is needed for clipping, I recalculate an (x, y) coordinate pair based on 
                                    the current (x1, y1) (x2, y2) and re-assign it depending on which pair was out of the 
                                    world windows bounds. I do this for all lines within the file.