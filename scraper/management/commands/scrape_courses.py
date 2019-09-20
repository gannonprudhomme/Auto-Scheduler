# Called to execute the beginning of scaping courses

from django.base import base

class Command(base.Command):
    def handle(self, *args, **options):
        # Do stuff