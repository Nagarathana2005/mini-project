import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    NAVY = RGBColor(30, 58, 138)       # #1E3A8A - Deep Academic Navy
    BLUE = RGBColor(2, 132, 199)       # #0284C7 - Accent Ocean Blue
    DARK = RGBColor(15, 23, 42)        # #0F172A - Text Main
    MUTED = RGBColor(100, 116, 139)    # #64748B - Muted Text
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC - Light Card Fill
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(22, 163, 74)      # Success
    AMBER = RGBColor(217, 119, 6)      # Warning
    BORDER_COL = RGBColor(226, 232, 240)

    blank_layout = prs.slide_layouts[6] # Blank slide layout

    def add_header(slide, title_text, category_text="MCA 2ND PROJECT REVIEW"):
        # Header background banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = NAVY
        header_shape.line.fill.background()

        # Accent line under header
        line_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        line_shape.fill.solid()
        line_shape.fill.fore_color.rgb = BLUE
        line_shape.line.fill.background()

        # Category text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(186, 230, 253)
        p_cat.font.name = 'Segoe UI'

        # Main Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = 'Segoe UI'

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.35))
        tf_foot = footer_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Hostel Management System  |  MCA Project Review II  |  Django & SQLite"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = MUTED
        p_foot.font.name = 'Segoe UI'

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Decorative accent card
    decor = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(5.7))
    decor.fill.solid()
    decor.fill.fore_color.rgb = RGBColor(23, 37, 84)
    decor.line.color.rgb = RGBColor(59, 130, 246)
    decor.line.width = Pt(1.5)

    # Title badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(4.5), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = BLUE
    badge.line.fill.background()
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "MASTER OF COMPUTER APPLICATIONS (MCA)"
    p_b.alignment = PP_ALIGN.CENTER
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = WHITE

    # Project Title
    t_box = slide1.shapes.add_textbox(Inches(1.3), Inches(1.9), Inches(10.7), Inches(1.2))
    tf_t = t_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "HOSTEL MANAGEMENT SYSTEM"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE
    p_t.font.name = 'Segoe UI'

    # Subtitle
    sub_box = slide1.shapes.add_textbox(Inches(1.3), Inches(3.0), Inches(10.7), Inches(0.7))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Project Review - II: Implementation Architecture, Core Modules & System Demonstration"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(191, 219, 254)
    p_sub.font.name = 'Segoe UI'

    # Divider
    div = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(3.8), Inches(10.7), Inches(0.04))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(59, 130, 246)
    div.line.fill.background()

    # Meta info (2 columns)
    meta_box1 = slide1.shapes.add_textbox(Inches(1.3), Inches(4.1), Inches(5.0), Inches(2.2))
    tf_m1 = meta_box1.text_frame
    p_m1_1 = tf_m1.paragraphs[0]
    p_m1_1.text = "PRESENTED BY:"
    p_m1_1.font.size = Pt(11)
    p_m1_1.font.bold = True
    p_m1_1.font.color.rgb = RGBColor(147, 197, 253)
    p_m1_2 = tf_m1.add_paragraph()
    p_m1_2.text = "Student Name: [Candidate Name]\nRoll / Reg No: [Student Roll Number]\nDepartment: Master of Computer Applications\nAcademic Year: 2025 - 2026"
    p_m1_2.font.size = Pt(13)
    p_m1_2.font.color.rgb = WHITE

    meta_box2 = slide1.shapes.add_textbox(Inches(6.8), Inches(4.1), Inches(5.2), Inches(2.2))
    tf_m2 = meta_box2.text_frame
    p_m2_1 = tf_m2.paragraphs[0]
    p_m2_1.text = "PROJECT GUIDANCE & TECH STACK:"
    p_m2_1.font.size = Pt(11)
    p_m2_1.font.bold = True
    p_m2_1.font.color.rgb = RGBColor(147, 197, 253)
    p_m2_2 = tf_m2.add_paragraph()
    p_m2_2.text = "Project Guide: [Faculty Supervisor Name]\nBackend Engine: Python 3 & Django 6.1 (MVT)\nDatabase: SQLite3 Relational Engine\nUser Interface: HTML5, CSS3, Bootstrap 5.3"
    p_m2_2.font.size = Pt(13)
    p_m2_2.font.color.rgb = WHITE

    # ==========================================
    # SLIDE 2: PROJECT OVERVIEW & PROBLEM STATEMENT
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Project Overview & Problem Statement", "PROJECT BACKGROUND")

    # Left Card: Traditional System Challenges
    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card1.fill.solid()
    card1.fill.fore_color.rgb = WHITE
    card1.line.color.rgb = BORDER_COL

    header_c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(0.7))
    header_c1.fill.solid()
    header_c1.fill.fore_color.rgb = RGBColor(254, 242, 242)
    header_c1.line.fill.background()
    p1 = header_c1.text_frame.paragraphs[0]
    p1.text = "❌  Existing Challenges (Manual System)"
    p1.font.bold = True
    p1.font.size = Pt(14)
    p1.font.color.rgb = RGBColor(153, 27, 27)

    box_c1 = slide2.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(5.2), Inches(4.2))
    tf1 = box_c1.text_frame
    tf1.word_wrap = True
    points1 = [
        "Manual Paper Logbooks: Room allocations and student registers are maintained manually, leading to data loss and wear.",
        "Zero Real-Time Occupancy Visibility: Wardens struggle to know exact vacant beds, causing delays in student check-ins.",
        "Unmonitored Student Complaints: Maintenance issues (electrical, plumbing, Wi-Fi) get forgotten or lost in physical complaint registers.",
        "Over-allocation Errors: Risk of accidentally allotting students beyond certified room bed capacity.",
        "Privacy & Access Insecurity: Physical records can be viewed by unauthorized persons without verification."
    ]
    for i, pt in enumerate(points1):
        p = tf1.paragraphs[0] if i == 0 else tf1.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK
        p.space_after = Pt(10)

    # Right Card: Proposed Automated Solution
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = WHITE
    card2.line.color.rgb = BORDER_COL

    header_c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(0.7))
    header_c2.fill.solid()
    header_c2.fill.fore_color.rgb = RGBColor(240, 253, 244)
    header_c2.line.fill.background()
    p2 = header_c2.text_frame.paragraphs[0]
    p2.text = "✅  Proposed Solution (Hostel Management System)"
    p2.font.bold = True
    p2.font.size = Pt(14)
    p2.font.color.rgb = GREEN

    box_c2 = slide2.shapes.add_textbox(Inches(7.1), Inches(2.3), Inches(5.2), Inches(4.2))
    tf2 = box_c2.text_frame
    tf2.word_wrap = True
    points2 = [
        "Role-Based Secure Portals: Dedicated dashboards for Warden/Admin and Students with custom authentication decorators.",
        "Automated Bed Capacity Engine: Real-time calculation of vacant beds, visual progress bars, and strict overbooking prevention.",
        "End-to-End Grievance Tracking: Online complaint submission with category classification, live status, and official warden remarks.",
        "Search & Multi-Filtering: Instant retrieval of student records by Department, Year, Gender, and Room Allocation.",
        "Transparent Roommate Directory: Students can view assigned room amenities and verify fellow occupants seamlessly."
    ]
    for i, pt in enumerate(points2):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = DARK
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 3: WORK DONE SINCE REVIEW 1 (PROGRESS REVIEW)
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Review 1 Feedback & Work Completed (Review 2 Milestone)", "PROGRESS TRACKING")

    cards_data = [
        ("Review 1 Objective", "Planning & Database Architecture", [
            "Finalized database entity schemas (Room, Student, Complaint).",
            "Defined One-to-One and Foreign Key relationships with Django User.",
            "Established UI layout wireframes and accessibility standards."
        ], RGBColor(30, 58, 138)),
        ("Review 2 Milestone (Achieved)", "Complete Backend & Validation Engine", [
            "Implemented Django Models, Forms, and Views.",
            "Built automated room occupancy calculation & constraint checks.",
            "Created role-based security decorators (@admin_required, @student_required).",
            "Implemented 10-digit phone regex and unique ID validators."
        ], GREEN),
        ("Review 2 Milestone (Achieved)", "Responsive Frontend & UX Implementation", [
            "Clean Bootstrap 5 responsive UI across desktop and mobile.",
            "Custom CSS design with modern stat cards and status badges.",
            "Warden control center: Student CRUD, Room Allocation, Complaint actions.",
            "Student portal: Profile view, Room details, and Complaint tracker."
        ], BLUE),
        ("Verification & Testing", "Automated Testing & Demo Seeding", [
            "Constructed 12 comprehensive unit and integration tests.",
            "Achieved 100% test pass rate with 0 errors / 0 failures.",
            "Built 'python manage.py seed_data' for instant demo evaluation.",
            "Created 1-click Windows launcher (RUN_SERVER.bat)."
        ], AMBER)
    ]

    for idx, (badge_txt, title_txt, items, border_c) in enumerate(cards_data):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.5 + (idx // 2) * 2.7)
        c_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.45))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = WHITE
        c_shape.line.color.rgb = border_c
        c_shape.line.width = Pt(1.5)

        tb = slide3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.2), Inches(2.15))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_badge = tf.paragraphs[0]
        p_badge.text = badge_txt.upper()
        p_badge.font.size = Pt(9)
        p_badge.font.bold = True
        p_badge.font.color.rgb = border_c
        
        p_title = tf.add_paragraph()
        p_title.text = title_txt
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK
        p_title.space_after = Pt(4)

        for item in items:
            p_it = tf.add_paragraph()
            p_it.text = "✓ " + item
            p_it.font.size = Pt(10.5)
            p_it.font.color.rgb = DARK

    # ==========================================
    # SLIDE 4: SYSTEM ARCHITECTURE & TECH STACK
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. System Architecture & Technology Stack", "TECHNICAL SPECIFICATIONS")

    # Left: Architecture Flow Chart
    arch_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.2))
    arch_box.fill.solid()
    arch_box.fill.fore_color.rgb = WHITE
    arch_box.line.color.rgb = BORDER_COL

    header_arch = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(6.8), Inches(0.6))
    header_arch.fill.solid()
    header_arch.fill.fore_color.rgb = NAVY
    header_arch.line.fill.background()
    p_ha = header_arch.text_frame.paragraphs[0]
    p_ha.text = "Django MVT (Model - View - Template) Architecture"
    p_ha.font.bold = True
    p_ha.font.size = Pt(13)
    p_ha.font.color.rgb = WHITE

    # Diagram items inside left card
    layers = [
        ("1. Presentation Layer (Template)", "HTML5 + Bootstrap 5.3 + Responsive CSS", "Renders responsive dashboard cards, filters, tables, modals, & notification alerts."),
        ("2. Security & Routing Layer (URL / Decorators)", "urls.py + @admin_required + @student_required", "Directs traffic; enforces strict role isolation & prevents unauthorized URL browsing."),
        ("3. Controller / Business Logic Layer (View)", "views.py + forms.py (Form Validations)", "Coordinates requests, processes CRUD logic, evaluates capacity, & generates responses."),
        ("4. Data Persistence Layer (Model)", "models.py + SQLite Relational Database", "Maintains ACID compliance, relational integrity, auto-occupancy signals, & querysets.")
    ]
    for idx, (title, sub, desc) in enumerate(layers):
        ly = Inches(2.25 + idx * 1.05)
        layer_shape = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), ly, Inches(6.2), Inches(0.95))
        layer_shape.fill.solid()
        layer_shape.fill.fore_color.rgb = LIGHT_BG
        layer_shape.line.color.rgb = RGBColor(203, 213, 225)
        
        tb = slide4.shapes.add_textbox(Inches(1.2), ly + Inches(0.05), Inches(6.0), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title + "  [" + sub + "]"
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = NAVY
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = DARK

    # Right: Technology Stack Details
    stack_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.2))
    stack_box.fill.solid()
    stack_box.fill.fore_color.rgb = WHITE
    stack_box.line.color.rgb = BORDER_COL

    header_st = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.5), Inches(4.6), Inches(0.6))
    header_st.fill.solid()
    header_st.fill.fore_color.rgb = BLUE
    header_st.line.fill.background()
    p_st = header_st.text_frame.paragraphs[0]
    p_st.text = "Technology Stack Summary"
    p_st.font.bold = True
    p_st.font.size = Pt(13)
    p_st.font.color.rgb = WHITE

    tb_st = slide4.shapes.add_textbox(Inches(8.1), Inches(2.2), Inches(4.2), Inches(4.3))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True
    stack_items = [
        ("Backend Framework", "Python 3.14 / Django 6.1", "High-level web framework offering robust ORM, authentication, and secure session management."),
        ("Database Engine", "SQLite 3", "Self-contained, serverless relational database engine ideal for zero-config academic deployment."),
        ("Frontend Styling", "Bootstrap 5.3 + Custom CSS", "Responsive grid system, accessible interactive components, and customized academic theme."),
        ("Design Rules Adherence", "Zero Bloatware", "Pure Python Django application. No React, Node.js, MongoDB, or external heavy build tools used.")
    ]
    for idx, (title, name, desc) in enumerate(stack_items):
        p1 = tf_st.paragraphs[0] if idx == 0 else tf_st.add_paragraph()
        p1.text = title + ": " + name
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = DARK
        
        p2 = tf_st.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED
        p2.space_after = Pt(8)

    # ==========================================
    # SLIDE 5: DATABASE SCHEMA & ENTITY RELATIONSHIP
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Database Design & Entity Relationships", "DATA MODEL")

    entities = [
        ("Room Entity", "Table: hostel_room", [
            "room_number (PK, Char, Unique)",
            "block (Char: Boys/Girls Wing)",
            "floor (Integer: 1, 2, 3...)",
            "room_type (Single, Double, Triple)",
            "capacity (PositiveInteger)",
            "occupied_count (PositiveInteger)",
            "availability_status (Available/Full/Maint)"
        ], NAVY),
        ("Student Entity", "Table: hostel_student", [
            "id (PK, AutoField)",
            "user_id (OneToOne -> auth_user)",
            "student_id (Char, Unique, e.g. STU001)",
            "name (Char: Student Full Name)",
            "department (Char: MCA, CSE, IT...)",
            "year (Char: 1st, 2nd, 3rd, 4th)",
            "phone (Char: 10-Digit Validated)",
            "email (EmailField)",
            "room_id (FK -> Room, Nullable)"
        ], BLUE),
        ("Complaint Entity", "Table: hostel_complaint", [
            "id (PK, AutoField)",
            "complaint_id (Char: CMP-0001)",
            "student_id (FK -> Student, Cascade)",
            "category (Electrical, Plumbing, Wi-Fi...)",
            "subject (CharField, Max 150)",
            "description (TextField)",
            "date (DateTimeField, Auto)",
            "status (Pending/In Progress/Resolved)",
            "admin_response (TextField, Nullable)"
        ], GREEN),
    ]

    for idx, (ent_name, table_name, fields, col) in enumerate(entities):
        x = Inches(0.8 + idx * 3.95)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.75), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        h = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.75), Inches(0.65))
        h.fill.solid()
        h.fill.fore_color.rgb = col
        h.line.fill.background()
        p_h = h.text_frame.paragraphs[0]
        p_h.text = ent_name + "\n" + table_name
        p_h.font.bold = True
        p_h.font.size = Pt(10)
        p_h.font.color.rgb = WHITE

        tb = slide5.shapes.add_textbox(x + Inches(0.15), Inches(2.25), Inches(3.45), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        for f_idx, fld in enumerate(fields):
            p = tf.paragraphs[0] if f_idx == 0 else tf.add_paragraph()
            p.text = "• " + fld
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK
            p.space_after = Pt(3)

    # Relationships summary bar at bottom
    rel_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.85))
    rel_box.fill.solid()
    rel_box.fill.fore_color.rgb = LIGHT_BG
    rel_box.line.color.rgb = BORDER_COL

    tb_rel = slide5.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.3), Inches(0.75))
    tf_rel = tb_rel.text_frame
    p_r1 = tf_rel.paragraphs[0]
    p_r1.text = "KEY CARDINALITIES & INTEGRITY CONSTRAINTS:"
    p_r1.font.bold = True
    p_r1.font.size = Pt(10)
    p_r1.font.color.rgb = NAVY

    p_r2 = tf_rel.add_paragraph()
    p_r2.text = "1. User ↔ Student: 1-to-1 (OneToOneField)  |  2. Room ↔ Student: 1-to-Many (ForeignKey, ON_DELETE=SET_NULL)  |  3. Student ↔ Complaint: 1-to-Many (ForeignKey, ON_DELETE=CASCADE)"
    p_r2.font.size = Pt(9.5)
    p_r2.font.color.rgb = DARK

    # ==========================================
    # SLIDE 6: CORE MODULES & FEATURES
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Core Functional Modules (Review 2 Implementation)", "SYSTEM MODULES")

    modules = [
        ("Module 1: Authentication & Access Control", [
            "Unified single login page for Admin/Warden and Students.",
            "Automatic role-detection and secure redirect to respective portals.",
            "Custom decorators (@admin_required & @student_required) prevent privilege bypass.",
            "Session-based state management with secure logout."
        ], NAVY),
        ("Module 2: Student Management", [
            "Student registration automatically provisions underlying Django User credentials.",
            "Real-time search across Student ID, Name, Phone, and Room.",
            "Multi-criteria filtering: Department (MCA, CSE, IT...), Year, and Gender.",
            "Full profile management with roommate list and complaint history."
        ], BLUE),
        ("Module 3: Room Allocation & Capacity Engine", [
            "Dynamic bed occupancy tracking (Occupied / Capacity).",
            "Automatic status switching: Available ↔ Full ↔ Maintenance.",
            "Over-allocation prevention: Validation prevents assigning students to filled rooms.",
            "Safe room unassignment and re-allocation tools."
        ], GREEN),
        ("Module 4: Grievance Redressal System", [
            "Student complaint submission with automated ID tagging (CMP-0001).",
            "Classification across 8 categories: Electrical, Plumbing, Cleaning, Food, Wi-Fi, etc.",
            "Interactive status progression: Pending → In Progress → Resolved / Rejected.",
            "Official Warden remarks directly visible on the student's dashboard."
        ], AMBER)
    ]

    for idx, (m_title, m_points, m_color) in enumerate(modules):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.5 + (idx // 2) * 2.7)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = m_color
        card.line.width = Pt(1.5)

        h = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(0.55))
        h.fill.solid()
        h.fill.fore_color.rgb = m_color
        h.line.fill.background()
        p_h = h.text_frame.paragraphs[0]
        p_h.text = m_title
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.6), Inches(5.2), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        for p_idx, pt in enumerate(m_points):
            p = tf.paragraphs[0] if p_idx == 0 else tf.add_paragraph()
            p.text = "• " + pt
            p.font.size = Pt(10)
            p.font.color.rgb = DARK
            p.space_after = Pt(2)

    # ==========================================
    # SLIDE 7: SCREENSHOTS & UI SHOWCASE - ADMIN DASHBOARD & LOGIN
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. System Demonstration: Portal Login & Admin Dashboard", "USER INTERFACE SHOWCASE")

    # Left Showcase: Login UI Representation
    box_l = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.0), Inches(5.2))
    box_l.fill.solid()
    box_l.fill.fore_color.rgb = WHITE
    box_l.line.color.rgb = BORDER_COL

    h_l = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.0), Inches(0.55))
    h_l.fill.solid()
    h_l.fill.fore_color.rgb = NAVY
    h_l.line.fill.background()
    p_hl = h_l.text_frame.paragraphs[0]
    p_hl.text = "UI View: Unified Authentication Screen"
    p_hl.font.bold = True
    p_hl.font.size = Pt(11)
    p_hl.font.color.rgb = WHITE

    # Login UI Card Mockup
    login_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(2.2), Inches(4.2), Inches(3.6))
    login_card.fill.solid()
    login_card.fill.fore_color.rgb = LIGHT_BG
    login_card.line.color.rgb = BLUE

    tb_lc = slide7.shapes.add_textbox(Inches(1.4), Inches(2.3), Inches(3.8), Inches(3.3))
    tf_lc = tb_lc.text_frame
    tf_lc.word_wrap = True
    p = tf_lc.paragraphs[0]
    p.text = "🏛 HOSTEL PORTAL LOGIN"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    items_lc = [
        "Username / Student ID: [ STU001 or admin ]",
        "Password: [ ••••••••••• ]",
        "[ Button: Secure Sign In ]",
        "Demo Credentials Assistant Box:",
        "  • Admin: admin / admin123",
        "  • Warden: warden / warden123",
        "  • Student: STU001 / student123"
    ]
    for it in items_lc:
        p = tf_lc.add_paragraph()
        p.text = it
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK

    # Text under login
    tb_l_sub = slide7.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(4.6), Inches(0.7))
    tf_l_sub = tb_l_sub.text_frame
    p = tf_l_sub.paragraphs[0]
    p.text = "✓ Single unified access point with smart role detection\n✓ Handles error feedback for invalid credentials"
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED

    # Right Showcase: Admin Dashboard
    box_r = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.1), Inches(1.5), Inches(6.433), Inches(5.2))
    box_r.fill.solid()
    box_r.fill.fore_color.rgb = WHITE
    box_r.line.color.rgb = BORDER_COL

    h_r = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.1), Inches(1.5), Inches(6.433), Inches(0.55))
    h_r.fill.solid()
    h_r.fill.fore_color.rgb = BLUE
    h_r.line.fill.background()
    p_hr = h_r.text_frame.paragraphs[0]
    p_hr.text = "UI View: Warden & Admin Control Dashboard"
    p_hr.font.bold = True
    p_hr.font.size = Pt(11)
    p_hr.font.color.rgb = WHITE

    # Stat cards mockups
    stat_boxes = [
        ("Total Students", "8 Registered", NAVY),
        ("Total Rooms", "8 Rooms (19 Beds)", BLUE),
        ("Available Rooms", "6 with Vacancies", GREEN),
        ("Occupied Rooms", "4 Active Rooms", DARK),
        ("Pending Complaints", "2 Needs Action", AMBER),
        ("Resolved Complaints", "2 Successfully Solved", GREEN)
    ]
    for idx, (title, val, c) in enumerate(stat_boxes):
        sx = Inches(6.35 + (idx % 3) * 1.95)
        sy = Inches(2.2 + (idx // 3) * 0.95)
        sc = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, Inches(1.85), Inches(0.8))
        sc.fill.solid()
        sc.fill.fore_color.rgb = LIGHT_BG
        sc.line.color.rgb = c
        sc.line.width = Pt(1.2)
        
        tb = slide7.shapes.add_textbox(sx + Inches(0.05), sy + Inches(0.05), Inches(1.75), Inches(0.7))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title.upper()
        p1.font.size = Pt(7.5)
        p1.font.bold = True
        p1.font.color.rgb = MUTED
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = c

    # Bed occupancy bar mock
    bar_bg = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.35), Inches(4.3), Inches(5.9), Inches(0.5))
    bar_bg.fill.solid()
    bar_bg.fill.fore_color.rgb = RGBColor(226, 232, 240)
    bar_bg.line.fill.background()

    bar_fill = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.35), Inches(4.3), Inches(2.7), Inches(0.5))
    bar_fill.fill.solid()
    bar_fill.fill.fore_color.rgb = NAVY
    bar_fill.line.fill.background()
    p = bar_fill.text_frame.paragraphs[0]
    p.text = "Overall Bed Occupancy: 7 / 19 Beds (36%)"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Lower summary
    tb_dash_sub = slide7.shapes.add_textbox(Inches(6.35), Inches(5.0), Inches(5.9), Inches(1.5))
    tf_dash_sub = tb_dash_sub.text_frame
    tf_dash_sub.word_wrap = True
    points_dash = [
        "✓ Real-time automated calculations of available beds across Boys and Girls blocks.",
        "✓ Live tables displaying latest submitted grievances with 1-click 'Manage' buttons.",
        "✓ Quick action controls to add students, allocate rooms, and view statistics."
    ]
    for i, pt in enumerate(points_dash):
        p = tf_dash_sub.paragraphs[0] if i == 0 else tf_dash_sub.add_paragraph()
        p.text = pt
        p.font.size = Pt(10)
        p.font.color.rgb = DARK
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 8: SCREENSHOTS & UI SHOWCASE - ROOMS & STUDENT MANAGEMENT
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. System Demonstration: Room Allotment & Student Directory", "USER INTERFACE SHOWCASE")

    # Left: Room Management Showcase
    box_rm = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    box_rm.fill.solid()
    box_rm.fill.fore_color.rgb = WHITE
    box_rm.line.color.rgb = BORDER_COL

    h_rm = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(0.55))
    h_rm.fill.solid()
    h_rm.fill.fore_color.rgb = NAVY
    h_rm.line.fill.background()
    p = h_rm.text_frame.paragraphs[0]
    p.text = "Room Allocation & Capacity Visualization"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

    tb_rm = slide8.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True
    rm_points = [
        "Sample Room Table Layout (Live Implementation):",
        "  • Room A-101 | Single Bed | 0/1 Beds [Available Badge]",
        "  • Room A-102 | Double Sharing | 2/2 Beds [FULL - Overbooking Locked]",
        "  • Room A-201 | Triple Sharing | 2/3 Beds [Available Badge - 1 Bed Vacant]",
        "  • Room B-102 | Double Sharing | 2/2 Beds [FULL - Girls Block]",
        "  • Room B-202 | AC-Double | 0/2 Beds [Under Maintenance Badge]",
        "",
        "Capacity Engine Features:",
        "✓ Automatically counts occupied beds via related_name='students'.",
        "✓ Progress bar transitions from Green (vacant) to Red (full).",
        "✓ Prevents assigning students to full or maintenance rooms."
    ]
    for idx, pt in enumerate(rm_points):
        p = tf_rm.paragraphs[0] if idx == 0 else tf_rm.add_paragraph()
        p.text = pt
        p.font.size = Pt(10)
        p.font.color.rgb = DARK
        if "Capacity Engine" in pt or "Sample Room" in pt:
            p.font.bold = True
            p.font.color.rgb = NAVY

    # Right: Student Directory Showcase
    box_sm = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2))
    box_sm.fill.solid()
    box_sm.fill.fore_color.rgb = WHITE
    box_sm.line.color.rgb = BORDER_COL

    h_sm = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(0.55))
    h_sm.fill.solid()
    h_sm.fill.fore_color.rgb = BLUE
    h_sm.line.fill.background()
    p = h_sm.text_frame.paragraphs[0]
    p.text = "Student Directory & Multi-Criteria Filtering"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

    tb_sm = slide8.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_sm = tb_sm.text_frame
    tf_sm.word_wrap = True
    sm_points = [
        "Search & Filter Bar Components:",
        "  [ Search: 'Rahul' or 'MCA' ] [ Dept: All / MCA / CSE / IT ]",
        "  [ Year: 1st / 2nd / 3rd / 4th ] [ Room Status: Allocated / Unassigned ]",
        "",
        "Student Record Cards & Modals:",
        "✓ Student ID, Full Name, Department, Year, Gender, Phone & Email.",
        "✓ Room allotment status with direct link to Room Details.",
        "✓ View Profile: Shows personal information, roommates, & complaints.",
        "✓ Edit & Delete Operations with safe student account cleanup.",
        "✓ Unassigned students can be assigned to vacant beds with 1 click."
    ]
    for idx, pt in enumerate(sm_points):
        p = tf_sm.paragraphs[0] if idx == 0 else tf_sm.add_paragraph()
        p.text = pt
        p.font.size = Pt(10)
        p.font.color.rgb = DARK
        if "Search & Filter" in pt or "Student Record" in pt:
            p.font.bold = True
            p.font.color.rgb = BLUE

    # ==========================================
    # SLIDE 9: SCREENSHOTS & UI SHOWCASE - COMPLAINT SYSTEM
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. System Demonstration: Grievance Redressal Lifecycle", "COMPLAINT MANAGEMENT")

    steps = [
        ("Step 1: Student Lodges Complaint", "Student Portal", [
            "Category Selection: Electrical, Plumbing, Cleaning, Food, Water, Internet, etc.",
            "Subject & Detailed description.",
            "Auto-generates Complaint ID (e.g. CMP-0001).",
            "Initial Status: 'Pending' with yellow badge."
        ], AMBER),
        ("Step 2: Warden Reviews & Actions", "Warden Portal", [
            "Grievance appears instantly on admin dashboard.",
            "Warden inspects issue & student room details.",
            "Status updated to: 'In Progress' or 'Resolved'.",
            "Warden writes official remarks / action taken."
        ], BLUE),
        ("Step 3: Live Student Tracking", "Student Portal", [
            "Real-time status updates on student dashboard.",
            "Green 'Resolved' badge upon completion.",
            "Warden's remarks displayed in response card.",
            "Strict privacy: Students only see their own issues."
        ], GREEN),
    ]

    for idx, (s_title, s_badge, s_items, s_col) in enumerate(steps):
        x = Inches(0.8 + idx * 3.95)
        card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.75), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = s_col
        card.line.width = Pt(1.5)

        h = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.75), Inches(0.75))
        h.fill.solid()
        h.fill.fore_color.rgb = s_col
        h.line.fill.background()
        p = h.text_frame.paragraphs[0]
        p.text = s_title + "\n(" + s_badge + ")"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = WHITE

        tb = slide9.shapes.add_textbox(x + Inches(0.15), Inches(2.4), Inches(3.45), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for it_idx, item in enumerate(s_items):
            p = tf.paragraphs[0] if it_idx == 0 else tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(10)
            p.font.color.rgb = DARK
            p.space_after = Pt(10)

    # ==========================================
    # SLIDE 10: SCREENSHOTS & UI SHOWCASE - STUDENT PORTAL & ANALYTICS
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. System Demonstration: Student Portal & Hostel Analytics", "STUDENT & ANALYTICS")

    # Left: Student Portal Experience
    box_sp = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    box_sp.fill.solid()
    box_sp.fill.fore_color.rgb = WHITE
    box_sp.line.color.rgb = BORDER_COL

    h_sp = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(0.55))
    h_sp.fill.solid()
    h_sp.fill.fore_color.rgb = NAVY
    h_sp.line.fill.background()
    p = h_sp.text_frame.paragraphs[0]
    p.text = "Student Self-Service Portal"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

    tb_sp = slide10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_sp = tb_sp.text_frame
    tf_sp.word_wrap = True
    sp_items = [
        "Student Dashboard Experience (Logged in as STU001):",
        "  • Welcome greeting with Student ID & Department.",
        "  • Assigned Room Summary card (Room A-102, Block A, Floor 1).",
        "  • Quick Complaint counters: Total Lodged, Pending, Resolved.",
        "  • Roommate Directory: Names, department, and contact phone.",
        "",
        "My Profile & Room Details Views:",
        "✓ Displays institutional registration details.",
        "✓ Lists room amenities, sharing type, and bed counts.",
        "✓ 1-click 'Report Room Issue' button for immediate grievance entry."
    ]
    for idx, it in enumerate(sp_items):
        p = tf_sp.paragraphs[0] if idx == 0 else tf_sp.add_paragraph()
        p.text = it
        p.font.size = Pt(10)
        p.font.color.rgb = DARK
        if "Student Dashboard" in it or "My Profile" in it:
            p.font.bold = True
            p.font.color.rgb = NAVY

    # Right: Hostel Analytics & Statistics
    box_an = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.2))
    box_an.fill.solid()
    box_an.fill.fore_color.rgb = WHITE
    box_an.line.color.rgb = BORDER_COL

    h_an = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.733), Inches(0.55))
    h_an.fill.solid()
    h_an.fill.fore_color.rgb = BLUE
    h_an.line.fill.background()
    p = h_an.text_frame.paragraphs[0]
    p.text = "Warden Hostel Analytics & Statistics"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = WHITE

    tb_an = slide10.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_an = tb_an.text_frame
    tf_an.word_wrap = True
    an_items = [
        "Analytical Visualizations (Statistics Page):",
        "  1. Block-wise Occupancy Breakdown:",
        "     - Block A (Boys): 4 Rooms, 10 Beds, 5 Occupied (50%)",
        "     - Block B (Girls): 4 Rooms, 9 Beds, 2 Occupied (22%)",
        "",
        "  2. Student Demographics:",
        "     - Distribution by Department (MCA: 3, CSE: 2, IT: 1, ECE: 1...)",
        "     - Distribution by Academic Year (1st, 2nd, 3rd, 4th Year)",
        "",
        "  3. Grievance Redressal Metrics:",
        "     - Complaints by Category: Electrical, Plumbing, Internet, Cleaning",
        "     - Resolution Rates: Pending vs In Progress vs Resolved"
    ]
    for idx, it in enumerate(an_items):
        p = tf_an.paragraphs[0] if idx == 0 else tf_an.add_paragraph()
        p.text = it
        p.font.size = Pt(10)
        p.font.color.rgb = DARK
        if "Analytical Visualizations" in it:
            p.font.bold = True
            p.font.color.rgb = BLUE

    # ==========================================
    # SLIDE 11: TESTING, VALIDATION & SECURITY
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Verification, Security & Automated Testing", "QUALITY ASSURANCE")

    test_cards = [
        ("Automated Test Suite (12/12 Passed)", [
            "Executed 'python manage.py test' with 100% pass rate.",
            "test_room_occupancy_update: Verifies bed counting & status flip to 'Full'.",
            "test_complaint_auto_id_generation: Checks CMP-XXXX sequence.",
            "test_admin_views_render: Validates 200 OK across all admin URLs.",
            "test_student_views_render: Validates 200 OK across all student URLs."
        ], GREEN),
        ("Role-Based Security & Permissions", [
            "@admin_required: Intercepts unauthorized students and redirects them.",
            "@student_required: Prevents non-student access to personal portals.",
            "Student Complaint Isolation: Verified Student B cannot view Student A's grievances (returns 404 security barrier).",
            "Password Hashing: Uses PBKDF2 with SHA-256 algorithm."
        ], NAVY),
        ("Input Validation & Integrity Rules", [
            "10-Digit Mobile Regex: Rejects invalid or incomplete phone entries.",
            "Over-Capacity Validation: Form rejects assigning students to full rooms.",
            "Unique Student ID & Room Number constraint enforcement.",
            "Empty Subject & Description rejection on complaint forms."
        ], BLUE),
        ("Disaster Recovery & Portability", [
            "Zero Configuration Deployment: SQLite file (db.sqlite3) embedded.",
            "Self-healing sample data generator: 'python manage.py seed_data'.",
            "1-Click Windows execution via RUN_SERVER.bat.",
            "Django Admin integration for low-level database audits."
        ], AMBER)
    ]

    for idx, (t_title, t_points, t_col) in enumerate(test_cards):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.5 + (idx // 2) * 2.7)

        card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = t_col
        card.line.width = Pt(1.5)

        h = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(0.55))
        h.fill.solid()
        h.fill.fore_color.rgb = t_col
        h.line.fill.background()
        p = h.text_frame.paragraphs[0]
        p.text = t_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

        tb = slide11.shapes.add_textbox(x + Inches(0.2), y + Inches(0.6), Inches(5.2), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        for p_idx, pt in enumerate(t_points):
            p = tf.paragraphs[0] if p_idx == 0 else tf.add_paragraph()
            p.text = "✓ " + pt
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK
            p.space_after = Pt(2)

    # ==========================================
    # SLIDE 12: CONCLUSION & FUTURE WORK (REVIEW 3)
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Conclusion & Scope for Final Review (Review 3)", "CONCLUSION & NEXT STEPS")

    card_c1 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    card_c1.fill.solid()
    card_c1.fill.fore_color.rgb = WHITE
    card_c1.line.color.rgb = GREEN
    card_c1.line.width = Pt(1.5)

    h_c1 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(0.6))
    h_c1.fill.solid()
    h_c1.fill.fore_color.rgb = GREEN
    h_c1.line.fill.background()
    p = h_c1.text_frame.paragraphs[0]
    p.text = "Review 2 Deliverables Summary"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE

    tb_c1 = slide12.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    c1_points = [
        "100% Functional Web Prototype Developed:",
        "  • Implemented Python Django backend with SQLite.",
        "  • Responsive Bootstrap 5 interface tailored for all screen sizes.",
        "",
        "Dual-Role Operational Capabilities:",
        "  • Warden: Full control over room allocation, students, and grievances.",
        "  • Student: Personalized dashboard, profile, and complaint tracker.",
        "",
        "Academic & Robustness Standards Met:",
        "  • 12/12 Automated unit & integration tests passing.",
        "  • Clean MVC/MVT code structure adhering to industry best practices."
    ]
    for idx, pt in enumerate(c1_points):
        p = tf_c1.paragraphs[0] if idx == 0 else tf_c1.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK
        if "100%" in pt or "Dual-Role" in pt or "Academic" in pt:
            p.font.bold = True
            p.font.color.rgb = GREEN

    card_c2 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    card_c2.fill.solid()
    card_c2.fill.fore_color.rgb = WHITE
    card_c2.line.color.rgb = NAVY
    card_c2.line.width = Pt(1.5)

    h_c2 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(0.6))
    h_c2.fill.solid()
    h_c2.fill.fore_color.rgb = NAVY
    h_c2.line.fill.background()
    p = h_c2.text_frame.paragraphs[0]
    p.text = "Proposed Enhancements for Final Review (Review 3)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE

    tb_c2 = slide12.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.2), Inches(4.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    c2_points = [
        "1. Automated PDF Report Generation:",
        "   - Monthly hostel occupancy certificates & complaint summaries.",
        "",
        "2. Mess & Food Management Module:",
        "   - Weekly meal scheduling & student feedback ratings.",
        "",
        "3. Automated Notification Dispatcher:",
        "   - SMS / Email alerts when a warden marks a grievance as Resolved.",
        "",
        "4. Hostel Fee Payment Tracking:",
        "   - Maintenance dues & digital payment receipts.",
        "",
        "5. Final Review Documentation & Project Report Book Preparation."
    ]
    for idx, pt in enumerate(c2_points):
        p = tf_c2.paragraphs[0] if idx == 0 else tf_c2.add_paragraph()
        p.text = pt
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK
        if any(pt.startswith(str(n)) for n in range(1, 6)):
            p.font.bold = True
            p.font.color.rgb = NAVY

    # Save presentation
    output_path = r"c:\Users\Admin\Documents\miniproject\Hostel_Management_System_Review2.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_presentation()
