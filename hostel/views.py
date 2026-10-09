import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from .models import Room, Student, Complaint, LeaveRequest, MessMenu
from .forms import (
    LoginForm,
    RoomForm,
    StudentForm,
    StudentEditForm,
    ComplaintForm,
    ComplaintResponseForm,
    LeaveRequestForm,
    LeaveActionForm,
    MessMenuForm,
)
from .decorators import admin_required, student_required


# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

def login_view(request):
    """Unified login for Admin/Warden and Students."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_staff or user.is_superuser:
                    messages.success(request, f"Welcome back, {user.get_full_name() or user.username} (Admin/Warden)!")
                    return redirect('admin_dashboard')
                elif hasattr(user, 'student_profile'):
                    messages.success(request, f"Welcome, {user.student_profile.name}!")
                    return redirect('student_dashboard')
                else:
                    messages.info(request, "Logged in successfully.")
                    return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid Student ID / Username or Password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def dashboard_redirect(request):
    """Directs logged-in users to their appropriate dashboard."""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif hasattr(request.user, 'student_profile'):
        return redirect('student_dashboard')
    return redirect('login')


# ==========================================
# ADMIN / WARDEN VIEWS
# ==========================================

@admin_required
def admin_dashboard(request):
    """Main administrative dashboard displaying summary metrics and recent activity."""
    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(availability_status='Available').count()
    occupied_rooms = Room.objects.filter(occupied_count__gt=0).count()
    full_rooms = Room.objects.filter(availability_status='Full').count()
    maintenance_rooms = Room.objects.filter(availability_status='Maintenance').count()

    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    in_progress_complaints = Complaint.objects.filter(status='In Progress').count()
    resolved_complaints = Complaint.objects.filter(status='Resolved').count()
    rejected_complaints = Complaint.objects.filter(status='Rejected').count()

    # Leave requests count
    pending_leaves = LeaveRequest.objects.filter(status='Pending').count()
    approved_leaves = LeaveRequest.objects.filter(status='Approved').count()
    recent_leaves = LeaveRequest.objects.select_related('student', 'student__room').order_by('-applied_at')[:5]

    # Calculate overall occupancy percentage
    total_capacity = sum(r.capacity for r in Room.objects.all()) or 1
    total_occupied_beds = sum(r.occupied_count for r in Room.objects.all())
    overall_occupancy_pct = int((total_occupied_beds / total_capacity) * 100) if total_capacity else 0

    recent_complaints = Complaint.objects.select_related('student', 'student__room').order_by('-date')[:6]
    recent_students = Student.objects.select_related('room').order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'full_rooms': full_rooms,
        'maintenance_rooms': maintenance_rooms,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
        'rejected_complaints': rejected_complaints,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'recent_leaves': recent_leaves,
        'total_capacity': total_capacity,
        'total_occupied_beds': total_occupied_beds,
        'overall_occupancy_pct': overall_occupancy_pct,
        'recent_complaints': recent_complaints,
        'recent_students': recent_students,
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
def student_list(request):
    """View, search, and filter all registered students."""
    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '').strip()
    year = request.GET.get('year', '').strip()
    gender = request.GET.get('gender', '').strip()
    room_status = request.GET.get('room_status', '').strip()

    students = Student.objects.select_related('room').all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(room__room_number__icontains=query)
        )

    if department:
        students = students.filter(department=department)

    if year:
        students = students.filter(year=year)

    if gender:
        students = students.filter(gender=gender)

    if room_status == 'assigned':
        students = students.filter(room__isnull=False)
    elif room_status == 'unassigned':
        students = students.filter(room__isnull=True)

    departments = Student.DEPARTMENT_CHOICES
    years = Student.YEAR_CHOICES
    genders = Student.GENDER_CHOICES

    context = {
        'students': students,
        'query': query,
        'selected_department': department,
        'selected_year': year,
        'selected_gender': gender,
        'selected_room_status': room_status,
        'departments': departments,
        'years': years,
        'genders': genders,
        'total_count': students.count(),
    }
    return render(request, 'admin/student_list.html', context)


@admin_required
def student_create(request):
    """Add a new student and generate user authentication credentials."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create User instance
            user = User.objects.create_user(
                username=student_id,
                email=email,
                password=password,
                first_name=name
            )

            # Create Student instance
            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, f"Student {name} ({student_id}) has been added successfully! Login password: {password}")
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()

    return render(request, 'admin/student_form.html', {'form': form, 'title': 'Add New Student', 'is_create': True})


