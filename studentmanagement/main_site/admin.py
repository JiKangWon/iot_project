from django.contrib import admin
from .models import Lecturer, Student, Term, Subject, Class_Student, Attendance
# Register your models here.

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'gender', 'start_at', 'salary')
    search_fields = ('username', 'name', 'email')
    list_filter = ('gender', 'start_at')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'gender', 'start_at', 'credits', 'graduate_at')
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

@admin.register(Class_Student)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('class_code', 'term', 'lecturer', 'student', 'subject', 'start_day', 'sessions_number', 'middle_term_point', 'final_term_point')
    search_fields = ('class_code',)
    list_filter = ('term', 'subject', 'lecturer')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('class_student', 'session_order', 'status')
    list_filter = ('status',)
