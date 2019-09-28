from django.db import models

class Department(models.Model):
    # id = models.CharField(max_length=10, primary_key=True) # What does primary_key do?
    code = models.CharField(max_length=4, primary_key=True)# , db_index=True) # What does db_index do?
    description = models.TextField(max_length=100)

    class Meta:
        db_table = "departments"