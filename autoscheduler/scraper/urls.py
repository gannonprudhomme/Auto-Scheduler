from django.urls import path
from scraper import views

urlpatterns = [
    path("depts/<str:dept>", views.DepartmentSearchView.as_view(), name="departments"),
]