import os
import sys
from pathlib import Path
import datetime
from datetime import datetime
import piexif
from PIL import Image
import argparse
from ExifUtils import ExifUtils
from GpxUtils import GpxUtils


#path = "/home/erez/Pictures"
#fname = "IMG_3724.JPG"

#path = "/home/erez/Downloads"
fname = "20240316_123404.jpg"

exifu = ExifUtils()
gpxu = GpxUtils()

# Create the command line parser
parser = argparse.ArgumentParser(description='This program takes a folder containing JPG images and a GPS record as arguments. It then extracts the coordinates from the GPS record and adds them to the metadata of each JPG image, indicating the location where the picture was taken.')
parser.add_argument('folder', type=str, help='The folder that contains the images')
parser.add_argument('gpx', type=str, help='Full path to the GPX file')
parser.add_argument('--timedif', type=int, help='Time diferance between the image time(local) and the gps time (utc')


def convert_to_datetime(str):

    # Define the format of your string b'2024:03:16 12:34:04'
    format_string = "%Y:%m:%d %H:%M:%S"

    # Convert byte string to a regular string
    date_string = str.decode('utf-8')

    # Parse the string into a datetime object
    date_time_obj = datetime.strptime(date_string, format_string)

    # Now date_time_obj contains the datetime object
    return(date_time_obj)


def main():

    # Parse the command-line arguments
    args = parser.parse_args()
    path = args.folder
    gpx_file = args.gpx
    if args.timedif:
        timedif = args.timedif
    else:
        timedif = 0

    #Get the list of the files in a folder
    folder_path = Path(path)
    files_list = [file.name for file in folder_path.iterdir() if file.is_file()]
    jpg_files_list = [file for file in files_list if file.lower().endswith('.jpg')]

    # Save the current path and change to the working path
    original_path = os.getcwd()
    os.chdir(path)

   # Read the GPX file
    gpxu.gpx_read_route(gpx_file, timedif)

    # Run over the GPX file in the folder
    for fname in jpg_files_list:
        # Open the image file
        print(fname)
        img = Image.open(fname)
        exif_dict = piexif.load(img.info['exif'])
        # And read the creation date time
        creation_date = convert_to_datetime(exifu.get_exif_datetime(exif_dict))
        gps_point = gpxu.gpx_get_godata_by_date(creation_date)
        print(creation_date)
        print(gps_point)
        if gps_point:
            # And save the modified image with new file name
            exif_bytes = piexif.dump(exif_dict)
            img.save('_%s' % fname, "jpeg", exif=exif_bytes)

    # Finally restore the original folder and exit
    os.chdir(original_path)


if __name__ == "__main__":
    main()
