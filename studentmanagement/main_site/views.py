from django.shortcuts import render
from .models import *
# Create your views here.
# ! LECTURER:

#! LOGIN:
def get_login_lecturer(request):
    error = None
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            lecturer = Lecturer.objects.get(username=username, password=password)
            return get_home(request, lecturer.id)
        except Lecturer.DoesNotExist:
            error = 'Invalid username or password'
    context = {'error': error}
    return render(request, 'lecturer/login.html', context)

#!HOME:
def get_home(request, lecturer_id):
    error = None
    context = {}
    try:
        lecturer = Lecturer.objects.get(id=lecturer_id)
        context = {'lecturer': lecturer}
        return render(request, 'lecturer/home.html', context)
    except Lecturer.DoesNotExist:
        error = 'Lecturer not found'
    context = {'error': error}
