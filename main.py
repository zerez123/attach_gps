import os
from pathlib import Path
import datetime
import piexif
from PIL import Image
import argparse
from ExifUtils import ExifUtils
from GpxUtils import GpxUtils

exifu = ExifUtils()
gpxu = GpxUtils()


def parse_time_offset(offset_str):
    try:
        # Split the offset string into hours, minutes, and seconds
        offset_parts = offset_str.split(':')

        if offset_parts[0].startswith('-'):
            sign = -1
        else:
            sign = 1
        # Determine the number of parts in the offset string
        num_parts = len(offset_parts)

        # Default values for minutes and seconds
        minutes = 0
        seconds = 0

        # Handle different cases based on the number of parts
        if num_parts == 1:
            # Only hours provided
            hours = int(offset_parts[0])
        elif num_parts == 2:
            # Hours and minutes provided
            hours = int(offset_parts[0])
            minutes = int(offset_parts[1])
        elif num_parts == 3:
            # Hours, minutes, and seconds provided
            hours = int(offset_parts[0])
            minutes = int(offset_parts[1])
            seconds = int(offset_parts[2])
        else:
            raise ValueError

        # Calculate total offset in seconds
        total_seconds = sign * (abs(hours) * 3600 + minutes * 60 + seconds)

        # Create a timedelta object representing the time offset
        #offset1 = datetime.timedelta(seconds=total_seconds)

        return total_seconds
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid time offset format. Use format hh, hh:mm, or hh:mm:ss")


def convert_to_datetime(str):
    # Define the format of your string b'2024:03:16 12:34:04'
    format_string = "%Y:%m:%d %H:%M:%S"

    # Convert byte string to a regular string
    date_string = str.decode('utf-8')

    # Parse the string into a datetime object
    date_time_obj = datetime.datetime.strptime(date_string, format_string)

    # Now date_time_obj contains the datetime object
    return date_time_obj


def main():
    # Create the command line parser
    parser = argparse.ArgumentParser(
        description='This program takes a folder containing JPG images and a GPS record as '
                    'arguments. It then extracts the coordinates from the GPS record and '
                    'adds them to the metadata of each JPG image, indicating the location '
                    'where the picture was taken.')
    parser.add_argument('folder', type=str, help='The folder that contains the images')
    parser.add_argument('gpx', type=str, help='Full path to the GPX file')
    parser.add_argument('--timediff', type=parse_time_offset,
                        help='Time difference between the image time(local) and the gps time (utc) format hh:mm:ss')
    parser.add_argument('--cameradiff', type=parse_time_offset,
                        help='Time difference between the camera and the local time format hh:mm:ss')
    parser.add_argument('--olalt', type=int, help='if 1 Use on line altitude')

    # Parse the command-line arguments
    args = parser.parse_args()
    path = args.folder
    gpx_file = args.gpx
    timedif = args.timediff if args.timediff is not None else 0
    cameradif = args.cameradiff if args.cameradiff is not None else 0
    using_online_alt = args.olalt if args.olalt is not None else 0

    # Get the list of the files in a folder
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
        img = Image.open(fname)
        exif_dict = piexif.load(img.info['exif'])
        # And read the creation date time
        creation_date = convert_to_datetime(exifu.get_exif_datetime(exif_dict))
        creation_date = creation_date + datetime.timedelta(seconds=cameradif)
        gps_point = gpxu.gpx_get_godata_by_date(creation_date, using_online_alt)
        print("File: ", fname, "Creation date: ", creation_date.strftime("%Y-%m-%d %H:%M:%S"), "Location: ", gps_point)
        if gps_point:
            # And save the modified image with new file name
            exif_dict = exifu.set_exif_geoloc(exif_dict, gps_point[0], gps_point[1], gps_point[2])
            if cameradif != 0:
                datetime_str = creation_date.strftime("%Y:%m:%d %H:%M:%S")
                datetime_bytes = byte_data = datetime_str.encode('utf-8')
                exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime_bytes
            exif_bytes = piexif.dump(exif_dict)
            img.save('_%s' % fname, "jpeg", exif=exif_bytes)
    # Finally restore the original folder and exit
    os.chdir(original_path)


if __name__ == "__main__":
    main()
