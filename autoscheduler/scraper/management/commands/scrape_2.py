import asyncio
import os
import random
import string
import time

import aiohttp
import requests

from scraper.models.department import Department
from django.core.management import base

TAMU_BASE_URL = "compassxe-ssb.tamu.edu"
UAEU_BASE_URL = "eservices.uaeu.ac.ae"


def get_session_id():
    session_id = "".join(random.sample(string.ascii_lowercase, 5)) + str(int(time.time() * 1000))
    return session_id


class CourseGrabber:
    """Grabs courses for one or more terms.
    Args:
        loop: asyncio event loop
        base_url (str): Base Banner URL for university (e.g., eservices.uaeu.ac.ae)"
    """
    def __init__(self, base_url):
        self.session = None
        self.wrong = 0
        self.right = 0
        self.empty = 0

        # Build university-specific URLs
        self.terms_url = "https://%s/StudentRegistrationSsb/ssb/classSearch/getTerms" \
                         "?dataType=json&searchTerm=&offset=1&max=-1" % base_url
        self.start_search_url = \
            "https://%s/StudentRegistrationSsb/ssb/term/search?mode=search" % base_url
        self.reset_search_url = \
            "https://%s/StudentRegistrationSsb/ssb/classSearch/resetDataForm" % base_url
        self.subjects_url = \
            "https://%s/StudentRegistrationSsb/ssb/classSearch/get_subject" \
            "?dataType=json&term={term}&offset=1&max=-1&uniqueSessionId=" \
            "{session_id}" % base_url
        self.courses_url = \
            "https://%s/StudentRegistrationSsb/ssb/searchResults/searchResults" \
            "?txt_subject={subject}&txt_term={term}&startDatepicker=&endDatepi" \
            "cker=&pageOffset=0&pageMaxSize=1000&sortColumn=subjectDescription&" \
            "sortDirection=asc&uniqueSessionId={session_id}" % base_url

    def get_terms(self):
        return [each["code"] for each in requests.get(self.terms_url).json()]

    async def get_subjects(self, term, client):
        """Get all subjects for a given term."""
        args = {"session_id": self.session_id, "term": term}
        url = self.subjects_url.format(**args)

        async with client.get(url) as resp:
            data = await resp.json()
            print(data)

        return data

    async def get_courses(self, term, subject, session_id, client):
        args = {"session_id": session_id, "term": term, "subject": subject}
        url = self.courses_url.format(**args)

        async with client.get(url) as resp:
            data = await resp.json()

        # Reset the session
        async with client.post(self.reset_search_url,
                               data={"uniqueSessionId": session_id}) as resp:
            _ = await resp.text()

        if not data["success"]:
            self.empty = self.empty + 1
            return {}

        if data["data"] is None:
            self.empty = self.empty + 1
            print('Data is empty for ' + subject + ' ' + str(self.empty))
            return {}

        # Transform list to dict of subject -> course number -> data
        transformed = {}

        dept_retrieved = ''
        for info in data["data"]:
            dept_retrieved = info['subject']

        if(not subject == dept_retrieved):
            self.wrong = self.wrong + 1
            print(subject + ' retrieved ' + dept_retrieved + ' ' + str(self.wrong))
        else:
            self.right = self.right + 1
            print(subject + ' retrieved correctely ' + str(self.right))

        return dept_retrieved
        #return data["data"]

    async def search(self, term, subjects, client):
        """Start a new Banner course search for a given term."""
        loop = asyncio.get_running_loop()

        # Start new search session
        session_id = get_session_id()
        payload = {
            "uniqueSessionId": session_id,
            "dataType": "json",
            "term": term,
        }

        async with client.post(self.start_search_url, data=payload) as resp:
            _ = await resp.json()

        # Get all subjects for this term
        if not subjects:
            subjects = [each["code"] for each in
                        await self.get_subjects(term, client)]

        # Get courses for all subjects in the term
        tasks = [self.get_courses(term, subject, session_id, client) for subject in subjects]
        results = []

        # for result in asyncio.gather(*tasks, loop=loop):
        for task in tasks:
            results += await task

        return results

    async def fetch(self, terms, subjects=[]):
        """Start searching for courses in one or more terms."""
        loop = asyncio.get_running_loop()

        async with aiohttp.ClientSession(loop=loop) as client:
            tasks = [self.search(term, subjects, client) for term in terms]
            results = await asyncio.gather(*tasks, loop=loop)

        print(f'{self.right} correct and {self.wrong} incorrect, {self.empty} empty, {self.right + self.wrong + self.empty} total')

        return results

class Command(base.BaseCommand):
    def handle(self, *args, **options):
        grabber = CourseGrabber(base_url=TAMU_BASE_URL)
        terms = grabber.get_terms()

        depts = [model.code for model in Department.objects.all()]
        output = asyncio.run(grabber.fetch(["201931"], depts))

        # print(output)
