import requests
import sqlite3
from bs4 import BeautifulSoup
import json
import time

SCHOOL = 'berkeley'

base_url = 'https://www2.eecs.berkeley.edu/'
url = 'https://www2.eecs.berkeley.edu/Faculty/Lists/faculty.html'
headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping'}

time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def check_data():
    try:
        cache_file = open('cache/berkeley.json', 'r')
        cache_file_contents = cache_file.read()
        faculty = json.loads(cache_file_contents)
        cache_file.close()
    except:
        faculty = {'cache_time': time_now,'total_number' : 0, 'detail': []}

    if (faculty['cache_time'][:7] != time_now[:7] or faculty['total_number'] == 0):
        print('University of California, Berkeley: Fetching from website...')
        faculty['cache_time'] = time_now
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        faculty_list = soup.find_all('div', class_='media')
        for faculty_soup in faculty_list:
            name = faculty_soup.find('h3').find('a').text
            if ('.' in name):
                name_list = name.split('. ')
                firstname = name_list[0] + '.'
            else:
                name_list = name.split(' ')
                firstname = name_list[0]
            lastname = name_list[1]
            title = faculty_soup.find('p').find('strong').text
            research_list = faculty_soup.find('p').find_all('a')
            research_interests = ''
            for research in research_list:
                if (research['href'][1:9] == 'Research'):
                    research_interests += research.text + ' '
            web = base_url + faculty_soup.find('h3').find('a')['href']
            email_response = requests.get(web, headers=headers)
            email_soup = BeautifulSoup(email_response.text, 'html.parser')
            try:
                email = email_soup.find('div', class_='email').text.strip()
            except:
                email = None
            
            faculty['total_number'] += 1
            faculty['detail'].append({
                'firstname': firstname,
                'lastname': lastname,
                'title': title,
                'research_interests': research_interests,
                'personal_web': web,
                'email': email
            })

        cache_file = open('cache/berkeley.json', 'w')
        cache_content_write = json.dumps(faculty)
        cache_file.write(cache_content_write)
        cache_file.close()

        print('Updating database...')
        connection = sqlite3.connect('faculty.sqlite')
        cursor = connection.cursor()
        delete_old_data = '''
            DELETE FROM faculty
            WHERE SchoolId in (SELECT Id from school WHERE name = "berkeley")'''
        cursor.execute(delete_old_data)
        connection.commit()
        for data in faculty['detail']:
            update_data = f'''
            INSERT INTO faculty ("FirstName", "LastName", "SchoolId", "Title", "ResearchInterests", "PersonalWeb", "Email") VALUES("{data['firstname']}", "{data['lastname']}", 2, "{data['title']}", "{data['research_interests']}", "{data['personal_web']}", "{data['email']}")
            '''
            cursor.execute(update_data)
            connection.commit()

    else:
        print('University of California, Berkeley: Using cache')
