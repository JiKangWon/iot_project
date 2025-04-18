from django.shortcuts import render, redirect
from .models import *
from django.db.models import ExpressionWrapper, F, DateField, DurationField
from datetime import datetime, timedelta
from django.utils import timezone
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
            return redirect('get_home_lecturer', lecturer_id=lecturer.id)
        except Lecturer.DoesNotExist:
            error = 'Invalid username or password'
    context = {'error': error}
    return render(request, 'lecturer/login.html', context)

#!HOME:
def get_home_lecturer(request, lecturer_id):
    context = {}
    lecturer = Lecturer.objects.filter(id=lecturer_id).first()
    terms = Term.objects.all()
    for term in terms:
        if term.get_attribute():
            context['term'] = term
            context['lecturer'] = lecturer
            classes = Class.objects.filter(lecturer=lecturer, term=term)
            context['classes'] = classes
            break
    return render(request, 'lecturer/home.html', context)

# ! CLASS MANAGEMENT:
def get_class_management_lecturer(request, class_id):
    context = {}
    class_obj = Class.objects.filter(id=class_id).first()
    context['class_obj'] = class_obj
    class_student_list = Class_Student.objects.filter(class_obj=class_obj)
    attendance_date_list = Attendance_Date.objects.filter(class_obj=class_obj)
    context['attendance_date_list'] = attendance_date_list
    class_student_data = []
    for class_student in class_student_list:
        attendance_default = Attendance.objects.filter(class_student=class_student)
        attendance = []
        for att in attendance_default:
            att_date = Attendance_Date.objects.filter(class_obj=class_obj, session_order=att.session_order).first()
            if att_date.date <= timezone.now().date():
                attendance.append(att.status)
            else:
                attendance.append(None)
        class_student_data.append(
            {
                'class_student': class_student,
                'attendance': attendance,
            }
        )
    context['class_student_data'] = class_student_data
    return render(request, 'lecturer/class_management.html', context)

# ! INFORMATION:
def get_information_lecturer(request, lecturer_id):
    lecturer = Lecturer.objects.filter(id=lecturer_id).first()
    context = {}
    context['lecturer'] = lecturer
    return render(request, 'lecturer/information.html', context)

# ! CHANGE PASSWORD:
def get_change_password_lecturer(request, lecturer_id):
    error = None
    context = {}
    lecturer = Lecturer.objects.filter(id=lecturer_id).first()
    context['lecturer'] = lecturer
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if lecturer.password != old_password:
            error = 'Old password is incorrect!'
        elif new_password != confirm_password:
            error = 'New password and confirm password do not match!'
        else:
            lecturer.password = new_password
            lecturer.save()
            return redirect('get_login_lecturer')
    context['error'] = error
    return render(request, 'lecturer/change_password.html', context)

# ! UPDATE POINT:
def get_update_point(request, class_id):
    context = {}
    class_obj = Class.objects.filter(id=class_id).first()
    context['class_obj'] = class_obj
    class_student_list = Class_Student.objects.filter(class_obj=class_obj)
    context['class_student_list'] = class_student_list
    if request.method == 'POST':
        for class_student in class_student_list:
            middle_term_point = request.POST.get(f'middle_term_point_{class_student.id}')
            final_term_point = request.POST.get(f'final_term_point_{class_student.id}')
            if middle_term_point and final_term_point:
                class_student.middle_term_point = middle_term_point
                class_student.final_term_point = final_term_point
                class_student.save()
        return redirect('get_class_management_lecturer', class_id=class_obj.id)
    return render(request, 'lecturer/update_point.html', context)

# ! UPDATE INFORMATION:
def get_update_information_lecturer(request, lecturer_id):
    context = {}
    lecturer = Lecturer.objects.filter(id=lecturer_id).first()
    context['lecturer'] = lecturer
    if request.method == 'POST':
        lecturer.name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        lecturer.birth_day = datetime.strptime(birthday, '%Y-%m-%d').date()
        lecturer.email = request.POST.get('email')
        lecturer.phone_number = request.POST.get('phone')
        lecturer.gender = request.POST.get('gender')
        lecturer.save()
        return redirect('get_information_lecturer', lecturer_id=lecturer.id)
    return render(request, 'lecturer/update_information.html', context)

