import requests
import sqlite3
from bs4 import BeautifulSoup
import json
import time

SCHOOL = 'michigan'

ECE_URL = 'https://ece.engin.umich.edu/people/directory/faculty/'
CSE_URL = 'https://cse.engin.umich.edu/people/faculty/'
headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping'}

time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def check_data():
    try:
        cache_file = open('cache/michigan.json', 'r')
        cache_file_contents = cache_file.read()
        faculty = json.loads(cache_file_contents)
        cache_file.close()
    except:
        faculty = {'cache_time': time_now,'total_number' : 0, 'detail': []}

    if (faculty['cache_time'][:7] != time_now[:7] or faculty['total_number'] == 0):
        print('University of Michigan: Fetching from website...')
        faculty['cache_time'] = time_now
        ece_response = requests.get(ECE_URL, headers=headers)
        cse_response = requests.get(CSE_URL, headers=headers)
        ece_soup = BeautifulSoup(ece_response.text, 'html.parser')
        cse_soup = BeautifulSoup(cse_response.text, 'html.parser')

        # parse ece faculty detail
        for soup in [ece_soup, cse_soup]:
            people_lists_html = soup.find_all('div', class_='eecs_person_copy')
            for person in people_lists_html:
                name = person.find('h4').text.split(', ')
                lastname = name[0]
                firstname = name[1]
                title = person.find('span', class_='person_title_section').text
                try:
                    research_interests = person.find('span', class_='person_copy_section pcs_tall').text
                except:
                    research_interests = None
                try:
                    web = person.find('a', class_='person_web').text
                except:
                    web = None
                email_script = str(person.find('script'))
                email = email_script[email_script.index('one')+7:email_script.index('two')-6] + '@' + email_script[email_script.    index   ('two')    +7:email_script.index('document')-2]

                faculty['total_number'] += 1
                faculty['detail'].append({
                    'firstname': firstname,
                    'lastname': lastname,
                    'title': title,
                    'research_interests': research_interests,
                    'personal_web': web,
                    'email': email
                })

        cache_file = open('cache/michigan.json', 'w')
        cache_content_write = json.dumps(faculty)
        cache_file.write(cache_content_write)
        cache_file.close()

        print('Updating database...')
        connection = sqlite3.connect('faculty.sqlite')
        cursor = connection.cursor()
        delete_old_data = '''
            DELETE FROM faculty
            WHERE faculty.School = "michigan"
        '''
        cursor.execute(delete_old_data)
        connection.commit()
        for data in faculty['detail']:
            update_data = f'''
            INSERT INTO faculty ("FirstName", "LastName", "School", "Title", "ResearchInterests", "PersonalWeb", "Email") VALUES("{data['firstname']}", "{data['lastname']}", "michigan", "{data['title']}", "{data['research_interests']}", "{data['personal_web']}", "{data['email']}")
            '''
            cursor.execute(update_data)
            connection.commit()

    else:
        print('University of Michigan: Using cache')

