from django.shortcuts import render
from rest_framework import renderers, generics, response

from . import models, serializers

# Create your views here.
class DepartmentSearchView(generics.ListAPIView):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = serializers.DepartmentSerializer

    # Get 
    def get_queryset(self):
        """
        Returns all of the courses that match the text that was provided
        Ex: In: "AGS". Out: "AGSC - Agrictulral Science, AGSM - Agriculture Systems Mgmt"
        """

        dept = self.kwargs["dept"] # The input they've given us. If url was /api/data/AGS, dept would be AGS

        # Check for a cached result? django.core.cache package
        depts = models.Department.objects.filter(code__istartswith=dept)
        return depts
