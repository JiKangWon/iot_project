from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'gender', 'start_at', 'salary')
    search_fields = ('username', 'name', 'email')
    list_filter = ('gender', 'start_at')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'name', 'email', 'gender', 'start_at', 'credits', 'graduate_at')
    search_fields = ('username', 'name', 'email')
    list_filter = ('gender', 'start_at', 'graduate_at')

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_day', 'number_of_weeks')
    search_fields = ('name',)
    list_filter = ('start_day',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits', 'dean')
    search_fields = ('name',)
    list_filter = ('credits',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('term', 'lecturer', 'subject','sessions_number', 'start_day', 'start_time', 'end_time')
    search_fields = ('term__name', 'lecturer__name', 'subject__name')
    list_filter = ('term', 'lecturer', 'subject')

@admin.register(Class_Student)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'student', 'middle_term_point', 'final_term_point')
    search_fields = ('subject',)
   

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('class_student', 'session_order', 'status')
    list_filter = ('status',)

@admin.register(Attendance_Date)
class AttendanceDateAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'date', 'session_order', 'start_time', 'end_time')
    list_filter = ('date', 'session_order')