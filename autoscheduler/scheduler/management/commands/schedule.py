from django.core.management import base

import json, time, datetime
from pathlib import Path

from scraper.models import Course, Section, Meeting
from typing import List, Dict

def _load_json_file(path: str):
    """ Loads a json file given a path """
    base_path = Path(__file__).parent
    file_path = (base_path / path).resolve()

    data = None
    with open(file_path) as json_file:
        data = json.load(json_file)

        json_file.close()

    return data

def get_all_course_sections(json) -> List[List[Section]]:
    term = json["term"]

    data = []
    for course in json["courses"]:
        subject = course["subject"]
        course_num = course["course_num"]
        sections = course["sections"] # Will become a list of Section models

        if len(sections) == 0: # If they didn't specify any specific sections, get all
            sections = get_sections_for_course(subject, course_num, term)
        else: # Specified specific sections, get the according ones
            new_sections = []
            for crn in sections:
                section = Section.objects.get(subject=subject, course_num = course_num, 
                                                section_num=crn, term_code = term)
                new_sections.append(section)

            # Sections is now a list of sections
            sections = new_sections
        
        data.append(sections)
    
    return data



def get_sections_for_course(subject: str, course_num: int, term: str):
    """ Retrieves all of the sections for a given course """
    sections = Section.objects.filter(subject=subject, course_num=str(course_num), 
                                      term_code=term)

    return sections

schedules = []
def create_schedules(course_sections: List[List[Section]]):
    """ Creates a schedule given a list of section meeting lists """

    # Sort the list by courses that have the least amount of meetings first,
    # to maximize the amount of schedules we make?
    # Pick a meeting from [0] and try to find combinations that fit with the rest?
    def sortByLen(val):
        return len(val)

    meetings = { } # section-id : list of meetings

    # Sort the course_sections by the ones with the least sections first
    course_sections.sort(key = sortByLen, reverse=False)

    for sections in course_sections:
        for section in sections:
            id = section.id
            m = section.meetings.all()

            meetings[id] = m

    do_schedule(course_sections, meetings, [], 0)
    print(f'Generated {len(schedules)} schedules')

    # Iterate through sections and try to find a match

    return schedules

def do_schedule(courses: List[List[Section]], meetings,
                current: List[Section], currCourse: int):
    """ Meetings is a list of [section_id : List[Meeting]] """

    if currCourse == len(courses):
        schedules.append(current)
        print('Start schedule')
        for section in current:
            print(f'{section.subject} {section.course_num}-{section.section_num}')
        print('End schedule\n')
        return

    for section in courses[currCourse]:
        sec_meetings = meetings[section.id]
        curr_meetings = [meetings[sec.id] for sec in current]

        if not _does_intersect_with_current(sec_meetings, curr_meetings):
            new = current + [section]
            do_schedule(courses, meetings, new, currCourse + 1)

def _does_intersect(start1: int, end1: int, start2: int, end2: int):
    """ Returns whether these time ranges intersect. Times are in 24hr time """

    """ Ex: start1: 0910, end1: 1000, start2: 1020, end2: 1110 | Out -> false """
    """ Ex2: start1: 0910, end1: 1000, start2: 0935 end2 1100 | Out -> true """
    """ Ex3: start1: 0900, end1: 0950, start2: 8:35, end2: 1000 | Out -> true """

    if((start1 < start2 and end1 < end2) or (start2 < start1 and end2 < end1)):
        return False

    # Otherwise, they intersect at some point
    return True

def _time_to_int(time: datetime) -> int:
    return int(time.strftime('%H%M')) # Converts a time to the form HHMM, i.e. 0835

def _does_intersect_with_current(sec_meetings: List[Meeting], current: List[List[Meeting]]):
    for meetings in current:
        for sec_meeting in sec_meetings: # Iterate through the meetings sec_meetings has
            for meeting in meetings:
                start1 = _time_to_int(sec_meeting.start_time)
                end1 = _time_to_int(sec_meeting.end_time)
                start2 = _time_to_int(meeting.start_time)
                end2 = _time_to_int(meeting.end_time)

                if _does_intersect(start1, end1, start2, end2):
                    return True

    return False

class Command(base.BaseCommand):
    """ Creates a schedule given courses """
    def handle(self, *args, **options):
        start = time.time()

        json_data = _load_json_file("../commands/input.json")

        data = get_all_course_sections(json_data)

        schedules = create_schedules(data)

        # Calculate time to complete
        end = time.time()
        seconds_elapased = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapased)
        print(f"Finished in {time_delta}")

