import json
import logging
import datetime
from canvas.canvas import Canvas


def log_error(function_name,error_info,exception):
    error_message = f"time: {datetime.datetime.now()} - Error in function {function_name}:"
    error_log = f"{error_message}\n{error_info}\n{exception}\n"
    logging.error(error_log)

    return

def reduce_assignment(course_id, assignment_id):
    message = ''
    try:
        report = canvas.get_assignment_grades(course_id, assignment_id)
    except Exception as e:
        error_info = f"course_id: {course_id}, assignment_id: {assignment_id}"
        function_name = "canvas.get_assignment_grades()"
        log_error(function_name,error_info,str(e))
        return
    
    try:
        assignment_data = canvas.get_assignment(course_id,assignment_id)
        points_possible = int(assignment_data['points_possible'])
    except Exception as e:
        error_info = f"course_id: {course_id}, assignment_id: {assignment_id}"
        function_name = "canvas.get_assignment()"
        log_error(function_name,error_info,str(e))
        return

    for data in report:

        if data['grade'] is not None:
            grade, user_id = data['grade'], data['user_id']
            if int(round(float(grade))) > points_possible:
                try:
                    canvas.post_assignment_grade(course_id, assignment_id, user_id, points_possible)
                    message = f'{user_id} has been trimmed to {points_possible}\n'
                    logging.info(message)
                    print(message)
                except Exception as e:
                    error_info = f"course_id: {course_id}, assignment_id: {assignment_id}, user_id: {user_id}, "
                    function_name = "canvas.post_assignment_grade()"
                    log_error(function_name,error_info,str(e))
        else:
            pass




    if len(message) > 0:
        return
    else:
        message = f'No updates in {course_id} for assignment {assignment_id}\n'
        print(message)
        logging.info(message)
        return

def waive_late_assignment(course_id, assignment_id):
    message = ''
    try:
        report = canvas.get_assignment_grades(course_id, assignment_id)
    except Exception as e:
        error_info = f"course_id: {course_id}, assignment_id: {assignment_id}"
        function_name = "canvas.get_assignment_grades()"
        log_error(function_name,error_info,str(e))
        return

    for data in report:

        if (data['grade'] is not None) and (data['late'] is True):
            
            user_id = data['user_id']

            try:
                canvas.post_assignment_on_time(course_id, assignment_id, user_id)
                message = f'{user_id} has been marked on time\n'
                logging.info(message)
                print(message)
            except Exception as e:
                error_info = f"course_id: {course_id}, assignment_id: {assignment_id}, user_id: {user_id}, "
                function_name = "canvas.post_assignment_on_time()"
                log_error(function_name,error_info,str(e))

        else:
            pass

    if len(message) > 0:
        return
    else:
        message = f'No updates in {course_id} for assignment {assignment_id}\n'
        print(message)
        logging.info(message)
        return

def waive_assignment_group(course_id, assignment_group_id):
    
    try:
        report = canvas.get_assignment_groups(course_id)
    except Exception as e:
        error_info = f"course_id: {course_id}, assignment_group_id: {assignment_group_id},"
        function_name = "canvas.get_assignment_groups()"
        log_error(function_name,error_info,str(e))
        return

    for assignment_group in report:
        if assignment_group['id'] == assignment_group_id:
            assignment_group_assignments = assignment_group['assignments']
            break


    for assignment in assignment_group_assignments:
        waive_late_assignment(course_id, assignment['id'])

    return

if __name__ == '__main__':

    log_file = "config/error.log"
    reduce_config_file = "config/reduced_assignments.json"
    waived_config_file = "config/waived_assignments.json"

    instance = 'Test'
    canvas = Canvas(instance)

    # Configure the logging settings
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Log a message including the date and time
    log_message = f"\n {formatted_datetime} - Begin Run Time \n"
    logging.info(log_message)

    # Reduces course grades to the max points possible

    log_message = f"\n {formatted_datetime} - Reducing Course Grades \n"
    logging.info(log_message)

    file_name = reduce_config_file

    try:
        #reads from the reduced_assignments file
        with open(file_name, 'r') as f:
            course_list = json.load(f)
    except Exception as e:
        error_info = f"file_name: {file_name}"
        function_name = "open_file()"
        log_error(function_name,error_info,str(e))
        exit()

    for course_id in course_list:
        course = course_list[course_id]
        assignments = course['assignments']

        if len(assignments) >= 1:
            print("Checking Assignments")
            for assignment_id in assignments:
                reduce_assignment(course_id, assignment_id)
        

    
    # Waives late penalty for late assignments

    log_message = f"\n {formatted_datetime} - Waiving Late Penalties \n"
    logging.info(log_message)

    file_name = waived_config_file

    try:
        #reads from the waived_assignments file
        with open(file_name, 'r') as f:
            course_list = json.load(f)
    except Exception as e:
        error_info = f"file_name: {file_name}"
        function_name = "open_file()"
        log_error(function_name,error_info,str(e))
        exit()

    for course_id in course_list:
        course = course_list[course_id]
        assignments = course['assignments']
        assignment_groups= course['assignment_groups']

        if len(assignments) >= 1:
            print("Checking Assignments")
            for assignment_id in assignments:
                waive_late_assignment(course_id, assignment_id)
        
        if len(assignment_groups) >= 1:
            print("Checking Assignment Groups")
            for assignment_group_id in assignment_groups:
                assignment_group = assignment_groups[assignment_group_id]

                waive_assignment_group(course_id, assignment_group['id'])
    
        
    # Log a message including the date and time
    log_message = f"\n {formatted_datetime} - End Run Time \n"
    logging.info(log_message)
