import sqlite3

SCHOOL_TABLE = [{
    'name': 'michigan',
    'city': 'ann arbor',
    'state': 'MI',
    'mainweb': 'https://eecs.engin.umich.edu/',
    'admission': 'https://rackham.umich.edu/programs-of-study/'
},{
    'name': 'berkeley',
    'city': 'berkeley',
    'state': 'CA',
    'mainweb': 'https://eecs.berkeley.edu/',
    'admission': 'https://grad.berkeley.edu/admissions/apply/'
},{
    'name': 'mit',
    'city': 'cambridge',
    'state': 'MA',
    'mainweb': 'https://www.eecs.mit.edu/',
    'admission': 'https://gradadmissions.mit.edu/'
},{
    'name': 'illinois',
    'city': 'Champaign',
    'state': 'IL',
    'mainweb': 'https://cs.illinois.edu/',
    'admission': 'https://cs.illinois.edu/admissions/graduate/degree-program-options'
}]

def create_school_table():
    try:
        open('cache/michigan.json', 'r')
        initial = False
    except:
        initial = True
    if initial:
        create_school_table = '''
            CREATE TABLE IF NOT EXISTS "school" (
                "Id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "Name"    TEXT NOT NULL,
                "City" TEXT NOT NULL,
                "State" TEXT NOT NULL,
                "MainWeb"  TEXT NOT NULL,
                "Admission"   TEXT NOT NULL);'''
        connection = sqlite3.connect('faculty.sqlite')
        cursor = connection.cursor()
        cursor.execute(create_school_table)
        connection.commit()
        for school in SCHOOL_TABLE:
            query = f'''
            INSERT INTO school ("Name", "City", "State", "MainWeb", "Admission") VALUES("{school['name']}","{school['city']}", "    {school['state']}", "{school['mainweb']}", "{school['admission']}")'''
            cursor.execute(query)
            connection.commit()
    