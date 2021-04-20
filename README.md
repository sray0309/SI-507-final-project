# si507-final-project

A python project to view faculty information and their academic detail in Computer Science/Engineering field. Now this project only support four schools(University of Michigan; University of California, Berkeley; Massachusetts Institute of Technology; University of Illinois at Urbana-Champaign)

## Before running
  1. secrets.py is submitted through canvas. Please add secrets.py under the same directory as main.py before running.
  2. Required library includes requests, sqlite3, beautifulsoup, json, webbrowser, flask

## Running program
  1. run ```python3 main.py``` in terminal. 
  2. It will take a few minutes to load data if it is the first time running. 
  3. User can see a list of schools after running. User can choose to view detail by typing ```<school number> detail```. Then information like name and location will be shown in the terminal and the browser will open school page and admission page. User can also view all faculty list by running ```<school number> faculty```. Then a long list containing faculties' information will be shown in the terminal.
  4. After seeing the faculty list, user can run ```<faculty number> info``` to see detail about this faculty include full research interests, personal web and email. Or user can run ```<faculty number> detail``` to view more academic detail through a flask app. 100 publications of this faculty will be shown in a page. The faculty name will link to the SCOPUS page of this faculty and the publication name will link to the detail of this publication.
  5. User can exit anytime by running ```exit``` and can also back to viewing school list by running ```back```.
