# Called to execute the beginning of scaping courses

from django.base import base
import requests

def scrape_departments():
    """
    Scrapes the departments 
    """

class Command(base.Command):
    def handle(self, *args, **options):
        # Do stuff