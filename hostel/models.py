from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single Bed'),
        ('Double', 'Double Sharing'),
        ('Triple', 'Triple Sharing'),
        ('Four-Bed', 'Four Bed Sharing'),
        ('AC-Single', 'AC Single Room'),
        ('AC-Double', 'AC Double Sharing'),
        ('Deluxe', 'Deluxe Room'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Maintenance', 'Under Maintenance'),
    ]

    room_number = models.CharField(max_length=20, unique=True, help_text="e.g., A-101, B-204")
    block = models.CharField(max_length=50, help_text="e.g., A Block, B Block, Girls Wing")
    floor = models.IntegerField(default=1, help_text="Floor number (e.g., 1, 2, 3)")
    room_type = models.CharField(max_length=30, choices=ROOM_TYPE_CHOICES, default='Double')
    capacity = models.PositiveIntegerField(default=2, help_text="Maximum number of students")
    occupied_count = models.PositiveIntegerField(default=0, help_text="Current number of occupants")
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"Room {self.room_number} ({self.block} - Floor {self.floor}) [{self.occupied_count}/{self.capacity}]"

    def update_occupancy(self):
        """Update occupied count and availability status based on current students."""
        count = self.students.count()
        self.occupied_count = count
        if self.availability_status != 'Maintenance':
            if count >= self.capacity:
                self.availability_status = 'Full'
            else:
                self.availability_status = 'Available'
        self.save(update_fields=['occupied_count', 'availability_status', 'updated_at'])

    @property
    def is_full(self):
        return self.occupied_count >= self.capacity

    @property
    def available_beds(self):
        return max(0, self.capacity - self.occupied_count)

    @property
    def occupancy_percentage(self):
        if self.capacity == 0:
            return 0
        return int((self.occupied_count / self.capacity) * 100)


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]

    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('MCA', 'Master of Computer Applications'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('MBA', 'Master of Business Administration'),
        ('OTHER', 'Other Department'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits without country code or spaces."
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique Student ID / Roll Number")
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='MCA')
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default='1st Year')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    phone = models.CharField(validators=[phone_regex], max_length=10)
    email = models.EmailField()
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="Assigned room"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def save(self, *args, **kwargs):
        # Track old room if instance already exists in database
        old_room = None
        if self.pk:
            old_instance = Student.objects.filter(pk=self.pk).first()
            if old_instance:
                old_room = old_instance.room

        super().save(*args, **kwargs)

        # Update occupancy for both old and new room if room changed
        if old_room and old_room != self.room:
            old_room.update_occupancy()
        if self.room:
            self.room.update_occupancy()

    def delete(self, *args, **kwargs):
        assigned_room = self.room
        user_account = self.user
        super().delete(*args, **kwargs)
        if assigned_room:
            assigned_room.update_occupancy()
        if user_account:
            user_account.delete()


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Cleaning', 'Cleaning'),
        ('Food', 'Food / Mess'),
        ('Water', 'Water Supply'),
        ('Internet', 'Internet / Wi-Fi'),
        ('Room', 'Room Maintenance'),
        ('Other', 'Other Issue'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    complaint_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_response = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.complaint_id or 'Complaint'} - {self.subject} ({self.status})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.complaint_id:
            self.complaint_id = f"CMP-{self.id:04d}"
            Complaint.objects.filter(pk=self.pk).update(complaint_id=self.complaint_id)


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Home Leave', 'Home Leave / Vacation'),
        ('Day Outing', 'Day Outing / Local Visit'),
        ('Emergency', 'Emergency / Medical Leave'),
        ('Academic', 'Academic / Project / Conference'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    leave_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE_CHOICES, default='Home Leave')
    start_date = models.DateField(help_text="Departure / Start Date")
    end_date = models.DateField(help_text="Return / End Date")
    destination = models.CharField(max_length=200, help_text="Destination address / city")
    emergency_contact = models.CharField(
        max_length=10,
        validators=[Student.phone_regex],
        help_text="Parent or emergency contact number (10 digits)"
    )
    reason = models.TextField(help_text="Reason for leave or gate pass")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    warden_remarks = models.TextField(blank=True, null=True, help_text="Warden remarks or gate instructions")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.leave_id or 'Leave'} - {self.student.name} ({self.leave_type}) [{self.status}]"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.leave_id:
            self.leave_id = f"LEV-{self.id:04d}"
            LeaveRequest.objects.filter(pk=self.pk).update(leave_id=self.leave_id)


class MessMenu(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day_of_week = models.CharField(max_length=15, choices=DAY_CHOICES, unique=True)
    breakfast = models.TextField(help_text="South Indian Breakfast (e.g., Idli, Sambar, Chutney, Coffee)")
    lunch = models.TextField(help_text="Lunch (e.g., Rice, Sambar, Rasam, Poriyal, Curd, Appalam)")
    evening_snacks = models.TextField(help_text="Evening Snacks & Beverages (e.g., Tea/Coffee, Medu Vada)")
    dinner = models.TextField(help_text="Dinner (e.g., Chapati, Kurma, Steamed Rice, Rasam, Buttermilk)")
    special_dish = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Highlight special dishes, e.g. Chicken Biryani / Chicken Curry"
    )
    is_non_veg_day = models.BooleanField(
        default=False,
        help_text="Check if this day features Non-Veg specials (e.g., Wednesday Lunch, Sunday Lunch)"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        non_veg = " [Non-Veg Special]" if self.is_non_veg_day else ""
        return f"{self.day_of_week} Menu{non_veg}"

