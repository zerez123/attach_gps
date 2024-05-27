import argparse
import datetime


def parse_time_offset(offset_str):
    try:
        # Split the offset string into hours, minutes, and seconds
        offset_parts = offset_str.split(':')

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

        # Determine sign of the offset
        sign = 1 if hours >= 0 else -1

        # Calculate total offset in seconds
        total_seconds = sign * (abs(hours) * 3600 + minutes * 60 + seconds)

        # Create a timedelta object representing the time offset
        offset = datetime.timedelta(seconds=total_seconds)

        return offset
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid time offset format. Use format hh, hh:mm, or hh:mm:ss")


# Assuming creation_date is a datetime.datetime object
# Assuming cameradif is a datetime.timedelta object

# Example creation_date and cameradif objects
creation_date = datetime.datetime(2024, 5, 15, 12, 30, 0)
cameradif = 10

# Add cameradif to creation_date
creation_date = creation_date + datetime.timedelta(seconds=cameradif)

# Print the updated creation_date
print(creation_date)


def main():
    parser = argparse.ArgumentParser(description="Add time offset to current time")
    parser.add_argument("--offset", type=parse_time_offset, help="Time offset in format hh:mm:ss")
    args = parser.parse_args()
    offset = args.offset if args.offset is not None else datetime.timedelta(0)

    current_time = datetime.datetime.now()
    new_time = current_time + offset
    print(f"Current time: {current_time}")
    print(f"Time offset: {args.offset}")
    print(f"New time: {new_time}")


if __name__ == "__main__":
    main()
