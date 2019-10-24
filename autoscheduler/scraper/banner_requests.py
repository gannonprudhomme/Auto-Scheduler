import time
import asyncio
import aiohttp

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
        self.session_id = ""
        self.term_code = term_code

        self.course_search_url = 'https://%s/StudentRegistrationSsb/ssb/' \
                                  'searchResults/searchResults?txt_subject=' \
                                  '{subject}&txt_term={term}&pageOffset=0&' \
                                  'pageMaxSize={num_courses}&sortColumn=' \
                                  'subjectDescription&sortDirection=asc&' \
                                  'uniqueSessionId={session_id}' % base_url

    async def create_session(self, session: aiohttp.ClientSession):
        """ First function to be called """

        self.session_id = generate_session_id()

        data = {
            'uniqueSessionId': self.session_id,
            'term': self.term_code,
            'dataType': 'json',
        }

        URL = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/'
               'ssb/term/search?mode=search')

        async with session.post(URL, data=data) as resp:
            data = await resp.json()

    async def search(self, departments: List[str]):
        """ Returns a list of futures for retrieving """

        loop = asyncio.get_running_loop()

        results = []
        async with aiohttp.ClientSession(loop=loop) as session:
            await self.create_session(session)

            tasks = [self.get_courses(session, department) 
                     for department in departments]
            for result in await asyncio.gather(*tasks, loop=loop):
                results.append(result)
        
        return results

    async def get_courses(self, session, department: str):
        """ Retrieves all of the courses for a given department
            Department: 4 character string, such as CSCE
            Should return a future?
        """

        num_courses = 1000
        data = {
            'session_id': self.session_id,
            'subject': department,
            'term': self.term_code,
            'num_courses': num_courses
        }

        URL = self.course_search_url.format(**data)

        print('Attempting to retrieve ' + department)
        async with session.get(URL) as resp:
            json = await resp.json()

        await self.reset_search(session)
        
        data = json['data']
        if(data != None):
            print('Retreived ' + str(len(data)) + ' sections for ' + department)
        else:
            print('Retrieved no sections for ' + department)

        return data

    async def reset_search(self, session):
        """ Does something with the session ID to reset the search

        If you try to call get_courses twice in a row without this, the second
        response will always just be a duplicate of the firsts'
        """
        url = ('https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/'
               'classSearch/resetDataForm')

        await session.post(url)
        #async with session.post(url) as resp:
        #    data = await resp.json()

        #return data # Don't really need to though