@admin_required
def student_edit(request, pk):
    """Edit student details and room allocation."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            student = form.save()

            # Update student user account details
            user = student.user
            user.email = student.email
            user.first_name = student.name
            if new_password:
                user.set_password(new_password)
            user.save()

            messages.success(request, f"Student {student.name} updated successfully.")
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'admin/student_form.html', {
        'form': form,
        'student': student,
        'title': f"Edit Student: {student.name}",
        'is_create': False
    })


@admin_required
def student_delete(request, pk):
    """Delete a student and free up their allocated bed."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        sid = student.student_id
        student.delete()
        messages.success(request, f"Student {name} ({sid}) was deleted successfully.")
        return redirect('student_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': student,
        'type': 'Student',
        'cancel_url': 'student_list'
    })


@admin_required
def student_detail(request, pk):
    """View full profile, assigned room, roommates, and complaints for a student."""
    student = get_object_or_404(Student.objects.select_related('room', 'user'), pk=pk)
    roommates = []
    if student.room:
        roommates = student.room.students.exclude(pk=student.pk)
    complaints = student.complaints.all()

    # Room choices for quick room assignment if student has no room
    available_rooms = Room.objects.filter(Q(availability_status='Available') | Q(id=student.room_id if student.room else -1))

    if request.method == 'POST' and 'assign_room' in request.POST:
        new_room_id = request.POST.get('room_id')
        if new_room_id:
            new_room = get_object_or_404(Room, pk=new_room_id)
            if new_room.students.count() >= new_room.capacity and new_room != student.room:
                messages.error(request, f"Room {new_room.room_number} is already full.")
            elif new_room.availability_status == 'Maintenance':
                messages.error(request, f"Room {new_room.room_number} is under maintenance.")
            else:
                student.room = new_room
                student.save()
                messages.success(request, f"Room {new_room.room_number} assigned to {student.name}.")
        else:
            student.room = None
            student.save()
            messages.info(request, f"Room unassigned for {student.name}.")
        return redirect('student_detail', pk=student.pk)

    context = {
        'student': student,
        'roommates': roommates,
        'complaints': complaints,
        'available_rooms': available_rooms,
    }
    return render(request, 'admin/student_detail.html', context)


# ==========================================
# ROOM MANAGEMENT VIEWS
# ==========================================

@admin_required
def room_list(request):
    """View, search, and filter hostel rooms with capacity and occupancy stats."""
    query = request.GET.get('q', '').strip()
    block = request.GET.get('block', '').strip()
    status = request.GET.get('status', '').strip()
    room_type = request.GET.get('room_type', '').strip()

    rooms = Room.objects.prefetch_related('students').all()

    if query:
        rooms = rooms.filter(
            Q(room_number__icontains=query) |
            Q(block__icontains=query)
        )

    if block:
        rooms = rooms.filter(block=block)

    if status:
        rooms = rooms.filter(availability_status=status)

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    blocks = Room.objects.values_list('block', flat=True).distinct()
    room_types = Room.ROOM_TYPE_CHOICES
    status_choices = Room.STATUS_CHOICES

    context = {
        'rooms': rooms,
        'query': query,
        'selected_block': block,
        'selected_status': status,
        'selected_type': room_type,
        'blocks': blocks,
        'room_types': room_types,
        'status_choices': status_choices,
        'total_count': rooms.count(),
    }
    return render(request, 'admin/room_list.html', context)


