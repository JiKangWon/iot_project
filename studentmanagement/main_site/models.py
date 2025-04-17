from django.db import models
from datetime import timedelta
from django.utils import timezone
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
    def formatted_salary(self):
        return "{:,.0f} VND".format(self.salary)
    
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
    def get_end_day(self):
        return self.start_day + timedelta(weeks=self.number_of_weeks)
    def get_attribute(self):
        current_date = timezone.now().date()
        if self.start_day <= current_date <= self.get_end_day():
            return True

class Subject(models.Model):
    dean = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    credits = models.IntegerField()
    def __str__(self):
        return self.name

class Class(models.Model):
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    start_day = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    sessions_number = models.IntegerField()
    def __str__(self):
        if self.subject and self.lecturer:
            return f"{self.subject.name} - {self.lecturer.name} - {self.get_class_code()}"
        return self.get_class_code()
    def get_class_code(self):
        return f"HCMUTE{self.id}"

class Class_Student(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    middle_term_point = models.IntegerField(blank=True, null=True)
    final_term_point = models.IntegerField(blank=True, null=True)
    def __str__(self):
        if self.class_obj and self.student:
            return f"{self.class_obj.subject.name} - {self.student.name}"
        return f"Class_Student {self.id}"
    def get_total_point(self):
        if self.middle_term_point and self.final_term_point:
            return (self.middle_term_point + self.final_term_point) / 2
        return None
    def get_classification(self):
        absent_count = 0
        attendance = Attendance.objects.filter(class_student=self)
        for att in attendance:
            att_date = Attendance_Date.objects.filter(class_obj=self.class_obj, session_order=att.session_order).first()
            if att_date.date <= timezone.now().date() and att.status == 'absent':
                absent_count += 1
        if absent_count / self.class_obj.sessions_number >= 0.2:
            return "Fail (due to attendance)"
        total_point = self.get_total_point()
        if total_point is not None:
            if total_point >= 9.0:
                return "Excellent"
            elif total_point >= 8.0:
                return "Good"
            elif total_point >= 5.0:
                return "Pass"
            else:
                return "Fail"
        return None

class Attendance(models.Model):
    status_choices = [
        ('present','present'),
        ('absent','absent'),
        ('late','late')
    ]
    class_student = models.ForeignKey(Class_Student, on_delete=models.SET_NULL, null=True)
    session_order = models.IntegerField()
    status = models.CharField(max_length=10, default='absent')
    def __str__(self):
        if self.class_student:
            return f"{self.class_student.class_obj.subject.name} - {self.class_student.student.name} - {self.session_order}"
        return f"Attendance {self.id}"

class Attendance_Date(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    session_order = models.IntegerField()
    def __str__(self):
        if self.class_obj:
            return f"{self.class_obj.subject.name} - {self.date} - {self.session_order}"
        return f"Attendance_Date {self.id}"