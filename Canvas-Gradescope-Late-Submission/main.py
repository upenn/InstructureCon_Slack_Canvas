import pandas as pd
import requests
from canvas import Canvas
import json
from slacker import Slacker
from datetime import timedelta
import datetime
from datetime import datetime
import gradescope


def load_json():
    with open("/slack_cred.json", 'r') as f:
        cred = json.load(f)
        return cred


def slack_bot(message=None, type=None):
    cred = load_json()
    bot = Slacker(cred["slack_token_staff"])
    channel = "{slack Channel ID}"
    bot_name = "ed_bot"

    if type == 'msg':
        bot.chat.post_message(channel, as_user=bot_name,
                              text=f"{message}")

    if type == 'file':
        bot.files.upload(channels=channel,
                         file_=f'/late_submissions.csv')


def get_student_id(student_id):
    canvs_id = '{}/api/v1/users/sis_user_id:{}'.format(canvas.server_url[f'{canvas.instance}'],
                                                       student_id)

    r = requests.get(canvs_id, headers=canvas.headers())

    if r.status_code == 200:

        # return json.dumps(r.json(), indent=4)
        print(r.json()['id'])
        return r.json()['id']
    else:
        raise Exception(f'{r.status_code},{r.text}')
    # return canvas.get_canvas_id(student_id)


def check_student_enrollment(student_id, course_id):
    user_enrollmenets = '{}/api/v1/users/sis_user_id:{}/enrollments'.format(canvas.server_url[f'{canvas.instance}'],
                                                                             student_id)
    playload = {'state[]': 'active'}

    r = requests.get(user_enrollmenets, headers=canvas.headers(), params=playload)

    if r.status_code == 200:

        for data in r.json():
            if course_id == data["course_id"]:
                # print('Yes')
                # print(data)
                return True
            else:
                print('wrong')
                return False
    else:

        raise Exception(f'{r.status_code},{r.text}')


def check_submission_time(course_id, assignment_id, user_id):
    get_submission_time = '{0}/api/v1/courses/{1}/assignments/{2}/submissions/sis_user_id:{3}'.format(
        canvas.server_url[f'{canvas.instance}'],
        course_id, assignment_id, user_id)

    r = requests.get(get_submission_time, headers=canvas.headers())

    if r.status_code == 200:

        timestamp = r.json()["submitted_at"]

        est_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=5)

        print(r.json()["submitted_at"])

        print(est_timestamp)
        return est_timestamp
    else:
        raise Exception(f'{r.status_code},{r.text}')


def upload_submission_time(course_id, assignment_id, user_id, submission_time):
    submisson_times = '{}/api/v1/courses/{}/assignments/{}/submissions'.format(
        canvas.server_url[f'{canvas.instance}'],
        course_id, assignment_id)

    student_canvas_id = get_student_id(user_id)

    playload = {'submission[user_id]': student_canvas_id, 'submission[submitted_at]': submission_time,
                'submission[submission_type]': 'basic_lti_launch',
                'submission[url]': 'https://www.gradescope.com/auth/lti/callback'}

    r = requests.post(submisson_times, headers=canvas.headers(), params=playload)

    if r.status_code == 201:
        return json.dumps(r.json(), indent=4)
    else:
        raise Exception(f'{r.status_code},{r.text}')


def access_files():
    df = pd.read_csv("/late_submissions.csv")

    df = df[df["Lateness (H:M:S)"] > '01:00:00']

    # print(type(df["Lateness (H:M:S)"]))

    message = ""

    for index, row in df.iterrows():
        # print(index, row)

        try:
            student_submission_time = check_submission_time(row['Canvas_course_id'], row['assignment_id'], row['SID'])

            new_time = datetime.strptime(row['submission_time'], '%Y-%m-%d %H:%M:%S')
            if student_submission_time is None or student_submission_time != new_time:

                upload_submission_time(row['Canvas_course_id'], row['assignment_id'], row['SID'],
                                       row['submission_time'])

                row = f"Uploaded {row['student_name']}'s late {row['assignment_name']} in {row['course_name']} \n"

                message += row

                print('no new submission time, and just updated')
            else:
                print("already upload submission time")
                pass

        except:
            print("wrong")
            pass

    # print(row['submission_time'])

    if len(message) > 0:
        slack_bot(message, 'msg')

        slack_bot(None, 'file')

    else:
        slack_bot('No late submissions', 'msg')


if __name__ == '__main__':
    instance = 'Production'
    canvas = Canvas(instance)

    gradescope.run_files()
    
    access_files()


 
   
