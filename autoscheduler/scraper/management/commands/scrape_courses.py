from django.core.management import base

from http.cookiejar import CookieJar

from scraper.models.course import Course
from scraper.models.section import Section, Meeting

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
    id = json['id']
    crn = json['courseReferenceNumber]']
    subject = json['subject']
    course_num = json['courseNumber']
    title = json['courseTitle']

    maxSeats = json['maximumEnrollment']
    seatsAvailable = json['seatsAvailable']
    # Get wait info?
    # Get credit hour stuff? - probs
    subject_and_course = json['subjectCourse']

    faculty = json['faculty'] # Send to parse_instructor or whatever

    meetings = json['meetingsFaculty']
    for meeting in meetings:
        m = parse_meeting(meeting)
        m.save()

def parse_section(json, course):
    """ Given a single section data, parses it and returns a course, section tuple? """
    print(json)

# TODO: Rename json
def parse_meeting(json, section_id):
    """ Given a single meeting dict, parses it... and returns a Meeting object"""

    # Probably would need error catching in here to make sure it's formed correctly?
    count = 0
    meeting = Meeting(
        id = section_id + "-" + str(count), # Could just use the CRN
        crn = json["courseReferenceNumber"],
        building = json["building"],
        meeting_days = parse_meeting_days(json),
        start_time = parse_time(json["beginTime"]),
        end_time = parse_time(json["endTime"]),
        meeting_type = json["meetingType"]
    )

    return meeting

def parse_meeting_days(json):
    meeting_days = ""

    meeting_days = meeting_days + ('M' if json['monday'] else '')
    meeting_days = meeting_days + ('T' if json['tuesday'] else '')
    meeting_days = meeting_days + ('W' if json['wednesday'] else '')
    meeting_days = meeting_days + ('R' if json['thursday'] else '')
    meeting_days = meeting_days + ('F' if json['friday'] else '')
    meeting_days = meeting_days + ('S' if json['saturday'] else '')
    meeting_days = meeting_days + ('U' if json['sunday'] else '')

    return meeting_days

def parse_time(time_str):
   hr = int(time_str[0:2])
   m = int(time_str[2:5])

   return datetime.time(hr, m, 0)

class Command(base.BaseCommand):
    def handle(self, *args, **options):
        start = time.time()
        scrape_courses()
        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        # print(f"Finished scraping courses in {time_delta}")