@admin_required
def room_create(request):
    """Add a new room to the hostel."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f"Room {room.room_number} created successfully.")
            return redirect('room_detail', pk=room.pk)
    else:
        form = RoomForm()

    return render(request, 'admin/room_form.html', {'form': form, 'title': 'Add New Room'})


@admin_required
def room_edit(request, pk):
    """Edit room specifications and capacity."""
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            room.update_occupancy()
            messages.success(request, f"Room {room.room_number} updated successfully.")
            return redirect('room_detail', pk=room.pk)
    else:
        form = RoomForm(instance=room)

    return render(request, 'admin/room_form.html', {'form': form, 'room': room, 'title': f"Edit Room: {room.room_number}"})


@admin_required
def room_delete(request, pk):
    """Delete a room safely."""
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_num = room.room_number
        # Unassign any students currently in this room
        room.students.update(room=None)
        room.delete()
        messages.success(request, f"Room {room_num} deleted. Any allocated students have been unassigned.")
        return redirect('room_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': room,
        'type': 'Room',
        'cancel_url': 'room_list'
    })


@admin_required
def room_detail(request, pk):
    """View occupants, capacity details, and assign students to this room."""
    room = get_object_or_404(Room.objects.prefetch_related('students'), pk=pk)
    occupants = room.students.all()

    # Unassigned students available to be placed in this room
    unallocated_students = Student.objects.filter(room__isnull=True)

    if request.method == 'POST':
        if 'add_student' in request.POST:
            student_id = request.POST.get('student_id')
            if student_id:
                student = get_object_or_404(Student, pk=student_id)
                if room.students.count() >= room.capacity:
                    messages.error(request, f"Cannot assign student. Room {room.room_number} is already at full capacity ({room.capacity}).")
                elif room.availability_status == 'Maintenance':
                    messages.error(request, f"Cannot assign student. Room {room.room_number} is under maintenance.")
                else:
                    student.room = room
                    student.save()
                    messages.success(request, f"{student.name} assigned to Room {room.room_number}.")
            return redirect('room_detail', pk=room.pk)

        elif 'remove_student' in request.POST:
            student_id = request.POST.get('student_id')
            if student_id:
                student = get_object_or_404(Student, pk=student_id)
                student.room = None
                student.save()
                messages.info(request, f"{student.name} removed from Room {room.room_number}.")
            return redirect('room_detail', pk=room.pk)

    context = {
        'room': room,
        'occupants': occupants,
        'unallocated_students': unallocated_students,
    }
    return render(request, 'admin/room_detail.html', context)


# ==========================================
# COMPLAINT MANAGEMENT (ADMIN)
# ==========================================

@admin_required
def complaint_list(request):
    """View and filter all hostel complaints."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    complaints = Complaint.objects.select_related('student', 'student__room').all()

    if query:
        complaints = complaints.filter(
            Q(complaint_id__icontains=query) |
            Q(subject__icontains=query) |
            Q(student__name__icontains=query) |
            Q(student__student_id__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        complaints = complaints.filter(category=category)

    if status:
        complaints = complaints.filter(status=status)

    categories = Complaint.CATEGORY_CHOICES
    status_choices = Complaint.STATUS_CHOICES

    context = {
        'complaints': complaints,
        'query': query,
        'selected_category': category,
        'selected_status': status,
        'categories': categories,
        'status_choices': status_choices,
        'total_count': complaints.count(),
    }
    return render(request, 'admin/complaint_list.html', context)


@admin_required
def complaint_detail(request, pk):
    """View complaint details, update status, and add warden response."""
    complaint = get_object_or_404(Complaint.objects.select_related('student', 'student__room'), pk=pk)

    if request.method == 'POST':
        form = ComplaintResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, f"Complaint {complaint.complaint_id} updated successfully.")
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintResponseForm(instance=complaint)

    context = {
        'complaint': complaint,
        'form': form,
    }
    return render(request, 'admin/complaint_detail.html', context)


# ==========================================
# HOSTEL STATISTICS (ADMIN)
# ==========================================

@admin_required
def hostel_stats(request):
    """Analytical statistics and breakdown charts data for MCA project presentation."""
    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    total_capacity = sum(r.capacity for r in Room.objects.all())
    total_occupied_beds = sum(r.occupied_count for r in Room.objects.all())
    available_beds = max(0, total_capacity - total_occupied_beds)

    # Department breakdown
    dept_stats = Student.objects.values('department').annotate(count=Count('id')).order_by('-count')

    # Year breakdown
    year_stats = Student.objects.values('year').annotate(count=Count('id')).order_by('year')

    # Gender breakdown
    gender_stats = Student.objects.values('gender').annotate(count=Count('id'))

    # Complaint categories breakdown
    complaint_category_stats = Complaint.objects.values('category').annotate(count=Count('id')).order_by('-count')

    # Complaint status breakdown
    complaint_status_stats = Complaint.objects.values('status').annotate(count=Count('id'))

    # Block-wise room occupancy
    blocks = Room.objects.values('block').annotate(
        total_rooms=Count('id'),
    )
    block_data = []
    for b in blocks:
        block_name = b['block']
        block_rooms = Room.objects.filter(block=block_name)
        b_cap = sum(r.capacity for r in block_rooms)
        b_occ = sum(r.occupied_count for r in block_rooms)
        b_pct = int((b_occ / b_cap * 100)) if b_cap > 0 else 0
        block_data.append({
            'block': block_name,
            'total_rooms': b['total_rooms'],
            'capacity': b_cap,
            'occupied': b_occ,
            'available': max(0, b_cap - b_occ),
            'percentage': b_pct
        })

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'total_capacity': total_capacity,
        'total_occupied_beds': total_occupied_beds,
        'available_beds': available_beds,
        'dept_stats': dept_stats,
        'year_stats': year_stats,
        'gender_stats': gender_stats,
        'complaint_category_stats': complaint_category_stats,
        'complaint_status_stats': complaint_status_stats,
        'block_data': block_data,
    }
    return render(request, 'admin/stats.html', context)


