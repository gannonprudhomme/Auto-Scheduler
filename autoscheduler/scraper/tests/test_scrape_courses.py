from django.test import TestCase

import json
from pathlib import Path

from scraper.management.commands import scrape_courses
from scraper.models import Course, Section, Meeting
from datetime import time

class ScrapeCoursesTestCase(TestCase):
    section_input = {}

    def setUp(self):
        base_path = Path(__file__).parent
        file_path = (base_path / ".../section_inputs.json").resolve()

        # Load in the section input test data
        with open(file_path) as json_file:
            data = json.load(json_file)
            self.section_input = data['section_test']
            
            json_file.close()

    def test__get_courses__normalInput__formsCorrectly(self):
        pass

    def test__parse_section__normalInput__formsCorrectly(self):
        """ Given a normal section/course input, does it format correctly? """
        expected = Section(
            id = "10915-201931",
            
            instructor="T00918203"
        )

        scrape_courses.parse_section({ }, "10915")

    def test__parse_meeting__normalInput__formsCorrectly(self):
        """ Given a normal section meeting input, ensure it formats correctly """
        expected = Meeting(
            id = "CSCE110-501-0",
            crn = "10915",
            building = "ZACH",
            meeting_days = "TR",
            start_time = time(12, 45, 0),
            end_time = time(14, 0, 0),
            meeting_type = "LEC"
        )

        actual = scrape_courses.parse_meeting(self.section_input['meetingsFaculty'][0]['meetingTime'], 'CSCE110-501')
        print(expected.crn)
        print(actual.crn)

        self.assertEqual(expected, actual)

    def test__parse_meeting_days__normalInput__formsCorrectly(self):
        """ Given a normal section meeting input, ensure it formats the days correctly """
        expected = "TR"
        actual = scrape_courses.parse_meeting_days(self.section_input['meetingsFaculty'][0]['meetingTime'])

        self.assertEqual(expected, actual)

    def test__parse_time__normalInput__formsCorrectly(self):
        expected = time(12, 45, 0)
        actual = scrape_courses.parse_time("1245")

        self.assertEqual(expected, actual)