import requests
import sqlite3
from bs4 import BeautifulSoup
import json
import time

SCHOOL = 'illinois'

url = 'https://cs.illinois.edu/about/people/all-faculty'
headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping'}
time_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))

def check_data():
    try:
        cache_file = open('cache/illinois.json', 'r')
        cache_file_contents = cache_file.read()
        faculty = json.loads(cache_file_contents)
        cache_file.close()
    except:
        faculty = {'cache_time': time_now,'total_number' : 0, 'detail': []}

    if (faculty['cache_time'][:7] != time_now[:7] or faculty['total_number'] == 0):
        print('University of Illinois at Urbana-Champaign: Fetching from website...')
        faculty['cache_time'] = time_now
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        faculty_list = soup.find('div', class_='directory-list directory-list-4').find_all('div', recursive=False)
        for faculty_soup in faculty_list:
            name_list = faculty_soup.find('div', class_='name').text.split(' ')
            lastname = name_list[-1]
            firstname = ''
            for i in name_list[:-1]:
                firstname = firstname + ' ' + i
                firstname = firstname.strip()
            title = faculty_soup.find('div', class_='title').text.strip()
            web = 'https://cs.illinois.edu' + faculty_soup.find('div', class_='name').find('a')['href']
            email = faculty_soup.find('div', class_='email').find('a')['href'][7:]
            research_response = requests.get(web, headers=headers)
            research_soup = str(research_response.text)
            if ('Interests' in research_soup):
                research_soup = research_soup.split('Interests</h2>')[-1]
                research_soup = research_soup.split('</ul>')[0].strip()
                research_interests = research_soup.replace('<li>','').replace('<ul>','').replace('</li>','').replace('"','').replace('\n','').replace('\r','')
            else:
                research_interests = 'see personal web'

            faculty['total_number'] += 1

            faculty['detail'].append({
                'firstname': firstname,
                'lastname': lastname,
                'title': title,
                'research_interests': research_interests,
                'personal_web': web,
                'email': email
            })

        cache_file = open('cache/illinois.json', 'w')
        cache_content_write = json.dumps(faculty)
        cache_file.write(cache_content_write)
        cache_file.close()
        

        print('Updating database...')
        connection = sqlite3.connect('faculty.sqlite')
        cursor = connection.cursor()
        delete_old_data = '''
            DELETE FROM faculty
            WHERE SchoolId in (SELECT Id from school WHERE name = "illinois")'''
        cursor.execute(delete_old_data)
        connection.commit()
        for data in faculty['detail']:
            update_data = f'''
            INSERT INTO faculty ("FirstName", "LastName", "SchoolId", "Title", "ResearchInterests", "PersonalWeb", "Email") VALUES("{data['firstname']}", "{data['lastname']}", 4, "{data['title']}", "{data['research_interests']}", "{data['personal_web']}", "{data['email']}")
            '''
            cursor.execute(update_data)
            connection.commit()

    else:
        print('University of Illinois at Urbana-Champaign: Using cache')