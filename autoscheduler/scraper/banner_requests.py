import requests
import time
import asyncio

from typing import Dict, List

TAMU_BASE_URL = 'compassxe-ssb.tamu.edu'

def generate_session_id():
    """ Generates a 18 character session id """
    # TODO: Actually generate this
    session_id = "y8ixb1571813088562"

    return session_id

class BannerRequests():
    """ Handles basic banner requsts stuff """

    # Should we have our own session object?

    def __init__(self, base_url, term_code):
        self.session = None
        self.session_id = ""
        self.term_code = term_code

        self.course_search_url = 'https://%s/StudentRegistrationSsb/ssb/' \
                                  'searchResults/searchResults?txt_subject=' \
                                  '{subject}&txt_term={term}&pageOffset=0&' \
                                  'pageMaxSize={num_courses}&sortColumn=' \
                                  'subjectDescription&sortDirection=asc&' \
                                  'uniqueSessionId={session_id}' % base_url

    def create_session(self):
        """ First function to be called """

        self.session = requests.Session()
        self.session_id = generate_session_id()

        data = {
            'uniqueSessionId': self.session_id,
            'term': self.term_code,
            'dataType': 'json',
        }

        URL = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/'
               'ssb/term/search?mode=search')

        self.session.post(URL, data=data)

    def get_courses(self, department: str):
        """ Retrieves all of the courses for a given department
            Department: 4 character string, such as CSCE
        """

        self.reset_search() # Reset the session preemptively

        num_courses = 1000
        data = {
            'session_id': self.session_id,
            'subject': department,
            'term': self.term_code,
            'num_courses': 1000
        }

        URL = self.course_search_url.format(**data)
        print(URL)

        response = self.session.get(URL)

        json = response.json()
        data = json['data']

        return data

    def reset_search(self):
        """ Does something with the session ID to reset the search

        If you try to call get_courses twice in a row without this, the second
        response will always just be a duplicate of the firsts'
        """
        url = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/'
               'classSearch/resetDataForm')

        self.session.post(url)
