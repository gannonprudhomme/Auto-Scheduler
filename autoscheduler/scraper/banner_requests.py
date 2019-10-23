import requests
import time

class BannerRequests():
    """ Handles basic banner requsts stuff """

    # Should we have our own session object?

    def __init__(self):
        self.session = requests.Session()
        self.session_id = ""
        self.term_code = "201931"

    def create_session(self):
        """ First function to be called """

        self.session_id = self.generate_session_id()

        data = {
            'uniqueSessionId': self.session_id,
            'term': self.term_code,
            'dataType': 'json',
        }

        URL = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/'
               'ssb/term/search?mode=search')

        self.session.post(URL, data=data)

    def get_courses(self, department):
        """ Retrieves all of the courses for a given department
            Department: 4 character string, such as CSCE
        """

        self.reset_search() # Reset the session preemptively

        num_courses = 1000
        data = {
            'uniqueSessionId': self.session_id,
            'txt_subject': department,
            'txt_term': self.term_code,
            'pageMaxSize': 1000
        }

        # Would rather use the form above than formatted strings
        URL = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/'
               f'searchResults?txt_subject={department}&txt_term={self.term_code}&'
               f'startDatepicker=&endDatepicker=&pageOffset=0&pageMaxSize={num_courses}&sortColumn='
               f'subjectDescription&sortDirection=asc&uniqueSessionId={self.session_id}')

        response = self.session.get(URL, data=data)

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

    def generate_session_id(self):
        """ Generates a 18 character session id """
        # TODO: Actually generate this
        self.session_id = "y8ixb1571813088562"

        return self.session_id