# ==========================================
# STUDENT PORTAL VIEWS
# ==========================================

@student_required
def student_dashboard(request):
    """Personalized dashboard for logged-in student."""
    student = request.user.student_profile
    complaints = student.complaints.all()

    total_submitted = complaints.count()
    pending_count = complaints.filter(status='Pending').count()
    in_progress_count = complaints.filter(status='In Progress').count()
    resolved_count = complaints.filter(status='Resolved').count()

    recent_complaints = complaints[:5]
    roommates = []
    if student.room:
        roommates = student.room.students.exclude(pk=student.pk)

    # Leave & Gate Pass metrics
    pending_leaves_count = student.leave_requests.filter(status='Pending').count()
    approved_leaves_count = student.leave_requests.filter(status='Approved').count()
    active_gate_pass = student.leave_requests.filter(status='Approved').order_by('-start_date').first()
    latest_leave = student.leave_requests.order_by('-applied_at').first()

    # Today's South Indian Mess Menu
    today_name = datetime.date.today().strftime('%A')
    today_menu = MessMenu.objects.filter(day_of_week=today_name).first()

    context = {
        'student': student,
        'room': student.room,
        'roommates': roommates,
        'total_submitted': total_submitted,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'recent_complaints': recent_complaints,
        'pending_leaves_count': pending_leaves_count,
        'approved_leaves_count': approved_leaves_count,
        'active_gate_pass': active_gate_pass,
        'latest_leave': latest_leave,
        'today_name': today_name,
        'today_menu': today_menu,
    }
    return render(request, 'student/dashboard.html', context)



@student_required
def student_profile(request):
    """View personal information and hostel registration details."""
    student = request.user.student_profile
    return render(request, 'student/profile.html', {'student': student})


@student_required
def student_room(request):
    """View allocated room specifications and roommates."""
    student = request.user.student_profile
    room = student.room
    roommates = []
    if room:
        roommates = room.students.exclude(pk=student.pk)

    context = {
        'student': student,
        'room': room,
        'roommates': roommates,
    }
    return render(request, 'student/my_room.html', context)


@student_required
def submit_complaint(request):
    """Submit a hostel maintenance or service grievance."""
    student = request.user.student_profile
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = student
            complaint.save()
            messages.success(
                request,
                f"Your complaint ({complaint.complaint_id}) has been submitted successfully! The warden will review it shortly."
            )
            return redirect('my_complaints')
    else:
        form = ComplaintForm()

    return render(request, 'student/submit_complaint.html', {'form': form, 'student': student})


@student_required
def my_complaints(request):
    """View history of submitted complaints with real-time status and warden responses."""
    student = request.user.student_profile
    status_filter = request.GET.get('status', '').strip()

    complaints = student.complaints.all()
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    context = {
        'complaints': complaints,
        'selected_status': status_filter,
        'student': student,
    }
    return render(request, 'student/my_complaints.html', context)


@student_required
def student_complaint_detail(request, pk):
    """View specific complaint details and admin response. Protected to author only."""
    student = request.user.student_profile
    # Guarantee that student can ONLY see their own complaint
    complaint = get_object_or_404(Complaint, pk=pk, student=student)

    return render(request, 'student/complaint_detail.html', {'complaint': complaint, 'student': student})