# ! STUDENT:

#! LOGIN:
def get_login_student(request):
    error = None
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(username=username, password=password)
            return redirect('home_student', student_id=student.id)
        except Student.DoesNotExist:
            error = 'Invalid username or password'
    context = {'error': error}
    return render(request, 'student/login.html', context)

#!HOME:
def get_home_student(request, student_id):
    error = None
    context = {}
    try:
        student= Student.objects.get(id=student_id)
        context = {'student': student}
        return render(request, 'student/home.html', context)
    except Student.DoesNotExist:
        error = 'Student not found'
        context = {'error': error}
        return render(request, 'student/home.html', context)

# ! INFORMATION:
def get_information_student(request, student_id):
    error = None
    context = {}
    student = Student.objects.filter(id=student_id).first()
    context['student'] = student
    return render(request, 'student/information.html', context)

#! CHANGE PASSWORD:
def get_change_password_student(request, student_id):
    error = None
    context = {}
    student = Student.objects.filter(id=student_id).first()
    context['student'] = student
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if student.password != old_password:
            error = 'Old password is incorrect!'
        elif new_password != confirm_password:
            error = 'New password and confirm password do not match!'
        else:
            student.password = new_password
            student.save()
            return redirect('get_login_student')
    context['error'] = error
    return render(request, 'student/change_password.html', context)

def get_update_information_student(request, student_id):
    context = {}
    student = Student.objects.filter(id=student_id).first()
    context['student'] = student
    if request.method == 'POST':
        student.name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        student.birth_day = datetime.strptime(birthday, '%Y-%m-%d').date()
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone')
        student.gender = request.POST.get('gender')
        student.save()
        return redirect('get_information_student', student_id=student.id)
    return render(request, 'student/update_information.html', context)

#Class
def get_class_information_student(request, class_id, student_id):
    context = {}

    # Lấy thông tin lớp học
    class_obj = Class.objects.filter(id=class_id).first()
    if not class_obj:
        context['error_message'] = 'Lớp học không tồn tại.'
        return render(request, 'student/class_information.html', context)

    context['class_obj'] = class_obj

    # Kiểm tra sinh viên có học lớp này không
    class_student = Class_Student.objects.filter(
        class_obj=class_obj,
        student__id=student_id
    ).first()

    if not class_student:
        context['error_message'] = 'Sinh viên không học lớp này.'
        return render(request, 'student/class_information.html', context)

    # Lấy danh sách các buổi học của lớp
    attendance_date_list = Attendance_Date.objects.filter(class_obj=class_obj).order_by('session_order')

    # Lấy các bản ghi điểm danh của sinh viên trong lớp này
    attendance_records = Attendance.objects.filter(class_student=class_student)

    # Tạo dictionary để tra nhanh trạng thái điểm danh theo session_order
    attendance_dict = {att.session_order: att.status for att in attendance_records}

    # Gộp thông tin từng buổi học với trạng thái điểm danh
    attendance_data = []
    for att_date in attendance_date_list:
        if att_date.date <= timezone.now().date():
            status = attendance_dict.get(att_date.session_order, None)
        else:
            status = None  # Buổi học tương lai
        attendance_data.append((att_date.session_order, att_date.date, status))

    # Truyền dữ liệu về điểm số và phân loại
    context['class_student'] = class_student
    context['attendance_data'] = attendance_data
    context['total_point'] = class_student.get_total_point()
    context['classification'] = class_student.get_classification()

    return render(request, 'student/class_information.html', context)



def home_student(request, student_id):
    context = {}
    student = Student.objects.filter(id=student_id).first()
    context['student'] = student

    # Lấy các lớp mà sinh viên đã tham gia
    class_students = Class_Student.objects.filter(student=student)
    classes = [cs.class_obj for cs in class_students]
    context['classes'] = classes

    return render(request, 'student/home.html', context)