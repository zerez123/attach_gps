import piexif
from PIL import Image


class ExifUtils:
    def get_exif_datetime(self, exif_data):
        return exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal]

    def get_exif_altitude_meter(self, exif_date):
        alt = exif_date['GPS'][piexif.GPSIFD.GPSAltitude]
        return alt[0] * alt[1]

    def set_exif_geoloc(self, exif_data, altitude):
        # Set the GPS altitude
        # The GPS altitude format:
        # (167,3) -> Altitude 167/3 meter
        alt_div = altitude // 256 + 1
        alt = (altitude // alt_div, alt_div)
        exif_data['GPS'][piexif.GPSIFD.GPSAltitude] = alt
        # The GPS lat and lon stored in hr min sec format:
        # 0:(2,2,0,0) -> Version
        # 1:'N' 2:((31,1),(23,1),(23071559,1000000)) -> N31 23 23.071559
        # 3:'E' 4:((34,1),(27,1),(28693800,1000000)) -> E34 27 28.6938
