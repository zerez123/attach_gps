import os
import sys
from pathlib import Path
import datetime
from datetime import datetime
import piexif
from PIL import Image
import argparse
from ExifUtils import ExifUtils

#{0: (2, 2, 0, 0), 1: b'N', 2: ((32, 1), (4, 1), (54631200, 1000000)), 3: b'E', 4: ((34, 1), (58, 1), (57748800, 1000000)), 5: 0, 6: 0}
#fname = './pics/P1090303.JPG'
fname = '/home/erez/Downloads/20240316_123345.jpg'

# Open the image file
print(fname)
img = Image.open(fname)
exif_dict = piexif.load(img.info['exif'])
print(exif_dict)