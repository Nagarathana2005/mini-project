from django.contrib import admin
from .models import Room, Student, Complaint, LeaveRequest, MessMenu


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'block', 'floor', 'room_type', 'capacity', 'occupied_count', 'availability_status')
    list_filter = ('block', 'room_type', 'availability_status', 'floor')
    search_fields = ('room_number', 'block')
    ordering = ('room_number',)
    readonly_fields = ('occupied_count', 'created_at', 'updated_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department', 'year', 'gender', 'phone', 'email', 'room')
    list_filter = ('department', 'year', 'gender', 'room__block')
    search_fields = ('student_id', 'name', 'phone', 'email', 'room__room_number')
    ordering = ('student_id',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_id', 'student', 'category', 'subject', 'status', 'date')
    list_filter = ('status', 'category', 'date')
    search_fields = ('complaint_id', 'subject', 'student__student_id', 'student__name', 'description')
    ordering = ('-date',)
    readonly_fields = ('complaint_id', 'date', 'updated_at')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'student', 'leave_type', 'start_date', 'end_date', 'destination', 'status')
    list_filter = ('status', 'leave_type', 'start_date')
    search_fields = ('leave_id', 'student__name', 'student__student_id', 'destination', 'reason')
    ordering = ('-applied_at',)
    readonly_fields = ('leave_id', 'applied_at', 'updated_at')


@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'special_dish', 'is_non_veg_day', 'updated_at')
    list_filter = ('is_non_veg_day',)
    search_fields = ('day_of_week', 'special_dish', 'lunch', 'breakfast')

