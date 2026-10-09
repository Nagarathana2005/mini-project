from django.urls import path
from . import views

urlpatterns = [
    # General / Auth
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Admin / Warden Portal
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/stats/', views.hostel_stats, name='hostel_stats'),

    # Student Management
    path('admin-dashboard/students/', views.student_list, name='student_list'),
    path('admin-dashboard/students/add/', views.student_create, name='student_create'),
    path('admin-dashboard/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('admin-dashboard/students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('admin-dashboard/students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Room Management
    path('admin-dashboard/rooms/', views.room_list, name='room_list'),
    path('admin-dashboard/rooms/add/', views.room_create, name='room_create'),
    path('admin-dashboard/rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('admin-dashboard/rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('admin-dashboard/rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    # Complaints (Admin)
    path('admin-dashboard/complaints/', views.complaint_list, name='complaint_list'),
    path('admin-dashboard/complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),

    # Leave & Gate Pass (Admin)
    path('admin-dashboard/leaves/', views.leave_list, name='leave_list'),
    path('admin-dashboard/leaves/<int:pk>/', views.leave_detail, name='leave_detail'),

    # Mess & Food Menu (General & Admin)
    path('mess-menu/', views.mess_menu_view, name='mess_menu_view'),
    path('admin-dashboard/mess-menu/<int:pk>/edit/', views.mess_menu_edit, name='mess_menu_edit'),

    # Student Portal
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-dashboard/profile/', views.student_profile, name='student_profile'),
    path('student-dashboard/room/', views.student_room, name='student_room'),
    path('student-dashboard/complaints/submit/', views.submit_complaint, name='submit_complaint'),
    path('student-dashboard/complaints/', views.my_complaints, name='my_complaints'),
    path('student-dashboard/complaints/<int:pk>/', views.student_complaint_detail, name='student_complaint_detail'),

    # Leave & Gate Pass (Student)
    path('student-dashboard/leaves/apply/', views.apply_leave, name='apply_leave'),
    path('student-dashboard/leaves/', views.my_leaves, name='my_leaves'),
    path('student-dashboard/leaves/<int:pk>/', views.leave_detail_student, name='leave_detail_student'),
]

