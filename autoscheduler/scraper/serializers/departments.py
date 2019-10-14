from rest_framework import serializers
from scraper import models as scraper_models

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = scraper_models.Department
        fields = (
            "code",
            "description",
        )