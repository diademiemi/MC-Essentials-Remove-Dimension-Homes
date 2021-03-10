#!/usr/bin/env python3

# Home remover script made by DiaDemiEmi
# PLEASE READ README.md BEFORE USING

import os
import re
from dotenv import load_dotenv

load_dotenv()
userdata_location = os.getenv('USERDATA_LOCATION')
dimension = os.getenv('DIMENSION')

# Define function to scan string for homes in certain dimension.
# It reads the string line by line, searches for "home:", stores the line number of the first match.
# It then searches for "world: " followed by the name of the dimension, if found, and is after 
# The line with "home: ", return the line number
def scanln(text):
    homesln = 0
    count = 0
    for line in text.splitlines():
        if re.search("homes:", line):
            homesln = count
        if re.search("world: {0}".format(dimension), line) and 0 < homesln < count:
            print("Found home")
            return(count - 1)
        count += 1

# Read every file in the userdata folder, call the scan function defined above, if a home is found
# go through the file and remove the associated lines, which is the line of the name, until that plus 6
# It then writes this to the file, reads the file again and checks if there are any more homes remaining
# from that dimension, if there are, it repeats. It stops and proceeds to the next file if there are none.
for filename in os.listdir(userdata_location):
    file_path = os.path.join(userdata_location, filename)
    print("Opening {0}".format(filename))
    with open(file_path, 'r') as f:
        ftext = f.read()
    dhomeln = scanln(ftext)
    while dhomeln:
        newf = ""
        count = 0
        for line in ftext.splitlines():
            if not ((count>= dhomeln) and (count<= dhomeln +6)):
                newf += "{0}\n".format(line)
            count += 1
        print("Removed home from {0}".format(filename))
        with open(file_path, 'w') as f:
            f.write(newf)
        with open(file_path, 'r') as f:
            ftext = f.read()
        dhomeln = scanln(ftext)

print("Done!")