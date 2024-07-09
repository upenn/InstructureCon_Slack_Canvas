import requests
import json
from dotenv import load_dotenv
import os

load_dotenv('Config/.env')
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
CANVAS_TEST_TOKEN = os.getenv("TEST_CANVAS_TOKEN")

class Canvas:
    def __init__(self, instance):
        server_url = {'Prod': 'https://canvas.upenn.edu', 
                      'Test': 'https://upenn.test.instructure.com'}

        self.instance = instance
        self.server_url = server_url[instance]
        self.access_token = self.get_token(instance)

    def get_token(self=None, instance=None):

        if instance == 'Test':
            cred = CANVAS_TEST_TOKEN
        else:
            cred = CANVAS_TOKEN 

        return cred

    def headers(self):
        headers = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(self.access_token)
        }
        
        return headers

    def post_assignment_grade(self, course_id, assignment_id, student_id, post_grade):

        assignment_grade = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{student_id}'

        payload = {'submission[posted_grade]': post_grade}

        r = requests.put(assignment_grade, headers=self.headers(), params=payload)

        if r.status_code == 200:
            return json.dumps(r.json(), indent=4)
        else:
            raise Exception(r.status_code,r.text)
        
    def post_assignment_on_time(self, course_id, assignment_id, student_id):
        assignment_grade = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions/{student_id}'

        payload = {'submission[late_policy_status]': 'none'}

        r = requests.put(assignment_grade, headers=self.headers(), params=payload)

        if r.status_code == 200:
            return json.dumps(r.json(), indent=4)
        else:
            raise Exception(r.status_code,r.text)

    def post_assignment_override(self, course_id, assignment_id, student_ids, due_date, unlock_date, lock_date):

        override = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/overrides/'

        title = f'{len(student_ids)} students'

        sis_ids = []
        for student in student_ids:
            sis_ids.append(f'sis_user_id:{student}')

        payload = {'assignment_override[student_ids][]': sis_ids,
                   'assignment_override[title]': title,
                   'assignment_override[due_at]': due_date,
                    'assignment_override[unlock_at]': unlock_date,
                    'assignment_override[lock_at]': lock_date,
                   }

        r = requests.post(override, headers=self.headers(), params=payload)

        if r.status_code == 201:
            return json.dumps(r.json(), indent=4)
        else:
            raise Exception(r.status_code,r.text)
        



    def get_assignment_grades(self, course_id, assignment_id):

        student_grade = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions?per_page=100'

        r = requests.get(student_grade, headers=self.headers())

        raw  = r.json()

        data_set = []

        for question in raw:

            data_set.append(question)
        
        while r.links['current']['url'] != r.links['last']['url']:

            r = requests.get(r.links['next']['url'], headers=self.headers())

            raw = r.json()

            for question in raw:

                data_set.append(question)

        if r.status_code == 200:
            return data_set
        else:
            raise Exception(r.status_code,r.text)
        
    def get_assignment_groups(self, course_id):

        assignment_groups = f'{self.server_url}/api/v1/courses/{course_id}/assignment_groups'


        payload = {'include[]': ['assignments']}

        r = requests.get(assignment_groups, headers=self.headers(), params=payload)

        raw = r.json()

        data_set = []

        for group in raw:

            data_set.append(group)
        
        while r.links['current']['url'] != r.links['last']['url']:

            r = requests.get(r.links['next']['url'], headers=self.headers())

            raw = r.json()

            for group in raw:

                data_set.append(group)


        if r.status_code == 200:
            return data_set
        else:
            raise Exception(r.status_code,r.text)

    def get_assignment(self, course_id, assignment_id):

        assignment_data = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/'

        r = requests.get(assignment_data, headers=self.headers())

        raw  = r.json()

        if r.status_code == 200:
            return raw
        else:
            raise Exception(r.status_code,r.text)

    def get_assignment_overrides(self, course_id, assignment_id):

        assignment_data = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/overrides'

        r = requests.get(assignment_data, headers=self.headers())

        raw  = r.json()

        if r.status_code == 200:
            return raw
        else:
            raise (r.status_code,r.text)
        
    def get_course(self, course_id):
            assignment_data = f'{self.server_url}/api/v1/courses/{course_id}/'

            r = requests.get(assignment_data, headers=self.headers())

            raw  = r.json()

            if r.status_code == 200:
                return raw
            else:
                raise Exception(r.status_code,r.text)   
            
    def get_students(self, course_id):
            assignment_data = f'{self.server_url}/api/v1/courses/{course_id}/students'

            r = requests.get(assignment_data, headers=self.headers())

            raw  = r.json()

            if r.status_code == 200:
                return raw
            else:
                raise Exception(r.status_code,r.text)



    def delete_assignment_override(self, course_id, assignment_id, override_id):

        assignment_data = f'{self.server_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/overrides/{override_id}'

        r = requests.delete(assignment_data, headers=self.headers())

        raw  = r.json()

        if r.status_code == 200:
            return raw
        else:
            raise Exception(r.status_code,r.text)
        
    def get_quiz_submissions(self, course_id, quiz_id):

        quiz_submissions = f'{self.server_url}/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions?per_page=100'

        r = requests.get(quiz_submissions, headers=self.headers())

        raw  = r.json()

        data_set = []

        for submission in raw['quiz_submissions']:

            data_set.append(submission)
        
        while r.links['current']['url'] != r.links['last']['url']:

            r = requests.get(r.links['next']['url'], headers=self.headers())

            raw = r.json()

            for submission in raw['quiz_submissions']:

                data_set.append(submission)

        if r.status_code == 200:
            return data_set
        else:
            raise Exception(r.status_code,r.text)

    def put_fudge_points(self,course_id, quiz_id,submission_id,points):
            
            quiz_submission = f'{self.server_url}/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}'
    
            
            payload = {'quiz_submissions[][fudge_points]': points,
                       'quiz_submissions[][attempt]': 1
                       }
    
            r = requests.put(quiz_submission, headers=self.headers(), params=payload)
    
            if r.status_code == 200:
                return json.dumps(r.json(), indent=4)
            else:
                raise Exception(r.status_code,r.text)
    
    def put_regrade_exam_question(self,course_id, quiz_id,submission_id,question,points):
          
            quiz_submission = f'{self.server_url}/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions/{submission_id}'
    
            
            payload = {'quiz_submissions[][attempt]': 1,
                       'quiz_submissions[][questions]': {
                            question: {'score': points,'comment':""},
                            }
                        }   
            
            payload = {
                'quiz_submissions': [
                    {
                        'attempt': 1,
                        'questions': {
                            question: {
                                'score': points,
                                'comment': ""
                            }
                        }
                    }
                ]
            }
    
            r = requests.put(quiz_submission, headers=self.headers(), json=payload)
    
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception(r.status_code,r.text)
    
    def get_paginated_data(self, url):
        data_set = []
        r = requests.get(url, headers=self.headers())

        if r.status_code != 200:
            r.raise_for_status()

        data_set.extend(r.json())

        while 'next' in r.links and r.links['current']['url'] != r.links['last']['url']:
            r = requests.get(r.links['next']['url'], headers=self.headers())
            if r.status_code != 200:
                r.raise_for_status()
            data_set.extend(r.json())

        return data_set

    def get_module_items(self, course_id, module_id):
        url = f"{self.server_url}/api/v1/courses/{course_id}/modules/{module_id}/items?per_page=100"
        return self.get_paginated_data(url)

    def get_modules(self, course_id):
        url = f"{self.server_url}/api/v1/courses/{course_id}/modules?per_page=100"
        return self.get_paginated_data(url)


    def get_module(self,course_id,module_id):
        url = f"{self.server_url}/api/v1/courses/{course_id}/modules/{module_id}"
    
        r = requests.get(url, headers=self.headers())
        
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

    def get_wiki_page(self, course_id, page_id):
        url = f"{self.server_url}/api/v1/courses/{course_id}/pages/{page_id}"
        r = requests.get(url, headers=self.headers())
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

    def get_new_quiz(self, course_id, quiz_id):
        url = f"{self.server_url}/api/quiz/v1/courses/{course_id}/quizzes/{quiz_id}"
        r = requests.get(url, headers=self.headers())
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

    def get_new_quizes(self, course_id):
        url = f"{self.server_url}/api/quiz/v1/courses/{course_id}/quizzes"
        r = requests.get(url, headers=self.headers())
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

    def get_file(self, course_id, file_id):
        url = f"{self.server_url}/api/v1/courses/{course_id}/files/{file_id}"
        r = requests.get(url, headers=self.headers())
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()