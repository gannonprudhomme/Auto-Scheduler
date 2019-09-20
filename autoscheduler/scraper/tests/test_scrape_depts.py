from django.test import TestCase
import requests
import requests_mock

from scraper.management.commands import scrape_depts

class ScrapeDepsTestCase(TestCase):
    def setUp(self):

    def parse_departments__emptyInput_doesThrowError(self):
        """Should throw an error if the json input is empty"""
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)

        with requests_mock.mock() as m:
            m.get(scrape_depts.BASE_URL, text='')

        actual = scrape_depts.get_departments()
        self.assertEqual('', actual)