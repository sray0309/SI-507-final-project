import schools.school, schools.michigan, schools.berkeley, schools.mit, schools.illinois
import requests
import sqlite3
from bs4 import BeautifulSoup
import show_detail
import scopus
import json
import webbrowser

SCHOOL_LIST = ['University of Michigan', 'University of California, Berkeley', 'Massachusetts Institute of Technology', 'University of Illinois at Urbana-Champaign']
SCHOOL_DICT = {
    'University of Michigan': 'michigan',
    'University of California, Berkeley': 'berkeley',
    'Massachusetts Institute of Technology': 'mit',
    'University of Illinois at Urbana-Champaign': 'illinois'}

def load_data():
    schools.school.create_school_table()
    connection = sqlite3.connect('faculty.sqlite')
    cursor = connection.cursor()
    create_table = '''
        CREATE TABLE IF NOT EXISTS "faculty" (
            "Id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "SchoolId" INTEGER,
            "FirstName" TEXT NOT NULL,
            "LastName" TEXT NOT NULL,
            "Title"  TEXT NOT NULL,
            "ResearchInterests"   TEXT,
            "PersonalWeb"    TEXT,
            "Email" TEXT,
            FOREIGN KEY(SchoolId) REFERENCES school(Id));'''
    cursor.execute(create_table)
    connection.commit()
    print('########## Loading data... ##########')
    schools.michigan.check_data()
    schools.berkeley.check_data()
    schools.mit.check_data()
    schools.illinois.check_data()
    print('########## Finish loading ##########')

def retrieve_data_from_database(school):
    connection = sqlite3.connect('faculty.sqlite')
    cursor = connection.cursor()
    query = f'''
    SELECT faculty.FirstName, faculty.LastName, faculty.Title, faculty.ResearchInterests, faculty.PersonalWeb, faculty.email from faculty
    JOIN school
    ON faculty.SchoolId = school.ID
    WHERE school.Name = '{school}'
    ORDER BY faculty.FirstName, faculty.LastName
    '''
    results = cursor.execute(query).fetchall()
    return results

def retrieve_school_from_database(school):
    connection = sqlite3.connect('faculty.sqlite')
    cursor = connection.cursor()
    query = f'''
    SELECT school.Name, school.City, school.State, school.MainWeb, school.Admission from school
    WHERE school.Name = '{school}'
    '''
    results = cursor.execute(query).fetchall()
    return results

def interactive_prompt():
    while True:
        print('')
        print('School List Results:')
        print('-'*58)
        for i in range(len(SCHOOL_LIST)):
            print('|', i+1,'|',SCHOOL_LIST[i].ljust(50),'|')
        print('-'*58)
        print('''
################################################################################################################
#### enter a school number with option to check details                                                     ####
#### options:                                                                                               ####
####     <faculty>: show faculty list of this school, with name and research interest                       ####
####     <detail>: show detail of this school(location) and open shool website and admission website        ####
#### examples:                                                                                              ####
####     1 faculty                                                                                          #### 
####     3 detail                                                                                           ####
################################################################################################################
        ''')
        user_input = input('please choose a school number with option or exit: \n')
        if user_input == 'exit':
            break
        if len(user_input.split(' ')) != 2:
            print('please enter a number with option')
            continue
        input_list = user_input.split(' ')
        if not input_list[0].isnumeric():
            print('please input a number')
            continue
        if int(input_list[0])-1 not in range(len(SCHOOL_LIST)):
            print('Missing data, please choose from the list below')
            continue
        if input_list[1] not in ['faculty', 'detail']:
            print('please choose a correct option')
            continue
        school = SCHOOL_DICT[SCHOOL_LIST[int(input_list[0])-1]]
        if input_list[1] == 'detail':
            results = retrieve_school_from_database(school)[0]
            print('')
            print('School Detail Results:')
            print('  [school name]:', results[0].strip())
            print('  [location:city]:', results[1].strip())
            print('  [location:state]:', results[2].strip())
            print('')
            webbrowser.open(results[3], new=2)
            webbrowser.open(results[4], new=2)
            continue
        elif input_list[1] == 'faculty':
            results = retrieve_data_from_database(school)
            print('')
            print('Faculty Results:')
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
#### enter a faculty number with option to check details                                                    ####
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
                    elif command[1] not in ['info', 'detail']:
                        print('please choose a correct option')
                        continue
                    elif command[1] == 'info':
                        print('')
                        print('Faculty Information Results:')
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

def change_html(auth_id, firstname, lastname):
    main_default = open('templates/main_template.html', 'r')
    main_template = open('templates/main.html', 'w')
    main_read = main_default.read()
    main_default.close()
    # change template content
    if auth_id != None:
        main_write = main_read.replace('name', f'{firstname} {lastname}')
        main_write = main_write.replace('scopus_web', f'https://www.scopus.com/authid/detail.uri?authorId={auth_id}')
    else:
        main_write = main_read.replace('name', 'cannot find this faculty on scopus')
        main_write = main_write.replace('scopus_web', '#')
    # finish changing
    main_template.write(main_write)
    main_template.close()

if __name__=="__main__":
    load_data()
    result = interactive_prompt()

    if result != None:
        auth_id = scopus.find_id(result[0], result[1], result[2])
        change_html(auth_id, result[0], result[1])
        publications = {
            'data': scopus.retrieve_auth_detail(auth_id)
            }
        pub_file = open('publications.json', 'w')
        content = json.dumps(publications)
        pub_file.write(content)
        pub_file.close()
        show_detail.app.run(debug=True, use_reloader=False)


