# Tempify, a CSV Processor

Tempify is a Python application built with Tkinter that allows you to quickly upload and process CSV files containing temperature data generated from exporting data from the Mocreo mobile app. It calculates the average temperature for each individual date in the file, automatically detects which months' data it's processing, and displays the results in a user-friendly, easy-to-read, one-page Excel template that is ready for printing.

## Features

- Load one-by-one or multiple CSV files at once
- Calculate the average temperature for each date in the file based on the expected Mocreo output format
- Display up to 8 files' results in a list of scrollable content boxes
- Copy Data button to copy the processed data to the clipboard in a format suitable for Excel
- Clear All results button to remove all displayed results
- Remove Single result button to remove individual content boxes

## Prerequisites

- Python 3.x
- pandas library

## Installation

Tempify is a portable Windows application so you simply download the executable and launch it. Due to it being a customized Python program without (valid) certificates that aren't recognized by Windows, a security prompt will likely appear. Click 'Run anyway' to start the application if you run into this.

## Usage
**Note:** It is assumed that you have already logged onto the Mocreo portal website to export all the historical data you want to extract in individual CSV files per sensor.

1. Run the Tempify application, and the main window will open.

2. Click the "Load CSV(s)" button to select one or multiple CSV files containing temperature data.

3. The application will process the selected files and display the results in separate content boxes.

4. To copy the processed data for easy pasting into Excel, click the "← Copy Data" button on the corresponding content box. The data will be copied to your clipboard.

5. To clear all the results, click the "Clear" button. To remove a single content box, click the red "X" button to the left of each file's results.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE.md).
