import requests
import sqlite3
from bs4 import BeautifulSoup
import json
import time

SCHOOL = 'mit'

url = 'https://www.eecs.mit.edu/people/faculty-advisors'
headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping'}
time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def check_data():
    try:
        cache_file = open('cache/mit.json', 'r')
        cache_file_contents = cache_file.read()
        faculty = json.loads(cache_file_contents)
        cache_file.close()
    except:
        faculty = {'cache_time': time_now,'total_number' : 0, 'detail': []}

    if (faculty['cache_time'][:7] != time_now[:7] or faculty['total_number'] == 0):
        print('Massachusetts Institute of Technology: Fetching from website...')
        faculty['cache_time'] = time_now
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        faculty_list = soup.find('div', class_='people-list').find_all('li')
        for faculty_soup in faculty_list:
            try:
                raw_name_list = faculty_soup.find('span', class_='field-content card-title').find('a').text.strip().split(' ')
            except:
                raw_name_list = faculty_soup.find('span', class_='field-content card-title').text.strip().split(' ')
            if len(raw_name_list) == 1:
                name_list[0] = raw_name_list[0]
                name_list[1] = None
            elif len(raw_name_list) == 3:
                name_list[0] = raw_name_list[0] + raw_name_list[1]
                name_list[1] = raw_name_list[2] 
            elif len(raw_name_list) == 4:
                name_list[0] = raw_name_list[0] + raw_name_list[1]
                name_list[1] = raw_name_list[2] + raw_name_list[3]
            else:
                name_list = raw_name_list
            firstname = name_list[0]
            lastname = name_list[1]
            title = faculty_soup.find('div', class_='views-field views-field-field-person-title').find('div', class_='field-content').text.strip()
            research_interests = faculty_soup.find('div', class_='views-field views-field-term-node-tid').find('span', class_='field-content').text.strip()
            try:
                web = faculty_soup.find('span', class_='field-content card-title').find('a')['href']
            except:
                web = None
            email = faculty_soup.find('div', class_='views-field views-field-field-person-email').find('div', class_='field-content').text.strip()

            faculty['total_number'] += 1

            faculty['detail'].append({
                'firstname': firstname,
                'lastname': lastname,
                'title': title,
                'research_interests': research_interests,
                'personal_web': web,
                'email': email
            })

        cache_file = open('cache/mit.json', 'w')
        cache_content_write = json.dumps(faculty)
        cache_file.write(cache_content_write)
        cache_file.close()
        

        print('Updating database...')
        connection = sqlite3.connect('faculty.sqlite')
        cursor = connection.cursor()
        delete_old_data = '''
            DELETE FROM faculty
            WHERE faculty.School = "mit"
        '''
        cursor.execute(delete_old_data)
        connection.commit()
        for data in faculty['detail']:
            update_data = f'''
            INSERT INTO faculty ("FirstName", "LastName", "School", "Title", "ResearchInterests", "PersonalWeb", "Email") VALUES("{data['firstname']}", "{data['lastname']}", "mit", "{data['title']}", "{data['research_interests']}", "{data['personal_web']}", "{data['email']}")
            '''
            cursor.execute(update_data)
            connection.commit()

    else:
        print('Massachusetts Institute of Technology: Using cache')
