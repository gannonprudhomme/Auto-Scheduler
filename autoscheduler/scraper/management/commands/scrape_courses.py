from django.core.management import base

from http.cookiejar import CookieJar

from scraper.models.course import Course
from scraper.models.section import Section, Meeting

import requests, json
import time, datetime

from pathlib import Path # Temporary

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

loaded_courses = set()

def generate_session():
    """ Goes to the correct places to generate a valid JSESSIONID cookie that we need to search for courses """
    session = requests.Session()
    session.get('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/registration/registration')
    session.get('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/classSearch')
    data = session.post('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=search')
    terms = session.get(TERMS_URL)

    return session

# Temporary, until I can get the courses actually scraped
def get_faked_courses():
    base_path = Path(__file__).parent
    file_path = (base_path / "../../tests/course_inputs.json").resolve()
    data = ''

    with open(file_path) as json_file:
        data = json.load(json_file)

        json_file.close()

    return data

# Rename to retrieve_courses?
def get_courses():
    # Somehow create a session id
    # session = generate_session()
    # data = session.get(BASE_URL_PARAMS)
    data = get_faked_courses()
    print(data)

    try:
        json = data.json()
        return json
        # print(f"totalCount: {json["totalCount"]}")
    except:
        print('Error: scrape_courses could not get json')

    return dict()
    

def parse_course_list(json):
    for section in json["data"]:
        subject_and_course = parse_course(section)
        parse_section(section, subject_and_course)

def parse_course(json):
    course = Course(
        id = json['id'],
        dept = json['subject'],
        course_num = json['courseNumber'],
        title = json['courseTitle'],
        # crn = json['courseReferenceNumber]'],
    )

    maxSeats = json['maximumEnrollment']
    seatsAvailable = json['seatsAvailable']
    # Get wait list info?
    # Get credit hour stuff? - probs
    subject_and_course = json['subjectCourse'] # i.e. CSCE221

    faculty = json['faculty'] # Send to parse_instructor or whatever

    # Only save it to the database if it hasn't been loaded yet? Or does it not matter
    if course_num not in loaded_courses:
        course.save()

        # Add this course to the
        loaded_courses.add(course_num)

    return subject_and_course

# TODO: Complete this
def parse_section(json, course):
    """ Given a single section data, parses it and returns a course, section tuple? """

    crn = json["courseReferenceNumber"]
    section = Section( # Not sure what else I want to have in here
        id=f"{crn}-{json['term']}",
        crn=crn,
        subject=json["subject"], # Not sure if we need this
        instructor=json["faculty"]["bannerId"], # I assume this is their ID?
    )

    meetings = json['meetingsFaculty']
    for meeting_data in meetings:
        meeting = parse_meeting(meeting_json)
        meeting.save()
        section.meetings.add(meeting)
        # Need to connect the meetings to the courses somehow

    section.save()

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

        data = get_courses()
        parse_course_list(data)

        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        # print(f"Finished scraping courses in {time_delta}")
