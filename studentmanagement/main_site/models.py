from django.db import models

# Create your models here.
class Lecturer(models.Model):
    gender_choices = [
        ('male','male'),
        ('female','female'),
        ('other','other')
    ]
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    birth_day = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, default='other')
    start_at = models.DateField()
    salary = models.IntegerField()
    def __str__(self):
        return self.name
    
class Student(models.Model):
    gender_choices = [
        ('male','male'),
        ('female','female'),
        ('other','other')
    ]
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    birth_day = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, default='other')
    start_at = models.DateField()
    credits = models.IntegerField()
    graduate_at = models.DateField(null=True)
    def __str__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_day = models.DateField()
    number_of_weeks = models.IntegerField()
    def __str__(self):
        return self.name

class Subject(models.Model):
    dean = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    credits = models.IntegerField()

class Class_Student(models.Model):
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    class_code = models.CharField(max_length=100)
    start_day = models.DateField()
    sessions_number = models.IntegerField()
    middle_term_point = models.IntegerField()
    final_term_point = models.IntegerField()

class Attendance(models.Model):
    status_choices = [
        ('present','present'),
        ('absent','absent'),
        ('late','late')
    ]
    class_student = models.ForeignKey(Class_Student, on_delete=models.SET_NULL, null=True)
    session_order = models.IntegerField()
    status = models.CharField(max_length=10, default='absent')

