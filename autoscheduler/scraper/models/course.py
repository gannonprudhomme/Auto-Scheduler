from django.db import models

class Course(models.Model): # Directly from GBS:w
    id = models.CharField(max_length=10, primary_key=True) # Could be dept+course_num
    dept = models.CharField(max_length=4, db_index=True) # CSCE
    course_num = models.CharField(max_length=5, db_index=True) # i.e. 221
    title = models.CharField(max_length=100) # Course title, i.e. "Data Structres & Algorithms"
    description = models.TextField(null=True, blank=True)
    # prerequisites = models.TextField(null=True, blank=True)
    # corequisites = models.TextField(null=True, blank=True)
    # min_credits = models.FloatField(null=True)
    # max_credits = models.FloatField(null=True)
    # distribution_of_hours = models.CharField(max_length=100)

    class Meta:
        db_table = "courses"