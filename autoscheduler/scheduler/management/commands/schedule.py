import datetime
import json
import time
from pathlib import Path
from typing import Dict, List

from django.core.management import base

from scraper.models import Course, Meeting, Section


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
    total = 1
    for course in json["courses"]:
        subject = course["subject"]
        course_num = course["course_num"]
        sections = course["sections"] # Will become a list of Section models

        # Remove sections with current seats == max seats(no empty seats)
        # Remove sections where meetings aren't within start & end times
        # Sort sections by ones with priorities first?

        if len(sections) == 0: # If they didn't specify any specific sections, get all
            sections = get_sections_for_course(subject, course_num, term)
            print(len(sections))
            total = total * len(sections)
        else: # Specified specific sections, get the according ones
            new_sections = []
            total = total * len(sections)
            for crn in sections:
                section = Section.objects.get(subject=subject, course_num = course_num, 
                                                section_num=crn, term_code = term)
                new_sections.append(section)

            # Sections is now a list of sections
            sections = new_sections
            print(len(sections))
        
        data.append(sections)

    print(f'There are {total} possible combinations')
    return data

def get_sections_for_course(subject: str, course_num: int, term: str):
    """ Retrieves all of the sections for a given course """
    sections = Section.objects.filter(subject=subject, course_num=str(course_num), 
                                      term_code=term)

    return sections

schedules = []
def create_schedules(course_sections: List[List[Section]], start: int, end: int):
    """ Creates a schedule given a list of section meeting lists """

    # Sort the list by courses that have the least amount of meetings first,
    # to maximize the amount of schedules we make?
    # Pick a meeting from [0] and try to find combinations that fit with the rest?
    def sortByLen(val):
        return len(val)

    meetings = { } # section-id : list of meetings

    # Sort the course_sections by the ones with the least sections first
    course_sections.sort(key = sortByLen, reverse=False)

    print('getting all meetings')
    start = time.time()

    filtered_course_sections = [] # List[List[Section]]

    for sections in course_sections:
        filtered_sections = []

        # While retrieving the meetings, only add the sections whose meetings meet our
        # criteria
        for section in sections:
            # Remove meetings without a time as no need to compare(will always work)
                # If they end up with no meetings, then don't add them at all

            meetings_set = section.meetings.all()

            # Remove sections whose meetings aren't within start & end times
            count = 0
            should_add = True
            for m in meetings_set:
                # Check if start time is not null
                if not m.start_time == None:
                    # Needs better names 
                    start_time = _time_to_int(m.start_time) 
                    end_time = _time_to_int(m.end_time)

                    if _does_intersect(start, end, start_time, end_time):
                        should_add = False
                        break # One meeting time intersecting invalidates the whole section

            if should_add:
                filtered_sections.append(section)
                meetings[section.id] = meetings_set
        
        filtered_course_sections.append(filtered_sections)
    
    end = time.time()
    delta = datetime.timedelta(seconds=int(end - start))
    print(f'got all meetings in {delta}')

    do_schedule(filtered_course_sections, meetings, [], 0)
    print(f'Generated {len(schedules)} schedules')

    # Iterate through sections and try to find a match

    return schedules

def do_schedule(courses: List[List[Section]], meetings,
                current: List[Section], currCourse: int):
    """ Meetings is a list of [section_id : List[Meeting]] """

    if currCourse == len(courses):
        schedules.append(current)
        return

    for section in courses[currCourse]:
        sec_meetings = meetings[section.id]
        curr_meetings = [meetings[sec.id] for sec in current]
        # print(f'{section.subject} {section.course_num}-{section.section_num}')

        if not _does_intersect_with_current(sec_meetings, curr_meetings):
            new = current + [section]
            do_schedule(courses, meetings, new, currCourse + 1)

def _does_intersect(start1: int, end1: int, start2: int, end2: int):
    """ Returns whether these time ranges intersect. Times are in 24hr time """

    """ Ex: start1: 0910, end1: 1000, start2: 1020, end2: 1110 | Out -> false """
    """ Ex2: start1: 0910, end1: 1000, start2: 0935 end2 1100 | Out -> true """
    """ Ex3: start1: 0900, end1: 0950, start2: 8:35, end2: 1000 | Out -> true """

    condition = max(start1, start2) < min(end1, end2)
    # print(f'{start1} {end1} to {start2} {end2} {condition}')

    return condition

def _time_to_int(time: datetime) -> int:
    return int(time.strftime('%H%M')) # Converts a time to the form HHMM, i.e. 0835

def _does_intersect_with_current(sec_meetings: List[Meeting], current: List[List[Meeting]]):
    for meetings in current:
        for sec_meeting in sec_meetings: # Iterate through the meetings sec_meetings has
            start1 = sec_meeting.start_time
            end1 = sec_meeting.end_time

            if start1 == None or end1 == None:
                continue

            start1 = _time_to_int(sec_meeting.start_time)
            end1 = _time_to_int(sec_meeting.end_time)

            sec_days = sec_meeting.meeting_days

            for meeting in meetings:
                start2 = meeting.start_time
                end2 = meeting.end_time

                days = meeting.meeting_days

                if start2 == None or end2 == None:
                    continue

                # Make sure the days don't overlap
                # If none of the days overlap, we don't need to compare them
                if days.find(sec_days) == -1 and sec_days.find(days) == -1:
                    # print(f'continuing b/c {days} {sec_days}')
                    continue


                start2 = _time_to_int(meeting.start_time)
                end2 = _time_to_int(meeting.end_time)

                if _does_intersect(start1, end1, start2, end2):
                    return True

    return False

class Command(base.BaseCommand):
    """ Creates a schedule given courses """
    def handle(self, *args, **options):
        start = time.time()

        json_data = _load_json_file("../commands/input2.json")

        time_ranges = json_data["timeRanges"]
        start_time = int(time_ranges[0]["start"])
        end_time = int(time_ranges[0]["end"])

        data = get_all_course_sections(json_data)

        schedules = create_schedules(data, start_time, end_time)

        # Calculate time to complete
        end = time.time()
        seconds_elapased = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapased)
        print(f"Finished in {time_delta}")
