from django.db import models

class Department(models.Model):
    id = models.CharField(max_length=11, primary_key=True) # What does primary_key do?
    code = models.CharField(max_length=5)# , db_index=True) # What does db_index do?
    description = models.TextField(max_length=100)
    term = models.CharField(max_length=6, null=True)

    class Meta:
        db_table = "departments"