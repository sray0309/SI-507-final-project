import schools.michigan, schools.berkeley, schools.mit
import requests
import sqlite3
from bs4 import BeautifulSoup
import show_detail
import scopus

SCHOOL_LIST = ['University of Michigan', 'University of California, Berkeley', 'Massachusetts Institute of Technology']
SCHOOL_DICT = {
    'University of Michigan': 'michigan',
    'University of California, Berkeley': 'berkeley',
    'Massachusetts Institute of Technology': 'mit'}

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
        print ('-'*142)
        num = 1
        for result in results:
            name = result[0] + ' ' + result[1]
            if len(result[3]) > 100:
                researchinterests = result[3][:97]+'...'
            else:
                researchinterests = result[3]
            print('|', num, '|', name.ljust(30) , '|', researchinterests.ljust(100), '|')
            num += 1
        print ('-'*142)
        print('''
################################################################################################################
#### enter a faculty number to check details                                                                ####
#### options:                                                                                               ####
####     <info>: show detail in terminal, include title, full research interests and contact information    ####
####     <detail>: show detail in browser, include SCOPUS personal web and publication details              ####
#### examples:                                                                                              ####
####     1 info                                                                                             #### 
####     23 detail                                                                                          ####
####     28 info                                                                                            ####
################################################################################################################
        ''')
        finish = False
        browser = False
        while(True):
            faculty_num = input('please enter a faculty number to check details(or exit or back to choose another school): ')
            if faculty_num == 'back':
                break
            elif faculty_num == 'exit':
                finish = True
                break
            else:
                command = faculty_num.split(' ')
                if len(command) != 2:
                    print('please enter proper command')
                    continue
                elif not command[0].isnumeric:
                    print('please enter a number')
                    continue
                elif int(command[0]) < 1 or int(command[0]) > len(results):
                    print('number out of range')
                    continue
                elif command[1] == 'info':
                    print('')
                    print('[name]:', results[(int(command[0])-1)][0], results[(int(command[0])-1)][1])
                    print('[title]:', results[(int(command[0])-1)][2])
                    print('[research interests]:', results[(int(command[0])-1)][3])
                    print('[personal web]:', results[(int(command[0])-1)][4])
                    print('[email]:', results[(int(command[0])-1)][5])
                    print('')
                elif command[1] == 'detail':
                    return results[(int(command[0])-1)][0], results[(int(command[0])-1)][1], school
        if finish:
            break
    return None

def show_in_browser(firstname, lastname, affil):
    main_default = open('templates/main_template.html', 'r')
    main_template = open('templates/main.html', 'w')
    main_read = main_default.read()
    main_default.close()
    # change template content
    auth_id = scopus.find_id(firstname, lastname, affil)
    if auth_id == None:
        print('Cannot find this faculty in SCOPUS')
        return None
    main_write = main_read.replace('name', f'{firstname} {lastname}')
    main_write = main_write.replace('scopus_web', f'https://www.scopus.com/authid/detail.uri?authorId={auth_id}')
    # finish changing
    main_template.write(main_write)
    main_template.close()
    show_detail.app.run(debug=None)

if __name__=="__main__":
    load_data()
    result = interactive_prompt()

    if result != None:
        show_in_browser(result[0], result[1], result[2])


