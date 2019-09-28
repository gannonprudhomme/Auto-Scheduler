from django.db import models

class Instructor(models.Model):
    id = models.CharField(max_length=9, primary_key=True) # I.e. T00023644
    name = models.TextField(max_length=70)
    pidm = models.CharField(max_length=9, null=True) # Another form of their ID, Like 5ish digits
    email = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "instructors"