import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Student, Room, Complaint, LeaveRequest, MessMenu


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter Student ID or Admin Username',
            'autofocus': True
        }),
        label="Username / Student ID"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter Password'
        }),
        label="Password"
    )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'block', 'floor', 'room_type', 'capacity', 'availability_status']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A-101'}),
            'block': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Block A (Boys)'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is None or capacity <= 0:
            raise ValidationError("Room capacity must be at least 1.")
        
        # If updating an existing room, capacity cannot be less than currently occupied beds
        if self.instance and self.instance.pk:
            current_occupancy = self.instance.students.count()
            if capacity < current_occupancy:
                raise ValidationError(
                    f"Capacity cannot be less than current occupancy ({current_occupancy} students currently allocated)."
                )
        return capacity


class StudentForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        initial="student123",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Initial password for student login'}),
        help_text="Default initial password is 'student123'."
    )

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'department', 'year', 'gender', 'phone', 'email', 'room']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. STU101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id', '').strip()
        if not student_id:
            raise ValidationError("Student ID is required.")
        if User.objects.filter(username__iexact=student_id).exists() or Student.objects.filter(student_id__iexact=student_id).exists():
            raise ValidationError(f"A student with ID '{student_id}' already exists.")
        return student_id

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Please enter a valid 10-digit phone number.")
        return phone

    def clean_room(self):
        room = self.cleaned_data.get('room')
        if room:
            # Check room capacity
            if room.availability_status == 'Maintenance':
                raise ValidationError(f"Room {room.room_number} is under maintenance.")
            if room.students.count() >= room.capacity:
                raise ValidationError(f"Room {room.room_number} is already full ({room.capacity}/{room.capacity} beds occupied).")
        return room


class StudentEditForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep current password'}),
        help_text="Leave blank if you do not wish to change the student's password."
    )

    class Meta:
        model = Student
        fields = ['name', 'department', 'year', 'gender', 'phone', 'email', 'room']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not re.match(r'^\d{10}$', phone):
            raise ValidationError("Please enter a valid 10-digit phone number.")
        return phone

    def clean_room(self):
        room = self.cleaned_data.get('room')
        if room:
            # If changing to a new room or re-assigning
            if room != self.instance.room:
                if room.availability_status == 'Maintenance':
                    raise ValidationError(f"Room {room.room_number} is under maintenance.")
                if room.students.count() >= room.capacity:
                    raise ValidationError(f"Room {room.room_number} is full ({room.capacity}/{room.capacity} beds occupied).")
        return room


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of the issue'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed explanation of the issue...'}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject or len(subject) < 3:
            raise ValidationError("Subject must be at least 3 characters long.")
        return subject

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if not desc or len(desc) < 5:
            raise ValidationError("Please provide a detailed description (minimum 5 characters).")
        return desc


class ComplaintResponseForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'admin_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter remarks or actions taken for this complaint...'
            }),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'destination', 'emergency_contact', 'reason']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Home town / city / place of visit'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit parent or emergency phone'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Reason for leave / outing request...'}),
        }

    def clean_emergency_contact(self):
        contact = self.cleaned_data.get('emergency_contact', '').strip()
        if not re.match(r'^\d{10}$', contact):
            raise ValidationError("Please provide a valid 10-digit emergency contact phone number.")
        return contact

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            import datetime
            today = datetime.date.today()
            if start_date < today:
                self.add_error('start_date', "Departure date cannot be in the past.")
            if end_date < start_date:
                self.add_error('end_date', "Return date cannot be earlier than departure date.")
        return cleaned_data


class LeaveActionForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'warden_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'warden_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Remarks or approval notes for student & security guard (optional)...'
            }),
        }


class MessMenuForm(forms.ModelForm):
    class Meta:
        model = MessMenu
        fields = ['day_of_week', 'breakfast', 'lunch', 'evening_snacks', 'dinner', 'special_dish', 'is_non_veg_day']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'breakfast': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lunch': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'evening_snacks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'dinner': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_dish': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Chicken Biryani (Wed) / Chicken Curry (Sun)'}),
            'is_non_veg_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

