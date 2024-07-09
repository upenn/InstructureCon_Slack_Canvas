
# Gradescope Late Submission Documentation

This repository contains a collection of Python scripts designed to interact with the Gradescope and Canvas platforms for managing student data, late submissions, and assignment grades. Below is an overview of each script and its functionality. The code was written by Drew Hopkins & Edward Tao. 

## `file_mapping.py`

This script contains mappings and configurations related to courses, assignments, and filters. Here's a breakdown of its contents:

- `course_url`: A dictionary that maps course numbers to their Gradescope URLs.
- `canvas_id_map`: A mapping of course numbers to Canvas Course IDs.
- `assignment_map`: Maps course numbers to assignments, linking assignment names to Canvas Assignment IDs.
- `filters`: Specifies which columns should be included in the data for each course number.

## `Gradescope.py`

`Gradescope.py` defines functions to interact with the Gradescope platform for downloading, processing, and analyzing student data. Key functions include:

- `download_data(course_number)`: Downloads student data from the specified course using the Gradescope API and returns it as a Pandas DataFrame.
- `clear_file()`: Clears the contents of a CSV file to prepare for new data.
- `late_columns(df)`: Extracts columns related to lateness from the DataFrame.
- `get_canvas_course_id(df)`: Extracts Canvas Course IDs from the DataFrame.
- `get_late_submission_time(df, late_column_name, course_number)`: Processes late submission data and saves it to a CSV file.
- `read_data(course_number)`: Coordinates the data extraction and transformation process for a given course.
- `run_files()`: Initiates the data processing for all configured courses.

## `main.py`

`main.py` serves as the entry point for running the entire workflow, including interactions with the Canvas API and Slack notifications. Key functions and tasks include:

- `load_json()`: Loads Slack credentials from a JSON file.
- `slack_bot(message=None, type=None)`: Sends messages and files to Slack channels.
- Functions for interacting with the Canvas API:
  - `get_student_id(student_id)`: Retrieves Canvas User IDs based on SIS User IDs.
  - `check_student_enrollment(student_id, course_id)`: Checks if a student is enrolled in a specific course.
  - `check_submission_time(course_id, assignment_id, user_id)`: Retrieves submission times for assignments.
  - `upload_submission_time(course_id, assignment_id, user_id, submission_time)`: Uploads submission times to Canvas.
- `access_files()`: Processes late submissions, checks submission times, and uploads them to Canvas.
- The `if __name__ == '__main__':` block initiates the workflow when the script is run.

## `SEAS_Canvas.py`

`SEAS_Canvas.py` defines a class, `Canvas`, for interacting with the Canvas API. It includes methods for managing assignments, grades, and user data.

Please note that certain aspects of the code, such as file paths and credentials, are configured for specific environments and may require customization to work in different setups.

Before running the code, ensure that you have the necessary API credentials, file paths, and dependencies installed.

This README.md provides an overview of the code's functionality, but further details on how to set up and configure the code may be needed depending on your specific use case and environment.


# Canvas-Late-and-Grade-Reduction

This repository contains Python scripts and related files for automating grade adjustments within Canvas LMS.

## Table of Contents

- [Files](#files)
  - [grade_adjustments.py](#grade_adjustmentspy)
  - [run_grade_adjustments.sh](#run_grade_adjustmentssh)
  - [crontab](#crontab)
  - [canvas/canvas.py](#canvascanvaspy)
  - [config/config_vars.py](#configconfig_varspy)

## Files

### grade_adjustments.py

- **Description**: This Python script automates the process of adjusting grades in Canvas based on specific criteria. It communicates with the Canvas API to perform grade adjustments waiving late submissions, and reducing grades that are over the maximum point value.

- **Usage**: To use this script, follow these steps:
  1. Configure the script settings, including Canvas LMS instance details and file paths.
  2. Run the script by executing it with Python.

### run_grade_adjustments.sh

- **Description**: This Bash script simplifies the execution of `grade_adjustments.py`. It handles the virtual environment activation and script execution process. This can be used to set a crontab that runs regularly.

- **Usage**: To run the grade adjustment script using this Bash script, open your terminal, navigate to the repository's root directory, and execute the Bash script:
   ```shell
   ./run_grade_adjustments.sh

### crontab

**Description**: This file contains a crontab configuration that schedules the automated execution of the grade adjustment script at specific intervals or times. Crontab is used for task automation on Unix-like systems.

**Usage**: To set up automated grade adjustments, add the contents of this crontab file to your system's crontab configuration, specifying when and how often you want the grade adjustments to run.

---

### canvas/canvas.py

**Description**: This Python module, located in the canvas directory, provides functionality for interacting with the Canvas API. It is utilized by grade_adjustments.py for communicating with Canvas LMS.

**Usage**: This module is imported and used by grade_adjustments.py. You do not need to run it directly.

---

### config/config_vars.py

**Description**: This Python file contains configuration variables used by the grade adjustment script and other components. It may include settings like API keys, Canvas LMS endpoints, or file paths. Dotenv can be used to create a .env file to store your access token.

**Usage**: Customize the variables in this file to match your specific Canvas LMS setup and preferences. Ensure that the script references these variables correctly for proper execution.

# Slack Bolt Integration

Please note that the code for the Slack Bolt integration is not shared in this repository. This is due to the personal scope of its development, and it is recommended that individuals interested in similar functionality develop their own integration tailored to their specific needs.

Slack Bolt is a framework that simplifies the creation of Slack apps using JavaScript, Python, or Java. For more information on how to get started with Slack Bolt, please refer to the official documentation:

- [Slack Bolt for JavaScript](https://slack.dev/bolt-js/tutorial/getting-started)
- [Slack Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)

These resources provide comprehensive guides on setting up and developing Slack applications, including how to handle events, commands, and interactive components.

# Canvas Extension Syncing

Our extension sync script is currently in active testing. This script will automate the synchronization of assignment extensions between Canvas and Gradescope. Once the testing phase is complete and the script is stable, it will be added to the repository for public use.

---
