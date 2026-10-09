from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hostel.models import Room, Student, Complaint


class Command(BaseCommand):
    help = "Populate database with sample rooms, students, complaints, and admin users for testing/demo."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Populating sample data for Hostel Management System..."))

        # 1. Create Superuser / Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hostel.edu', 'admin123', first_name="System", last_name="Administrator")
            self.stdout.write(self.style.SUCCESS("Created Admin: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Create Warden User
        if not User.objects.filter(username='warden').exists():
            warden = User.objects.create_user('warden', 'warden@hostel.edu', 'warden123', first_name="Chief", last_name="Warden")
            warden.is_staff = True
            warden.save()
            self.stdout.write(self.style.SUCCESS("Created Warden: warden / warden123"))
        else:
            self.stdout.write("Warden user already exists.")

        # 3. Create Sample Rooms
        rooms_data = [
            {'room_number': 'A-101', 'block': 'Block A (Boys)', 'floor': 1, 'room_type': 'Single', 'capacity': 1, 'availability_status': 'Available'},
            {'room_number': 'A-102', 'block': 'Block A (Boys)', 'floor': 1, 'room_type': 'Double', 'capacity': 2, 'availability_status': 'Available'},
            {'room_number': 'A-201', 'block': 'Block A (Boys)', 'floor': 2, 'room_type': 'Triple', 'capacity': 3, 'availability_status': 'Available'},
            {'room_number': 'A-202', 'block': 'Block A (Boys)', 'floor': 2, 'room_type': 'Four-Bed', 'capacity': 4, 'availability_status': 'Available'},
            {'room_number': 'B-101', 'block': 'Block B (Girls)', 'floor': 1, 'room_type': 'Single', 'capacity': 1, 'availability_status': 'Available'},
            {'room_number': 'B-102', 'block': 'Block B (Girls)', 'floor': 1, 'room_type': 'Double', 'capacity': 2, 'availability_status': 'Available'},
            {'room_number': 'B-201', 'block': 'Block B (Girls)', 'floor': 2, 'room_type': 'Triple', 'capacity': 3, 'availability_status': 'Available'},
            {'room_number': 'B-202', 'block': 'Block B (Girls)', 'floor': 2, 'room_type': 'AC-Double', 'capacity': 2, 'availability_status': 'Maintenance'},
        ]

        created_rooms = {}
        for r_info in rooms_data:
            room, _ = Room.objects.get_or_create(
                room_number=r_info['room_number'],
                defaults=r_info
            )
            created_rooms[room.room_number] = room

        self.stdout.write(self.style.SUCCESS(f"Configured {len(created_rooms)} rooms."))

        # 4. Create Sample Students
        students_data = [
            {
                'id': 'STU001', 'name': 'Rahul Sharma', 'dept': 'MCA', 'year': '1st Year',
                'gender': 'Male', 'phone': '9876543210', 'email': 'rahul.mca@hostel.edu',
                'room': 'A-102'
            },
            {
                'id': 'STU002', 'name': 'Amit Verma', 'dept': 'MCA', 'year': '1st Year',
                'gender': 'Male', 'phone': '9876543211', 'email': 'amit.mca@hostel.edu',
                'room': 'A-102'
            },
            {
                'id': 'STU003', 'name': 'Priya Patel', 'dept': 'CSE', 'year': '2nd Year',
                'gender': 'Female', 'phone': '9876543212', 'email': 'priya.cse@hostel.edu',
                'room': 'B-102'
            },
            {
                'id': 'STU004', 'name': 'Sneha Nair', 'dept': 'IT', 'year': '3rd Year',
                'gender': 'Female', 'phone': '9876543213', 'email': 'sneha.it@hostel.edu',
                'room': 'B-102'
            },
            {
                'id': 'STU005', 'name': 'Rohan Gupta', 'dept': 'ECE', 'year': '2nd Year',
                'gender': 'Male', 'phone': '9876543214', 'email': 'rohan.ece@hostel.edu',
                'room': 'A-201'
            },
            {
                'id': 'STU006', 'name': 'Vicky Kumar', 'dept': 'MECH', 'year': '4th Year',
                'gender': 'Male', 'phone': '9876543215', 'email': 'vicky.mech@hostel.edu',
                'room': 'A-201'
            },
            {
                'id': 'STU007', 'name': 'Ananya Singh', 'dept': 'CSE', 'year': '1st Year',
                'gender': 'Female', 'phone': '9876543216', 'email': 'ananya.cse@hostel.edu',
                'room': 'B-201'
            },
            {
                'id': 'STU008', 'name': 'Karthik Reddy', 'dept': 'MCA', 'year': '2nd Year',
                'gender': 'Male', 'phone': '9876543217', 'email': 'karthik.mca@hostel.edu',
                'room': None
            },
        ]

        created_students = {}
        for s_data in students_data:
            stu_id = s_data['id']
            # Create user if not exists
            user = User.objects.filter(username=stu_id).first()
            if not user:
                user = User.objects.create_user(
                    username=stu_id,
                    email=s_data['email'],
                    password='student123',
                    first_name=s_data['name']
                )

            # Assign room
            assigned_room = created_rooms.get(s_data['room']) if s_data['room'] else None

            # Create or update student profile
            student, _ = Student.objects.update_or_create(
                student_id=stu_id,
                defaults={
                    'user': user,
                    'name': s_data['name'],
                    'department': s_data['dept'],
                    'year': s_data['year'],
                    'gender': s_data['gender'],
                    'phone': s_data['phone'],
                    'email': s_data['email'],
                    'room': assigned_room,
                }
            )
            created_students[stu_id] = student

        self.stdout.write(self.style.SUCCESS(f"Configured {len(created_students)} students."))

        # 5. Create Sample Complaints
        complaints_data = [
            {
                'id': 'CMP-0001',
                'student_id': 'STU001',
                'category': 'Electrical',
                'subject': 'Ceiling fan makes humming noise and rotates slowly',
                'description': 'The ceiling fan in Room A-102 produces an abnormal clicking noise at speed 3 and doesn\'t cool properly.',
                'status': 'In Progress',
                'admin_response': 'Technician assigned. Electrician will visit Room A-102 today at 3:00 PM.'
            },
            {
                'id': 'CMP-0002',
                'student_id': 'STU003',
                'category': 'Plumbing',
                'subject': 'Bathroom tap continuously dripping in Block B',
                'description': 'The faucet in our attached washroom has a leaky washer causing steady water wastage throughout the night.',
                'status': 'Resolved',
                'admin_response': 'Plumbing maintenance staff inspected the tap and replaced the damaged rubber washer. Issue resolved.'
            },
            {
                'id': 'CMP-0003',
                'student_id': 'STU002',
                'category': 'Internet',
                'subject': 'Hostel Wi-Fi access point disconnections',
                'description': 'Wi-Fi connection keeps dropping every 15 minutes during evening study hours (7 PM to 10 PM).',
                'status': 'Pending',
                'admin_response': ''
            },
            {
                'id': 'CMP-0004',
                'student_id': 'STU004',
                'category': 'Cleaning',
                'subject': 'Corridor and staircase cleaning request',
                'description': 'First floor corridor in Block B needs sweeping and trash bins need clearance.',
                'status': 'Resolved',
                'admin_response': 'Housekeeping supervisor has dispatched cleaning crew. Waste bin cleared.'
            },
            {
                'id': 'CMP-0005',
                'student_id': 'STU005',
                'category': 'Water',
                'subject': 'Water cooler on 2nd floor not dispensing chilled water',
                'description': 'The drinking water cooler near Room A-201 cooling compressor appears to have stopped working.',
                'status': 'Pending',
                'admin_response': ''
            }
        ]

        for c_data in complaints_data:
            stu = created_students.get(c_data['student_id'])
            if stu:
                Complaint.objects.update_or_create(
                    complaint_id=c_data['id'],
                    defaults={
                        'student': stu,
                        'category': c_data['category'],
                        'subject': c_data['subject'],
                        'description': c_data['description'],
                        'status': c_data['status'],
                        'admin_response': c_data['admin_response']
                    }
                )

        # 6. Update all room occupancies
        for room in Room.objects.all():
            room.update_occupancy()

        # 7. Create South Indian Weekly Mess Menu
        import datetime
        from hostel.models import LeaveRequest, MessMenu

        mess_menu_data = [
            {
                'day_of_week': 'Monday',
                'breakfast': 'Soft Idli (4 pcs), Medu Vada (1 pc), Piping Hot Sambar, Coconut Chutney, Filter Coffee / Tea',
                'lunch': 'Traditional South Indian Meals: Steamed Ponni Rice, Murungakkai Sambar, Tomato Rasam, Beans Poriyal, Curd, Crisp Appalam',
                'evening_snacks': 'Filter Coffee / Tea with Hot Medu Vada (1 pc)',
                'dinner': 'Soft Phulka / Chapati, Dal Tadka, Steamed Rice, Pepper Rasam, Fresh Buttermilk',
                'special_dish': '',
                'is_non_veg_day': False,
            },
            {
                'day_of_week': 'Tuesday',
                'breakfast': 'Rava Kichadi / Upma, Sambar, Roasted Gram Chutney, Filter Coffee / Tea',
                'lunch': 'Steamed Rice, Vendakkai Mor Kulambu (Buttermilk Gravy), Garlic Rasam, Crispy Potato Roast, Curd, Papad',
                'evening_snacks': 'Filter Coffee / Tea with Onion / Potato Bajji',
                'dinner': 'South Indian Ghee Roast Dosa, Tomato Onion Chutney, Sambar, Steamed Rice, Rasam, Milk',
                'special_dish': '',
                'is_non_veg_day': False,
            },
            {
                'day_of_week': 'Wednesday',
                'breakfast': 'Ven Pongal with Ghee & Cashews, Medu Vada, Sambar, Coconut Chutney, Filter Coffee / Tea',
                'lunch': '🍗 WEDNESDAY SPECIAL NON-VEG: Flavourful Chicken Biryani, Boiled Egg, Onion Raitha, Ennai Kathirikai Salna (Veg Alternative: Paneer Dum Biryani) + Steamed White Rice, Tomato Rasam',
                'evening_snacks': 'Filter Coffee / Tea with Hot Crispy Onion Pakoda',
                'dinner': 'Soft Chapati (3 pcs), Vegetable Salna, Steamed Rice, Jeera Rasam, Chilled Buttermilk',
                'special_dish': '🍗 Chicken Biryani & Onion Raitha (Wed Lunch)',
                'is_non_veg_day': True,
            },
            {
                'day_of_week': 'Thursday',
                'breakfast': 'Crispy Plain / Masala Dosa, Vegetable Sambar, Mint Coriander Chutney, Filter Coffee / Tea',
                'lunch': 'Steamed Rice, Sundakkai Vatha Kulambu, Pepper Rasam, Cabbage & Chana Dal Poriyal, Curd, Fried Appalam',
                'evening_snacks': 'Filter Coffee / Tea with Masala Vada',
                'dinner': 'Idiyappam with Coconut Milk / Vegetable Kurma, Steamed Rice, Tomato Rasam, Milk',
                'special_dish': '',
                'is_non_veg_day': False,
            },
            {
                'day_of_week': 'Friday',
                'breakfast': 'Poori Masala (3 pcs), Potato Sagoo, Coconut Chutney, Filter Coffee / Tea',
                'lunch': 'South Indian Festival Meals: Steamed Rice, Paruppu & Ghee, Mixed Veg Sambar, Pineapple Rasam, Aviyal, Curd, Payasam (Sweet), Appalam',
                'evening_snacks': 'Filter Coffee / Tea with Navadhanya Sundal',
                'dinner': 'Soft Chapati, Paneer Butter Masala, Steamed Rice, Rasam, Fresh Buttermilk',
                'special_dish': 'Special Friday Payasam (Sweet)',
                'is_non_veg_day': False,
            },
            {
                'day_of_week': 'Saturday',
                'breakfast': 'Semiya Upma / Rava Dosa, Tomato Chutney, Sambar, Filter Coffee / Tea',
                'lunch': 'South Indian Variety Rice: Lemon Rice, Curd Rice with Pomegranate, Spicy Potato Fry, Pickle, Appalam',
                'evening_snacks': 'Filter Coffee / Tea with Veg Samosa',
                'dinner': 'Soft Uthappam with Sambar & Kara Chutney, Steamed Rice, Rasam, Milk',
                'special_dish': '',
                'is_non_veg_day': False,
            },
            {
                'day_of_week': 'Sunday',
                'breakfast': 'Crispy Kal Dosa, Tiffin Sambar, Peanut Chutney, Filter Coffee / Tea',
                'lunch': '🍗 SUNDAY SPECIAL NON-VEG: Spicy Chettinad Chicken Curry, Boiled Egg, Steamed Ponni Rice, Pepper Jeera Rasam, Thick Curd (Veg Alternative: Mushroom Chettinad Gravy)',
                'evening_snacks': 'Filter Coffee / Tea with Sweet Biscuit / Mixture',
                'dinner': 'Soft Chapati, Mixed Vegetable Kurma, Steamed Rice, Rasam, Warm Sweet Milk',
                'special_dish': '🍗 Chettinad Chicken Curry & Egg (Sun Lunch)',
                'is_non_veg_day': True,
            },
        ]

        for m_data in mess_menu_data:
            MessMenu.objects.update_or_create(
                day_of_week=m_data['day_of_week'],
                defaults=m_data
            )
        self.stdout.write(self.style.SUCCESS("Configured South Indian 7-day weekly mess menu with Wed & Sun Non-Veg specials."))

        # 8. Create Sample Leave Requests
        today = datetime.date.today()
        stu1 = created_students.get('STU001')
        stu3 = created_students.get('STU003')

        if stu1:
            LeaveRequest.objects.update_or_create(
                leave_id='LEV-0001',
                defaults={
                    'student': stu1,
                    'leave_type': 'Home Leave',
                    'start_date': today + datetime.timedelta(days=1),
                    'end_date': today + datetime.timedelta(days=4),
                    'destination': 'Chennai, Tamil Nadu (Home Visit)',
                    'emergency_contact': '9876543210',
                    'reason': 'Visiting parents for family festival function.',
                    'status': 'Approved',
                    'warden_remarks': 'Parent verified over phone call. Gate pass authorized for exit.'
                }
            )

        if stu3:
            LeaveRequest.objects.update_or_create(
                leave_id='LEV-0002',
                defaults={
                    'student': stu3,
                    'leave_type': 'Day Outing',
                    'start_date': today,
                    'end_date': today,
                    'destination': 'Central City Library & Book Fair',
                    'emergency_contact': '9876543212',
                    'reason': 'Visiting university library to collect research project reference materials.',
                    'status': 'Pending',
                    'warden_remarks': ''
                }
            )
        self.stdout.write(self.style.SUCCESS("Configured sample student leave requests and approved gate pass."))

        self.stdout.write(self.style.SUCCESS("All sample data populated successfully!"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("Admin login:    admin    / admin123"))
        self.stdout.write(self.style.SUCCESS("Warden login:   warden   / warden123"))
        self.stdout.write(self.style.SUCCESS("Student login:  STU001   / student123 (Rahul Sharma - Gate Pass Ready!)"))
        self.stdout.write(self.style.SUCCESS("Student login:  STU003   / student123 (Priya Patel)"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

