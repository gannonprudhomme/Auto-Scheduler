from django.contrib import admin

# Register your models here.
from scraper.models import Section, Course, Meeting, Instructor, Department

admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Meeting)
admin.site.register(Instructor)
admin.site.register(Department)