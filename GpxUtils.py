import gpxpy
from gpxpy import gpx
from datetime import datetime, timedelta

import pytz
from timezonefinder import TimezoneFinder

use_local_time = False

gpx_point_list = []


class GpxUtils:

    def __utc_to_local(self, utc_time, lat, lon):
        if use_local_time:
            # Find the time zone
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lat=lat, lng=lon)
            location_timezone = pytz.timezone(timezone_str)

            # Define the format string
            format_string = "%Y-%m-%dT%H:%M:%SZ"  # UTC format string with 'Z'
            # Convert datetime to UTC string
            utc_time_string = utc_time.strftime(format_string)
            utc_time = datetime.strptime(utc_time_string, "%Y-%m-%dT%H:%M:%SZ")
            # Convert to local time
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(location_timezone)
        else:
            local_time = utc_time
        return local_time

    def gpx_read_route(self, gpx_filename, timedif):
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    current_time = self.__utc_to_local(point.time, point.latitude, point.longitude)
                    current_time = current_time.replace(tzinfo=None) + timedelta(seconds=timedif)
                    current_point = (point.latitude, point.longitude, current_time)
                    gpx_point_list.append(current_point)

    def gpx_get_godata_by_date(self, date_time):
        for item in gpx_point_list:
            if date_time < item[2]:
                return item
