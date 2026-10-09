from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from hostel.models import Room, Student, Complaint
from hostel.forms import StudentForm, ComplaintForm, RoomForm


class HostelModelTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number="R-101",
            block="Block A",
            floor=1,
            room_type="Double",
            capacity=2,
            availability_status="Available"
        )

        self.user = User.objects.create_user(
            username="TEST001",
            password="password123",
            email="test1@hostel.edu"
        )

        self.student = Student.objects.create(
            user=self.user,
            student_id="TEST001",
            name="Test Student",
            department="MCA",
            year="1st Year",
            gender="Male",
            phone="9876543210",
            email="test1@hostel.edu",
            room=self.room
        )

    def test_room_occupancy_update(self):
        """Verify room occupancy automatically updates when a student is assigned."""
        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(self.room.availability_status, "Available")
        self.assertFalse(self.room.is_full)

        # Add second student to reach capacity
        user2 = User.objects.create_user(username="TEST002", password="password123")
        student2 = Student.objects.create(
            user=user2,
            student_id="TEST002",
            name="Second Student",
            department="CSE",
            year="1st Year",
            gender="Male",
            phone="9876543211",
            email="test2@hostel.edu",
            room=self.room
        )

        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 2)
        self.assertEqual(self.room.availability_status, "Full")
        self.assertTrue(self.room.is_full)

        # Remove student2
        student2.delete()
        self.room.refresh_from_db()
        self.assertEqual(self.room.occupied_count, 1)
        self.assertEqual(self.room.availability_status, "Available")

    def test_complaint_auto_id_generation(self):
        """Verify complaint ID is auto-generated in format CMP-XXXX."""
        complaint = Complaint.objects.create(
            student=self.student,
            category="Electrical",
            subject="Bulb fused",
            description="Tube light in room is not turning on."
        )
        self.assertIsNotNone(complaint.complaint_id)
        self.assertTrue(complaint.complaint_id.startswith("CMP-"))


class HostelViewAndAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Admin user
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="adminpassword",
            email="admin@hostel.edu"
        )

        # Student user
        self.student_user = User.objects.create_user(
            username="STU999",
            password="stupassword",
            email="stu999@hostel.edu"
        )
        self.student_profile = Student.objects.create(
            user=self.student_user,
            student_id="STU999",
            name="Alice",
            department="MCA",
            year="2nd Year",
            gender="Female",
            phone="9876543210",
            email="stu999@hostel.edu"
        )

        # Another student for privacy testing
        self.other_user = User.objects.create_user(
            username="STU888",
            password="stupassword2",
            email="stu888@hostel.edu"
        )
        self.other_profile = Student.objects.create(
            user=self.other_user,
            student_id="STU888",
            name="Bob",
            department="CSE",
            year="3rd Year",
            gender="Male",
            phone="9876543211",
            email="stu888@hostel.edu"
        )

        self.complaint = Complaint.objects.create(
            student=self.student_profile,
            category="Plumbing",
            subject="Tap leak",
            description="Water leaking from sink tap."
        )

    def test_unauthenticated_user_redirected(self):
        """Unauthenticated user accessing protected dashboards is redirected to login."""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('student_dashboard'))
        self.assertRedirects(response, reverse('login'))

    def test_student_cannot_access_admin_dashboard(self):
        """Logged-in student attempting to access admin dashboard is redirected to student dashboard."""
        self.client.login(username="STU999", password="stupassword")
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_admin_can_access_admin_dashboard(self):
        """Logged-in Admin can access admin dashboard."""
        self.client.login(username="adminuser", password="adminpassword")
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hostel Warden &amp; Admin Dashboard")

    def test_student_complaint_isolation(self):
        """Student cannot view another student's complaint details."""
        # Log in as Bob and try to access Alice's complaint
        self.client.login(username="STU888", password="stupassword2")
        response = self.client.get(reverse('student_complaint_detail', kwargs={'pk': self.complaint.pk}))
        # Should return 404 (object not found for Bob)
        self.assertEqual(response.status_code, 404)

        # Log in as Alice (author) - should succeed
        self.client.login(username="STU999", password="stupassword")
        response = self.client.get(reverse('student_complaint_detail', kwargs={'pk': self.complaint.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.complaint.subject)


class HostelFormValidationTests(TestCase):
    def test_phone_validation(self):
        """Validate that phone numbers must be exactly 10 digits."""
        form_data = {
            'student_id': 'VAL001',
            'name': 'Validation Student',
            'department': 'MCA',
            'year': '1st Year',
            'gender': 'Male',
            'phone': '12345',  # Invalid! Only 5 digits
            'email': 'valid@hostel.edu',
            'password': 'password123'
        }
        form = StudentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_empty_complaint_validation(self):
        """Validate that empty subject or description is rejected."""
        form = ComplaintForm(data={'category': 'Electrical', 'subject': '', 'description': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('description', form.errors)


class FullWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin", password="password123")
        self.room = Room.objects.create(
            room_number="T-101",
            block="Block T",
            floor=1,
            capacity=1,
            availability_status="Available"
        )
        self.student_user = User.objects.create_user(username="STU001", password="password123")
        self.student = Student.objects.create(
            user=self.student_user,
            student_id="STU001",
            name="John Doe",
            department="MCA",
            year="1st Year",
            gender="Male",
            phone="9876543210",
            email="john@example.com",
            room=self.room
        )

    def test_admin_views_render(self):
        self.client.login(username="admin", password="password123")
        # List of admin urls to test
        urls = [
            reverse('admin_dashboard'),
            reverse('student_list'),
            reverse('student_create'),
            reverse('student_detail', kwargs={'pk': self.student.pk}),
            reverse('student_edit', kwargs={'pk': self.student.pk}),
            reverse('room_list'),
            reverse('room_create'),
            reverse('room_detail', kwargs={'pk': self.room.pk}),
            reverse('room_edit', kwargs={'pk': self.room.pk}),
            reverse('complaint_list'),
            reverse('hostel_stats'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed at {url}")

    def test_student_views_render(self):
        self.client.login(username="STU001", password="password123")
        urls = [
            reverse('student_dashboard'),
            reverse('student_profile'),
            reverse('student_room'),
            reverse('submit_complaint'),
            reverse('my_complaints'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed at {url}")

    def test_student_submit_complaint_flow(self):
        self.client.login(username="STU001", password="password123")
        response = self.client.post(reverse('submit_complaint'), {
            'category': 'Plumbing',
            'subject': 'Pipe leakage',
            'description': 'Water leaking in washroom.'
        })
        self.assertRedirects(response, reverse('my_complaints'))
        complaint = Complaint.objects.filter(student=self.student).first()
        self.assertIsNotNone(complaint)
        self.assertEqual(complaint.subject, 'Pipe leakage')
        self.assertEqual(complaint.status, 'Pending')

    def test_admin_update_complaint_flow(self):
        complaint = Complaint.objects.create(
            student=self.student,
            category='Internet',
            subject='No signal',
            description='Wi-Fi router down.'
        )
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('complaint_detail', kwargs={'pk': complaint.pk}), {
            'status': 'Resolved',
            'admin_response': 'Router rebooted and firmware updated.'
        })
        self.assertRedirects(response, reverse('complaint_detail', kwargs={'pk': complaint.pk}))
        complaint.refresh_from_db()
        self.assertEqual(complaint.status, 'Resolved')
        self.assertEqual(complaint.admin_response, 'Router rebooted and firmware updated.')

    def test_mess_menu_view_renders(self):
        self.client.login(username="STU001", password="password123")
        response = self.client.get(reverse('mess_menu_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weekly Hostel Mess")

    def test_student_apply_leave_and_gate_pass_flow(self):
        import datetime
        self.client.login(username="STU001", password="password123")
        today = datetime.date.today()
        response = self.client.post(reverse('apply_leave'), {
            'leave_type': 'Home Leave',
            'start_date': today,
            'end_date': today + datetime.timedelta(days=2),
            'destination': 'Coimbatore',
            'emergency_contact': '9876543210',
            'reason': 'Family function'
        })
        self.assertRedirects(response, reverse('my_leaves'))
        from hostel.models import LeaveRequest
        leave = LeaveRequest.objects.filter(student=self.student).first()
        self.assertIsNotNone(leave)
        self.assertEqual(leave.status, 'Pending')

        # Admin approves the leave
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('leave_detail', kwargs={'pk': leave.pk}), {
            'status': 'Approved',
            'warden_remarks': 'Approved by Chief Warden'
        })
        self.assertRedirects(response, reverse('leave_detail', kwargs={'pk': leave.pk}))
        leave.refresh_from_db()
        self.assertEqual(leave.status, 'Approved')

        # Student views gate pass
        self.client.login(username="STU001", password="password123")
        response = self.client.get(reverse('leave_detail_student', kwargs={'pk': leave.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Official Digital Gate Pass")


