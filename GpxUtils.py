import gpxpy
from gpxpy import gpx
from datetime import datetime, timedelta

import pytz
from timezonefinder import TimezoneFinder

use_local_time = False

gpx_point_list = []

import requests

class GpxUtils:
    def __get_elevation(self, lat, lon):
        url = "https://api.open-elevation.com/api/v1/lookup"
        params = {
            'locations': f'{lat},{lon}'
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            if 'results' in result:
                elevation = result['results'][0]['elevation']
                return elevation
            else:
                print("Error fetching elevation data.")
                return None
        else:
            print(f"HTTP error: {response.status_code}")
            return None

    def __interpolate_coordinates(self, time_taken, gps_point_before, gps_point_after, using_online_alt):
        alt_interpolated = 0
        # Extract coordinates and timestamps from the GPS points
        lat_before, lon_before, time_before = gps_point_before
        lat_after, lon_after, time_after = gps_point_after

        if time_before < time_taken < time_after:
            # Calculate the time difference between before and after points
            time_diff = (time_after - time_before).total_seconds()

            # Calculate the time difference between time taken and time before
            time_diff_taken_before = (time_taken - time_before).total_seconds()

            # Calculate the proportion of time that has passed between before and after points
            proportion = time_diff_taken_before / time_diff

            # Interpolate latitude and longitude
            lon_interpolated = lon_before + proportion * (lon_after - lon_before)
            lat_interpolated = lat_before + proportion * (lat_after - lat_before)
            if using_online_alt > 0:
                elevation = self.__get_elevation(lat_interpolated, lon_interpolated)
                if elevation is not None:
                    alt_interpolated = elevation

            return lat_interpolated, lon_interpolated, alt_interpolated, time_taken


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

    def gpx_get_godata_by_date(self, date_time, using_online_alt):
        item_before = gpx_point_list[0]
        for item in gpx_point_list:
            if date_time < item[2]:
                return self.__interpolate_coordinates(date_time, item_before, item, using_online_alt)
            item_before = item
