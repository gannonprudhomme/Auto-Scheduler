# Called to execute the beginning of scaping courses

from django.core.management import base

import requests
import json

# BASE_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject'
BASE_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?dataType=json&searchTerm=&term=201931&offset=1&max=500'

def parse_departments(json):
    """
    Given the JSON of all of the departments, parses them and initializes them into Department objects
    """

    for dept in json:
        # Should have (code, decription)

        print(v)

    return

# Retrieve all of the departments
def get_departments():
    """
    Scrapes the departments and fills the database
    """

    term = '201931' # Get current term from somewhered
    maxCount = 500

    # Call getsubjects
    params = {
        'dataType': 'json',
        'term': term,
        'offset': 0,
        'max': maxCount
    }

    # r = requests.get(BASE_URL, params=params)
    r = requests.get(BASE_URL)

    return r.json()

def scrape_departments():
    json = get_departments()

    parse_departments(json)


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        # Do stuff
        scrape_departments()