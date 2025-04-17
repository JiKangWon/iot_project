"""
URL configuration for studentmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # ! LECTURER:
    path('lecturer/', views.get_login_lecturer, name='get_login_lecturer'),
    path('lecturer/home/<int:lecturer_id>/', views.get_home_lecturer, name='get_home_lecturer'),
    path('lecturer/class_management/<int:class_id>/', views.get_class_management_lecturer, name='get_class_management_lecturer'),
    path('lecturer/information/<int:lecturer_id>/', views.get_information_lecturer, name='get_information_lecturer'),
    path('lecturer/change_password/<int:lecturer_id>/', views.get_change_password_lecturer, name='get_change_password_lecturer'),
    path('lecturer/update/point/<int:class_id>', views.get_update_point, name='get_update_point'),
    path('lecturer/update/information/<int:lecturer_id>', views.get_update_information_lecturer, name='get_update_information_lecturer'),
    # ! STUDENT:
    path('', views.get_login_student, name='get_login_student'),
    path('student/home/<int:student_id>/', views.get_home_student, name='get_home_student'),
    path('student/information/<int:student_id>', views.get_information_student, name='get_information_student'),
]
