from django.db import models

from scraper.models import Course

# Should this have a different name?
# Basically a meeting time that a section meets at
class Meeting(models.Model):
    id = models.CharField(max_length=20, primary_key=True) # What would this be?
    build = models.CharField(max_length=4) # Should we reference Building here? If we need it as a model anyways
    dept = models.CharField(max_length=5)
    meeting_days = models.CharField(max_length=7)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # meeting_type = models.CharField(max_length=50)

class Section(models.Model):
    id = models.CharField(max_length=15, primary_key=True) # CRN? Might be a combo
    # parent_course = models.ManyToManyField(Course) # The course this is a section of?

    instructor = models.CharField(max_length=100) # Could this be NULL?
    meetings = models.ManyToManyField(Meeting)