from django.shortcuts import render

def index(request):
    return render(request, 'index.html') # Automatically assumes its in templates/ ?
