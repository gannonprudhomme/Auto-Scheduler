from django.core.management import base

from http.cookiejar import CookieJar

from scraper.models.course import Course
from scraper.models.section import Section, Meeting
from scraper.models.instructor import Instructor
from scraper.models.department import Department

from scraper.banner_requests import BannerRequests

import requests, json
import time, datetime
import asyncio

from pathlib import Path # Temporary

# This might need to scrape sections as well, since they're given together
# Everytime we load in a section, check if the course is in the database? Or just save it anyways?
# Will probably save us time if we don't attempt ot save it every time - use a hashset with courses #'s in this case

BASE_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults'
BASE_URL_PARAMS = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subject=CSCE&txt_term=201931&startDatepicker=&endDatepicker=&uniqueSessionId=scf271568699904823&pageOffset=0&pageMaxSize=50&sortColumn=subjectDescription&sortDirection=asc&[object%20Object]'
TERMS_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?uniqueSessionId=hq0xu1569180038532&dataType=json&searchTerm=&offset=1&max=10&_=1569181435047'
DESCRIPTION_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/getCourseDescription'
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
loaded_instructors = set() # Contains their "bannerId"

# Temporary, until I can get the courses actually scraped

def get_faked_section():
    base_path = Path(__file__).parent
    file_path = (base_path / "../../tests/section_inputs.json").resolve()
    data = ''

    with open(file_path) as json_file:
        data = json.load(json_file)

        json_file.close()

    return data

def get_courses(banner_requests, department):
    if(department == 'TAMU'):
        return


    print("Retrieving for department " + department)
    data = banner_requests.get_courses(department)

    return data

# Rename to retrieve_courses?
def get_course_descriptions(term, crn):
    "Given the term code & a crn, returns the course description for the class"
    pass

def parse_course_list(json):
    count = 0
    if(json == None):
        print('Json is none for some reason')
        return

    for section in json:
        subject_and_course = parse_course(section)
        parse_section(section, subject_and_course)
        count = count + 1

    print(f'Scraped {len(loaded_courses)} courses, {count} sections, and {len(loaded_instructors)} instructors')
    loaded_courses.clear()
    loaded_instructors.clear()

def parse_course(json):
    # print(json)
    # print(json)
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

    for faculty in json['faculty']:
        instructor_id = faculty['bannerId']
        if instructor_id not in loaded_instructors:
            parse_instructor(faculty)

            loaded_instructors.add(instructor_id)

    course_num = json['courseNumber']
    # Only save it to the database if it hasn't been loaded yet? Or does it not matter
    if course_num not in loaded_courses:
        course.save()

        # Add this course to the
        loaded_courses.add(course_num)

    return subject_and_course

# TODO: Complete this
def parse_section(json, course):
    """ Given a single section data, parses it and returns a course, section tuple? """

    instructor = ""
    if(len(json["faculty"]) > 0):
        instructor=json["faculty"][0]["bannerId"]

    crn = json["courseReferenceNumber"]
    section = Section( # Not sure what else I want to have in here
        id = f"{crn}-{json['term']}",
        subject = json["subject"], # Not sure if we need this
        section_num = json["sequenceNumber"],
        course_num = json["courseNumber"],
        term_code = json["term"],

        min_credits = json["creditHourLow"],
        max_credits = json["creditHourHigh"],

        max_enrollment = json["maximumEnrollment"],
        current_enrolled = json["enrollment"],

        instructor=instructor, # I assume this is their ID?
    )

    section.save()

    meetings = json['meetingsFaculty']
    count = 0
    for meeting_data in meetings:
        meeting = parse_meeting(meeting_data, section.id, count)
        meeting.save()
        section.meetings.add(meeting)
        # Need to connect the meetings to the courses somehow
        count = count + 1

    section.save()
    # print(f'Scrapped {count} meetings ')

# TODO: Rename json
def parse_meeting(json, section_id, count):
    """ Given a single meeting dict, parses it... and returns a Meeting object"""

    begin_time = json['meetingTime']['beginTime']
    end_time = json['meetingTime']['beginTime']
    if(begin_time != None):
        begin_time = parse_time(begin_time)
        end_time = parse_time(end_time)
    

    # Probably would need error catching in here to make sure it's formed correctly?
    meeting = Meeting(
        id = section_id + "-" + str(count), # Could just use the CRN
        crn = json["courseReferenceNumber"],
        building = json['meetingTime']['building'], # Can be null
        meeting_days = parse_meeting_days(json['meetingTime']),
        start_time = begin_time,
        end_time = end_time,
        meeting_type = json['meetingTime']['meetingType']
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

def parse_instructor(faculty_data):
    instructor = Instructor(
        id = faculty_data['bannerId'],
        name = faculty_data['displayName'],
        email = faculty_data['emailAddress'],
        pidm = faculty_data['instructorPidm'],
    )

    instructor.save()

class Command(base.BaseCommand):
    def handle(self, *args, **options):
        start = time.time()

        banner = BannerRequests('compassxe-ssb.tamu.edu', '201931')
        banner.create_session()

        models = Department.objects.all()
        for object in models:
            data = get_courses(banner, object.code)
            parse_course_list(data)

        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        print(f"Finished scraping courses in {time_delta}")
