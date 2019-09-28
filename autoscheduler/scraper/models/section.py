from django.db import models

from scraper.models import Course

# Should this have a different name?
# Basically a meeting time that a section meets at
class Meeting(models.Model):
    id = models.CharField(max_length=20, primary_key=True) # What would this be?
    crn = models.CharField(max_length=10, db_index=True) # The reference to the section
    building = models.CharField(max_length=4, null=True) # Should we reference Building here? If we need it as a model anyways
    meeting_days = models.CharField(max_length=7) # MTWRFSU, where S = saturday, U = Sunday?
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    meeting_type = models.CharField(max_length=50) # Lecture, Lab, etc

    class Meta:
        db_table = "meetings"


class Section(models.Model):
    id = models.CharField(max_length=15, primary_key=True) # Combination of crn & term

    subject = models.CharField(max_length=4, db_index=True) # Is this necessary?
    section_num = models.CharField(max_length=6, db_index=True)
    course_num = models.CharField(max_length=6, db_index=True)
    term_code = models.IntegerField(db_index=True) # Going to be filtering by term code a lot

    min_credits = models.IntegerField(null=True) # can this be null?
    max_credits = models.IntegerField(null=True) # Can definitely be null

    # Seating availability?
    max_enrollment = models.IntegerField() # Number of students in the class possible
    current_enrolled = models.IntegerField() # Can this be null?

    # Wait list stuff? Might be cool to show

    instructor = models.CharField(max_length=100) # The instructor's ID. Could this be NULL?
    meetings = models.ManyToManyField(Meeting) # Like an array of meetings?

    class Meta:
        db_table = "sections"
        