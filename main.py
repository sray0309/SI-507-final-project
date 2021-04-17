import schools.michigan, schools.berkeley, schools.mit
import requests
import sqlite3
from bs4 import BeautifulSoup
import scopus

SCHOOL_LIST = ['University of Michigan', 'University of California, Berkeley', 'Massachusetts Institute of Technology']
SCHOOL_DICT = {
    'University of Michigan': 'michigan',
    'University of California, Berkeley': 'berkeley',
    'Massachusetts Institute of Technology': 'mit'}
RESEARCH_FIELDS = []

class Faculty:

    def __init__(self, school, firstname, lastname, title, research_interests, web, email):
        self.firstname = firstname
        self.lastname = lastname
        self.school = school
        self.title = title
        self.research_interests = research_interests
        self.web = web
        self.email = email

    def __str__(self):
        return f"{self.firstname} {self.lastname} from {self.school}"

def load_data():
    connection = sqlite3.connect('faculty.sqlite')
    cursor = connection.cursor()
    create_table = '''
        CREATE TABLE IF NOT EXISTS "faculty" (
            "Id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "School"    TEXT NOT NULL,
            "FirstName" TEXT NOT NULL,
            "LastName" TEXT NOT NULL,
            "Title"  TEXT NOT NULL,
            "ResearchInterests"   TEXT,
            "PersonalWeb"    TEXT,
            "Email" TEXT);'''
    cursor.execute(create_table)
    connection.commit()
    print('########## Loading data... ##########')
    schools.michigan.check_data()
    schools.berkeley.check_data()
    schools.mit.check_data()
    print('########## Finish loading ##########')

def retrieve_data_from_database(school):
    connection = sqlite3.connect('faculty.sqlite')
    cursor = connection.cursor()
    query = f'''
    SELECT faculty.FirstName, faculty.LastName, faculty.Title, faculty.ResearchInterests, faculty.PersonalWeb, faculty.email from faculty
    WHERE faculty.School = '{school}'
    ORDER BY faculty.FirstName, faculty.LastName
    '''
    results = cursor.execute(query).fetchall()
    return results

def interactive_prompt():
    while True:
        for i in range(len(SCHOOL_LIST)):
            print(f'{i+1}: {SCHOOL_LIST[i]}')
        user_input = input('please choose a school number or exit: \n')
        if user_input == 'exit':
            break
        if not user_input.isnumeric():
            print('please input a number')
            continue
        if int(user_input)-1 not in range(len(SCHOOL_LIST)):
            print('Missing data, please choose from the list below')
            continue
        school = SCHOOL_DICT[SCHOOL_LIST[int(user_input)-1]]
        results = retrieve_data_from_database(school)

        print(results)

if __name__=="__main__":
    load_data()
    interactive_prompt()

