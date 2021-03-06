#!/usr/bin/python
from os import system
import argparse
import sys

TO_ESCAPE = ["!",'"',"#","$","&","'","(",")","*",";","<",">","?",r"\\","[","\\","`","{","|","~",r"\t",r"\n"]

class Colors:
    PURPLE = [91,92,129,135,141]
    PINK = [126,163,200,201,207]
    BLUE = [17,18,19,20,21]
    GREEN = [22,28,34,40,46]
    RED = [52,88,124,160,196,1]
    YELLOW = [142,190,226,227,228]
    ORANGE = [130,166,202,208,214]
    GRAY = [235,240,245,250,255]
    CYAN = [32,38,45,51,87,123]

parser = argparse.ArgumentParser(description="Convert a basic ASCII art to a bash script with colors included.")
parser.add_argument('--ascii', '-a', default=None, type=str, help="The ASCII art you want to convert. So that you can assure it works, surround the ASCII art with double quotes like this: \"YOUR ASCII ART\"")
parser.add_argument('--padding', '-p', default=0, type=int, help="The amount of pixels you wanna move your ASCII art by to the left.")
parser.add_argument('--color', '-c', default="RED", type=str, help="The color gradient you wanna use (PURPLE, PINK, BLUE, GREEN, RED, YELLOW, ORANGE, GRAY, CYAN)")
args = parser.parse_args()
padding = args.padding * " "

def convert(txt):
    result = ""
    for char in txt:
        if char in TO_ESCAPE:
            result += f"\"\{char}\""
        else:
            result += char
    return result

if args.ascii == None:
    asciiart = sys.stdin.read()
    if asciiart in [None, ""]:
        parser.error("ascii needs to have a value, either passed in or piped.")
    else:
        asciiart = convert(asciiart)
else:
    asciiart = args.ascii
color_iter = getattr(Colors, args.color.upper())

def convert():
    color_index = 0
    up = True
    complete_code = 'echo -e "'
    for line in asciiart.splitlines():
        complete_code += f'{padding}\e[38;5;{color_iter[color_index]}m' + str(line) + r'\n'
        if up is True:
            if color_index == len(color_iter)-1:
                up = False
                color_index -= 2
            color_index += 1
        elif up is False:
            if color_index == 0:
                up = True
                color_index += 2
            color_index -= 1
    complete_code += '"'
    return complete_code

converted = convert()
print(f"\33[7m{converted}\33[0m", "\n\n\n")
system(converted)
