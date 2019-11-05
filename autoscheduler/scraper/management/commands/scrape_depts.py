# Called to execute the beginning of scaping courses

from django.core.management import base
from scraper.models import Department

import requests
import json
import time
import datetime

BASE_URL = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject'
BASE_URL_PARAMS = 'https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?dataType=json&term=201931&offset=1&max=500'

def get_departments(term: str):
    """
    Retrieves all of the departments from BASE_URL and returns them as JSON, if it was successful
    """

    maxCount = 300

    # Call getsubjects
    params = {
        'dataType': 'json',
        'term': term,
        'offset': 1,
        'max': maxCount
    }

    r = requests.get(BASE_URL, params=params)
    print(r)

    json = ''
    # Attempt to convert it to JSON
    try:
        json = r.json()
    except:
        print('Error converting depts to JSON')

    return json

def parse_departments(json, term: str):
    """
    Given the JSON of all of the departments, parses them and initializes them into Department objects
    """

    i = 0
    for dept in json:
        code = dept["code"]
        id = f'{code}-{term}'
        # Should have (code, decription)
        dept = Department(id=id, code=code, description=dept["description"], term=term)
        dept.save()
        i = i + 1
    
    print(f"Filled {i} departments")

    return


def scrape_departments(term: str):
    json = get_departments(term)

    parse_departments(json, term)

class Command(base.BaseCommand):
    def handle(self, *args, **options):
        term = options['term']

        # Do stuff
        start = time.time()
        scrape_departments(str(term))
        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        print(f"Finished scraping departments in {time_delta}")

    def add_arguments(self, parser):
        parser.add_argument('term', type=int)