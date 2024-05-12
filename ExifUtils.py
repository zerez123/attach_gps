import piexif
from PIL import Image


class ExifUtils:
    def __decimal_to_dms(self, decimal):
        degrees = int(decimal)
        minutes_decimal = (decimal - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60
        return (int(degrees), 1), (int(minutes), 1), (int(seconds * 1000000), 1000000)

    def get_exif_datetime(self, exif_data):
        return exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal]

    def get_exif_altitude_meter(self, exif_date):
        alt = exif_date['GPS'][piexif.GPSIFD.GPSAltitude]
        return alt[0] * alt[1]

    def set_exif_geoloc(self, exif_data, lat, lon, alt):
        lat_ref = b'N' if lat >= 0 else b'S'
        lon_ref = b'E' if lon >= 0 else b'W'
        version = (2, 2, 0, 0)

        # Construct GPS data dictionary

        exif_data['GPS'][piexif.GPSIFD.GPSLatitude] = self.__decimal_to_dms(abs(lat))
        exif_data['GPS'][piexif.GPSIFD.GPSLatitudeRef] = lat_ref
        exif_data['GPS'][piexif.GPSIFD.GPSLongitude] = self.__decimal_to_dms(abs(lon))
        exif_data['GPS'][piexif.GPSIFD.GPSLongitudeRef] = lon_ref
        exif_data['GPS'][piexif.GPSIFD.GPSVersionID] = (2, 2, 0, 0)

        # The GPS lat and lon stored in hr min sec format:
        # 0:(2,2,0,0) -> Version
        # 1:'N' 2:((31,1),(23,1),(23071559,1000000)) -> N31 23 23.071559
        # 3:'E' 4:((34,1),(27,1),(28693800,1000000)) -> E34 27 28.6938
        return exif_data

    def set_exif_datetime(self, exif_dict, new_creation_date):
        date_string = new_creation_date.strftime("%Y-%m-%d %H:%M:%S")
        # Modify the creation date in the EXIF data
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_string.encode("utf-8")
        return exif_dict
