from django.core.management import base

from http.cookiejar import CookieJar

import requests, json
import time, datetime

# This might need to scrape sections as well, since they're given together
# Everytime we load in a section, check if the course is in the database? Or just save it anyways?
# Will probably save us time if we don't attempt ot save it every time - use a hashset with courses #'s in this case

BASE_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults'
BASE_URL_PARAMS = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subject=CSCE&txt_term=201931&startDatepicker=&endDatepicker=&uniqueSessionId=scf271568699904823&pageOffset=0&pageMaxSize=50&sortColumn=subjectDescription&sortDirection=asc&[object%20Object]'
TERMS_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?uniqueSessionId=hq0xu1569180038532&dataType=json&searchTerm=&offset=1&max=10&_=1569181435047'
#txt_subject=CSCE&txt_courseNumber=312&txt_term=201931&startDatepicker=&endDatepicker=&uniqueSessionId=scf271568699904823
# &pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc&[object%20Object]'

params = {
    'txt_subject': 'CSCE',
    'txt_term': '201931',
    'pageOffset': 0,
    'pageMaxSize': 500,
    'sortColumn': 'subjectDescription',
    'sortDirection': 'asc',
}

def update_cookies(session):
    cookie_to_add = { 'JSESSIONID': 'cookie' }

    session.cookies.set('JSESSIONID', 'cookie', domain='compassxe-ssb.tamu.edu')
    cookies = session.cookies
    # session.cookies.update(cookie_to_add)

    return session

def generate_session():
    """ Goes to the correct places to generate a valid JSESSIONID cookie that we need to search for courses """
    session = requests.Session()
    session.get('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/registration/registration')
    session.get('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/classSearch')
    data = session.post('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=search')
    terms = session.get(TERMS_URL)

    # session = update_cookies(session)

    print(session.cookies) # Doesn't have any cookies until we do the GET
    print()

    return session

def scrape_courses():
    # Somehow create a session id
    session = generate_session()
    data = session.get(BASE_URL_PARAMS)

    json = ''
    try:
        json = data.json()
    except:
        print('Error: scrape_courses could not get json')
    
    # print(json['data'])
    print(f"totalCount: {json['totalCount']}")
    return json

def parse_courses(json):
    # Stuff
    print(json)

def parse_section(json):
    """ Given a single section data, parses it and returns a course, section tuple? """
    print(json)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        start = time.time()
        scrape_courses()
        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        # print(f"Finished scraping courses in {time_delta}")
