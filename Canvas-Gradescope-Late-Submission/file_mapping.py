import pandas as pd

# df = pd.read_csv('/Users/minghaotao/Desktop/GS_Late/CIS_5810_-_Spring_2023_Spring_2023_grades.csv')
#
# print(df.columns)

course_url = {
    '5500': 'https://gradescope.com/courses/{Gradescope course ID}/gradebook.csv',
    '5810': '',

}

canvas_id_map = {"5500": {Canvas Course ID},
                 "5810": {Canvas Course ID}
    
                 }

assignment_map = {"5500": {"Homework 1 - Submission Time": {Canvas Assignment ID}, "Homework 2 - Submission Time": 10711033,
                           "Homework 3 - Submission Time": 10711034, "Homework 4 - Submission Time": 10711035,
                           "Homework 5 - Submission Time": 10711036, "Homework 6 - Submission Time": 10711037},
                  "5810": {
                  }

                  }

filters = {"5500": ["First Name", "Last Name", "Name", "SID", "Email", "Sections",
                    "Homework 1 - Submission Time",
                    "Homework 1 - Lateness (H:M:S)",
                    "Homework 2 - Submission Time",
                    "Homework 2 - Lateness (H:M:S)",
                    "Homework 3 - Submission Time",
                    "Homework 3 - Lateness (H:M:S)",
                    "Homework 4 - Submission Time",
                    "Homework 4 - Lateness (H:M:S)",
                    "Homework 5 - Submission Time",
                    "Homework 5 - Lateness (H:M:S)",
                    "Homework 6 - Submission Time",
                    "Homework 6 - Lateness (H:M:S)"],
           "5810": [
           ]

           }
