from django.contrib import admin
from .models import Room, Student, Complaint


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
