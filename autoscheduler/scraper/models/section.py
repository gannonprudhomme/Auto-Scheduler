from django.db import models

from scraper.models import Course

# Should this have a different name?
# Basically a meeting time that a section meets at
class Meeting(models.Model):
    id = models.CharField(max_length=20, primary_key=True) # What would this be?
    crn = models.CharField(max_length=10, db_index=True) # The reference to the section
    building = models.CharField(max_length=4) # Should we reference Building here? If we need it as a model anyways
    meeting_days = models.CharField(max_length=7) # MTWRFSU, where S = saturday, U = Sunday?
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_type = models.CharField(max_length=50) # Lecture, Lab, etc
    

class Section(models.Model):
    id = models.CharField(max_length=15, primary_key=True) # CRN?
    subject = models.CharField(max_length=4)
    # parent_course = models.ManyToManyField(Course) # The course this is a section of?

    instructor = models.CharField(max_length=100) # Could this be NULL?
    meetings = models.ManyToManyField(Meeting)