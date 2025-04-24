import serial
import time as time_module
import sys
import os
# import requests
from django.utils import timezone
from datetime import datetime, time, timedelta

# Thêm thư mục cha của dự án vào sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # C:\src\project\studentmanagement\studentmanagement
PROJECT_DIR = os.path.dirname(BASE_DIR)  # C:\src\project\studentmanagement
sys.path.append(PROJECT_DIR)

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentmanagement.settings')
import django
django.setup()

# Import mô hình sau khi thiết lập Django
from main_site.models import *
DJANGO_URL = 'http://localhost:8000/attendance/checkin/'
# Kết nối với Arduino
port = 'COM7'  # Cổng đã xác nhận
try:
    ser = serial.Serial(port, 9600, timeout=1)  # Baud rate khớp với Arduino
    time_module.sleep(2)  # Chờ Arduino khởi động
except serial.SerialException as e:
    print(f"Lỗi kết nối với Arduino trên cổng {port}: {e}")
    print("Hãy đảm bảo Arduino IDE Serial Monitor hoặc các chương trình khác không sử dụng COM7.")
    exit(1)

print(f"Đã kết nối với Arduino trên cổng {port}...")
print("Đang đọc dữ liệu từ Arduino...")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("FINGERPRINT_ID:"):
                fingerprint_id = int(line.split(":")[1])
                print(f'Nhận được sinh viên HCMUTE{fingerprint_id}')
                student = Student.objects.filter(id=fingerprint_id).first()
                terms = Term.objects.all()
                for term in terms:
                    if term.get_attribute():
                        current_date = timezone.now().date()
                        current_time = timezone.now().time()
                        class_student_list = Class_Student.objects.filter(class_obj__term=term, student=student)
                        for class_student in class_student_list:
                            today = datetime.today()
                            current_datetime = datetime.combine(today, current_time)
                            add_fifteen_minutes = current_datetime + timedelta(minutes=15)
                            add_thirty_minutes = current_datetime + timedelta(minutes=30)
                            attendance_date = Attendance_Date.objects.filter(class_obj=class_student.class_obj, date=current_date, start_time__lte=add_fifteen_minutes, end_time__gte=add_thirty_minutes).first()
                            if attendance_date:
                                attendance = Attendance.objects.filter(class_student=class_student, session_order=attendance_date.session_order).first()
                                if attendance.status == 'absent':
                                    start_datetime = datetime.combine(today, attendance_date.start_time)
                                    current_datetime = datetime.combine(today, current_time)
                                    if start_datetime - timedelta(minutes=15) <= current_datetime <= start_datetime + timedelta(minutes=15):
                                        attendance.status = 'present'
                                        attendance.save()
                                    else:
                                        attendance.status = 'late'
                                        attendance.save()
                                    # response = requests.post(DJANGO_URL, json={'student_id': student_id})
                                    print(f"Điểm danh thành công cho sinh viên {student.name} trong lớp {class_student.class_obj.subject.name} vào ngày {current_date} lúc {current_time}")
                                break
                        break
    except Exception as e:
        print(f"Lỗi: {e}")
    time_module.sleep(0.1)