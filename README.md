# GPS Coordinate Attachment for JPG Images

## Overview

This project aims to attach GPS coordinates to JPG images captured with a camera that doesn't have a built-in GPS feature. The program leverages GPS recordings of the path where the pictures were taken and assumes that the camera's clock is correctly set. If the camera's clock is set to UTC time, no additional configuration is needed. However, if the camera's clock is set to local time, the time difference between the local time and UTC should be provided as an argument.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/gps-coordinate-attachment.git
   ```

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Record GPS Path

Before running the program, ensure you have recorded the GPS path where the pictures were taken. You can use any GPS recording device or application to do this.

### Step 2: Run the Program

1. Navigate to the project directory.
2. Run the program with the following command:

   ```
   python attach_gps.py /path/to/images /path/to/gps/recordings.gpx [--local-offset <offset_in_hours>]
   ```

   - `/path/to/images`: Path to the directory containing the JPG images.
   - `/path/to/gps/recordings.gpx`: Path to the GPX file containing the GPS recordings.
   - `--timediff <offset_in_hh:mm:ss>` (optional): If the camera's clock is set to local time, provide the time difference between the local time and UTC in hours.
   - `--cameradiff <offset_in_hh:mm:ss>` (optional): Time difference between the camera and the local time.

### Step 3: Check Results

The program will attach GPS coordinates to the JPG images in the specified directory. You can verify the results by checking the metadata of the images.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](LICENSE) file for details.
