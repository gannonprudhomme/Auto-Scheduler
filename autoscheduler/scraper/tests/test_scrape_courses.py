from django.test import TestCase

import json
from pathlib import Path

from 

class ScrapeCoursesTestCase(TestCase):
    section_input = {}

    def setUp(self):
        base_path = Path(__file__).parent
        file_path = (base_path / ".../section_inputs.json").resolve()

        # Load in the section input
        with open(file_path) as json_file:
            data = json.load(json_file)
            section_input = data['section_test']
            
            json_file.close()

    def test_parse_section__normalInput__formsCorrectly(self):
        """ Given a normal section/course input, does it format correctly? """
        # expected = Section

