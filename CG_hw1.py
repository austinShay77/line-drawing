#!/usr/bin/env python3

import argparse
import math
import sys

class FileIO:
    def __init__(self, path):
        self.path = path

    # take a list of lines, write them to stdout in .ps form
    def write(self, lines, args):
        x_size = args.upper_boundx - args.lower_boundx + 1
        y_size = args.upper_boundy - args.lower_boundy + 1

        sys.stdout.write(f"%%BeginSetup\n   << /PageSize [{x_size} {y_size}] >> setpagedevice\n%%EndSetup\n\n%%%BEGIN")
        for line in lines:
            if "Line" in line:
                sys.stdout.write(f"\n{line[0]-args.lower_boundx} {line[1]-args.lower_boundy} moveto\n{line[2]-args.lower_boundx} {line[3]-args.lower_boundy} lineto\nstroke")
        sys.stdout.write(f"\n%%%END\n")

    # take a .ps file, parse it into a 2d array
    def read(self):
        with open(self.path) as file:
            commands = self._find_meaningful_lines([line.rstrip() for line in file if line != "\n"])
        return self._split_lines(commands)
    
    # splites the line so each coordinate is its own element
    def _split_lines(self, commands):
        organized = [element.split() for element in commands]
        return organized

    # only keeps lines after %%%BEGIN and before %%%END
    def _find_meaningful_lines(self, commands):
        meaningless = True
        meaningful_lines = []
        for element in commands:
            if meaningless:
                if f"%%%BEGIN" in element:
                    meaningless = False
            else:
                if f"%%%END" in element:
                    break
                meaningful_lines.append(element)
        return meaningful_lines

class Transformer:
    def __init__(self, lines, args):
        self.lines = lines
        self.args = args
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    # create a new list of transformed lines
    def transform_lines(self):
        new_lines = []
        for line in self.lines:
            self._set_points(line)
            self._scale()
            self._rotate()
            self._translate()
            new_lines.append([self.x1, self.y1, self.x2, self.y2, "Line"])
        return new_lines

    def _scale(self):
        self.x1 = self.x1 * self.args.scaling_factor
        self.y1 =  self.y1 * self.args.scaling_factor

        self.x2 = self.x2 * self.args.scaling_factor
        self.y2 =  self.y2 * self.args.scaling_factor

    def _rotate(self):
        phi = self.args.ccr * math.pi / 180
        x1 = self.x1 * math.cos(phi) - self.y1 * math.sin(phi)
        y1 = self.x1 * math.sin(phi) + self.y1 * math.cos(phi)
        x2 = self.x2 * math.cos(phi) - self.y2 * math.sin(phi)
        y2 = self.x2 * math.sin(phi) + self.y2 * math.cos(phi)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def _translate(self):
        self.x1 += self.args.x_dim
        self.y1 += self.args.y_dim

        self.x2 += self.args.x_dim
        self.y2 += self.args.y_dim
            
    # uses the current line to re-assign attributes
    def _set_points(self, line):
        self.x1, self.y1 = float(line[0]), float(line[1])
        self.x2, self.y2 = float(line[2]), float(line[3])

class Clip:
    def __init__(self, lines, args):
        self.lines = lines
        self.args = args
        self.inside = 0 # 0000
        self.left = 1   # 0001
        self.right = 2  # 0010
        self.bottom = 4 # 0100
        self.top = 8    # 1000
        self.x_min = self.args.lower_boundx
        self.y_min = self.args.lower_boundy
        self.x_max = self.args.upper_boundx
        self.y_max = self.args.upper_boundy
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    # sees which lines needs to be clipped and re-calculates coordinates
    def cohen_sutherland_clipping(self):
        clipped_lines = []
        for line in self.lines:
            self._set_points(line)
            x = 0
            y = 0

            p1_code = self._find_code(self.x1, self.y1)
            p2_code = self._find_code(self.x2, self.y2)

            # both in
            if p1_code == 0 and p2_code == 0:
                clipped_lines.append([self.x1, self.y1, self.x2, self.y2, "Line"])
            # both out
            elif (p1_code & p2_code) != 0:
                continue
            else:
                if p1_code == 0:
                    out_code = p2_code
                else:
                    out_code = p1_code

                if out_code == self.left:
                    x = self.x_min
                    y = (self.x_min - self.x1)/(self.x2 - self.x1) * (self.y2 - self.y1) + self.y1
                elif out_code == self.right:
                    x = self.x_max
                    y = (self.x_max - self.x1)/(self.x2 - self.x1) * (self.y2 - self.y1) + self.y1
                elif out_code == self.bottom:
                    y = self.y_min
                    x = (self.y_min - self.y1)/(self.y2 - self.y1) * (self.x2 - self.x1) + self.x1
                elif out_code == self.top:
                    y = self.y_max
                    x = (self.y_max - self.y1)/(self.y2 - self.y1) * (self.x2 - self.x1) + self.x1

                if out_code == p1_code:
                    self.x1 = x
                    self.y1 = y 
                else:
                    self.x2 = x
                    self.y2 = y 
                clipped_lines.append([self.x1, self.y1, self.x2, self.y2, "Line"])
        return clipped_lines

    # calculates the binary value of clipped lines
    def _find_code(self, x, y):
        code = self.inside
        if x < self.x_min:
            code |= self.left
        elif x > self.x_max:
            code |= self.right
        if y < self.y_min:
            code |= self.bottom
        elif y > self.y_max:
            code |= self.top
        return code

    # uses the current line to re-assign attributes
    def _set_points(self, line):
        self.x1, self.y1 = float(line[0]), float(line[1])
        self.x2, self.y2 = float(line[2]), float(line[3])

def hw1(args):
    fileio = FileIO(args.ps_file)
    lines = fileio.read()

    transformer = Transformer(lines, args)
    new_lines = transformer.transform_lines()

    clipping = Clip(new_lines, args)
    clipped_lines = clipping.cohen_sutherland_clipping()

    fileio.write(clipped_lines, args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--ps_file", type=str, default="hw1.ps")
    parser.add_argument("-s", "--scaling_factor", type=float, default=1.0)
    parser.add_argument("-r", "--ccr", type=int, default=0)
    parser.add_argument("-m", "--x_dim", type=int, default=0)
    parser.add_argument("-n", "--y_dim", type=int, default=0)

    parser.add_argument("-a", "--lower_boundx", type=int, default=0)
    parser.add_argument("-b", "--lower_boundy", type=int, default=0)
    parser.add_argument("-c", "--upper_boundx", type=int, default=499)
    parser.add_argument("-d", "--upper_boundy", type=int, default=499)

    args = parser.parse_args()

    hw1(args)

if __name__ == "__main__":
    main()