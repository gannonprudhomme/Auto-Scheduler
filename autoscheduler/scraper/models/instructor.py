from django.db import models

class Instructor(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    name = models.TextField(max_length=70)
    # id = models.CharField(_(""), max_length=50)

    class Meta:
        db_table = "instructors"