# ==========================================
# LEAVE & GATE PASS MANAGEMENT (ADMIN)
# ==========================================

@admin_required
def leave_list(request):
    """View, search, and filter student leave and gate pass requests."""
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    leave_type = request.GET.get('leave_type', '').strip()

    leaves = LeaveRequest.objects.select_related('student', 'student__room').all()

    if query:
        leaves = leaves.filter(
            Q(leave_id__icontains=query) |
            Q(student__name__icontains=query) |
            Q(student__student_id__icontains=query) |
            Q(destination__icontains=query) |
            Q(reason__icontains=query)
        )

    if status:
        leaves = leaves.filter(status=status)

    if leave_type:
        leaves = leaves.filter(leave_type=leave_type)

    leave_types = LeaveRequest.LEAVE_TYPE_CHOICES
    status_choices = LeaveRequest.STATUS_CHOICES

    context = {
        'leaves': leaves,
        'query': query,
        'selected_status': status,
        'selected_type': leave_type,
        'leave_types': leave_types,
        'status_choices': status_choices,
        'total_count': leaves.count(),
        'pending_count': LeaveRequest.objects.filter(status='Pending').count(),
    }
    return render(request, 'admin/leave_list.html', context)


@admin_required
def leave_detail(request, pk):
    """View leave request details, student info, and approve or reject."""
    leave = get_object_or_404(LeaveRequest.objects.select_related('student', 'student__room'), pk=pk)

    if request.method == 'POST':
        form = LeaveActionForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, f"Leave request {leave.leave_id} updated to '{leave.status}'.")
            return redirect('leave_detail', pk=leave.pk)
    else:
        form = LeaveActionForm(instance=leave)

    context = {
        'leave': leave,
        'form': form,
    }
    return render(request, 'admin/leave_detail.html', context)


# ==========================================
# LEAVE & GATE PASS (STUDENT PORTAL)
# ==========================================

@student_required
def apply_leave(request):
    """Student applies for hostel leave / gate pass."""
    student = request.user.student_profile
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = student
            leave.save()
            messages.success(
                request,
                f"Your leave request ({leave.leave_id}) has been submitted! The warden will review and approve it."
            )
            return redirect('my_leaves')
    else:
        form = LeaveRequestForm()

    return render(request, 'student/apply_leave.html', {'form': form, 'student': student})


@student_required
def my_leaves(request):
    """View student's leave requests history and gate pass status."""
    student = request.user.student_profile
    status_filter = request.GET.get('status', '').strip()

    leaves = student.leave_requests.all()
    if status_filter:
        leaves = leaves.filter(status=status_filter)

    context = {
        'leaves': leaves,
        'selected_status': status_filter,
        'student': student,
    }
    return render(request, 'student/my_leaves.html', context)


@student_required
def leave_detail_student(request, pk):
    """View leave details & printable Gate Pass (author-only protection)."""
    student = request.user.student_profile
    leave = get_object_or_404(LeaveRequest, pk=pk, student=student)

    return render(request, 'student/leave_detail.html', {'leave': leave, 'student': student})


# ==========================================
# HOSTEL MESS & FOOD MENU VIEWS
# ==========================================

@login_required
def mess_menu_view(request):
    """View weekly South Indian mess menu timetable with Wednesday & Sunday Non-Veg specials."""
    menus = MessMenu.objects.all().order_by('id')
    today_name = datetime.date.today().strftime('%A')
    today_menu = MessMenu.objects.filter(day_of_week=today_name).first()

    context = {
        'menus': menus,
        'today_name': today_name,
        'today_menu': today_menu,
    }
    return render(request, 'mess_menu.html', context)


@admin_required
def mess_menu_edit(request, pk):
    """Warden updates mess menu for a specific day."""
    menu = get_object_or_404(MessMenu, pk=pk)

    if request.method == 'POST':
        form = MessMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mess menu for {menu.day_of_week} updated successfully.")
            return redirect('mess_menu_view')
    else:
        form = MessMenuForm(instance=menu)

    context = {
        'form': form,
        'menu': menu,
    }
    return render(request, 'admin/mess_menu_edit.html', context)

