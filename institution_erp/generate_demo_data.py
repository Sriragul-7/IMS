"""
Generate Demo Data for Institution ERP
=======================================
Run: bench --site institution.localhost execute institution_erp.generate_demo_data.run

Idempotent: safe to run multiple times without creating duplicates.
Uses @demo.institution.local email domain for all demo Users/Guardians/Students
so demo records are identifiable by pattern without looking fake in the UI.
"""
import frappe
import random
import json
from frappe.utils import today, add_days, add_months, getdate, nowdate, cint
from datetime import datetime, timedelta

random.seed(42)  # Reproducible data

DEMO_EMAIL_DOMAIN = "demo.institution.local"
DEMO_PASSWORD = "Demo@2026"
TAG = "DEMO_DATA"  # Not a real field, but used in remarks/comments where applicable

# ─── Name Pools ──────────────────────────────────────────────────────────────

FIRST_NAMES_M = [
    "Arjun", "Vivaan", "Aditya", "Vihaan", "Arnav", "Reyansh", "Krishna",
    "Ishaan", "Shaurya", "Atharv", "Advik", "Pranav", "Advaith", "Aarav",
    "Vedant", "Kabir", "Aarush", "Dhruv", "Hrithik", "Rohit", "Suresh",
    "Vikram", "Rajesh", "Manoj", "Sanjay", "Prakash", "Ravi", "Sunil",
    "Deepak", "Ajay", "Nitin", "Mohan", "Ramesh", "Sachin", "Amit",
    "Rahul", "Nikhil", "Pankaj", "Vishal", "Tarun", "Karan", "Naveen",
    "Shankar", "Ganesh", "Mohan", "Vijay", "Subhash", "Anil", "Rajiv"
]

FIRST_NAMES_F = [
    "Ananya", "Diya", "Myra", "Sara", "Aanya", "Aadhya", "Aaradhya",
    "Anvi", "Navya", "Prisha", "Riya", "Kavya", "Ishita", "Pihu",
    "Aisha", "Ritika", "Nisha", "Pooja", "Sunita", "Geeta", "Suman",
    "Rekha", "Asha", "Meena", "Kavita", "Sapna", "Pallavi", "Neelam",
    "Shweta", "Sneha", "Divya", "Preeti", "Mamta", "Usha", "Vandana",
    "Deepika", "Priyanka", "Sonal", "Rachna", "Garima", "Nandini",
    "Tanya", "Lakshmi", "Parvati", "Manju", "Sabita", "Jyoti", "Kusum"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Reddy", "Nair",
    "Iyer", "Mishra", "Pandey", "Tiwari", "Rao", "Das", "Mukherjee",
    "Chatterjee", "Banerjee", "Joshi", "Mehta", "Patel", "Shah",
    "Choudhary", "Yadav", "Malhotra", "Kapoor", "Chauhan", "Sinha",
    "Bhat", "Pillai", "Menon", "Pandit", "Kulkarni", "Desai",
    "Naik", "Gowda", "Shetty", "Hegde", "Kamath", "Prasad",
    "Saxena", "Khanna", "Bajaj", "Goyal", "Agarwal", "Srivastava",
    "Trivedi", "Dubey", "Mishra", "Chaubey", "Tandon", "Bhatt"
]

GUARDIAN_FIRST_NAMES = [
    "Rajesh", "Suresh", "Mahesh", "Dinesh", "Ramesh", "Naresh",
    "Ganesh", "Yogesh", "Mukesh", "Hitesh", "Bhavesh", "Kalpesh",
    "Kamlesh", "Piyush", "Sanjay", "Vijay", "Ajay", "Nikhil",
    "Pooja", "Sunita", "Geeta", "Suman", "Rekha", "Asha",
    "Meena", "Kavita", "Sapna", "Pallavi", "Neelam", "Shweta",
    "Usha", "Vandana", "Deepika", "Priyanka", "Suman", "Arun",
    "Bharat", "Chetan", "Darshan", "Eeshan"
]

COURSES_PER_PROGRAM = {
    "B.Sc Computer Science": [
        ("Programming in C", "BCS101", 4),
        ("Data Structures", "BCS102", 4),
        ("Database Management Systems", "BCS201", 4),
        ("Operating Systems", "BCS202", 4),
    ],
    "B.Com": [
        ("Financial Accounting", "BCO101", 4),
        ("Business Economics", "BCO102", 3),
        ("Corporate Law", "BCO201", 3),
        ("Cost Accounting", "BCO202", 4),
    ],
    "BBA": [
        ("Principles of Management", "BBA101", 3),
        ("Marketing Management", "BBA102", 3),
        ("Human Resource Management", "BBA201", 3),
        ("Business Communication", "BBA202", 3),
    ],
    "B.A. English": [
        ("English Literature: Poetry", "BEN101", 3),
        ("English Literature: Prose", "BEN102", 3),
        ("Linguistics", "BEN201", 4),
        ("Creative Writing", "BEN202", 3),
    ],
}

# Instructor names (fixed set for consistency)
INSTRUCTOR_DATA = [
    ("Dr. Priya Sharma", "priya.sharma@demo.institution.local", "Computer Science"),
    ("Prof. Rakesh Gupta", "rakesh.gupta@demo.institution.local", "Computer Science"),
    ("Dr. Meena Iyer", "meena.iyer@demo.institution.local", "Commerce"),
    ("Prof. Suresh Kumar", "suresh.kumar@demo.institution.local", "Commerce"),
    ("Dr. Anita Reddy", "anita.reddy@demo.institution.local", "Management"),
    ("Prof. Deepak Nair", "deepak.nair@demo.institution.local", "Management"),
    ("Dr. Kavita Joshi", "kavita.joshi@demo.institution.local", "English"),
    ("Prof. Vikram Singh", "vikram.singh@demo.institution.local", "English"),
    ("Dr. Sunita Patel", "sunita.patel@demo.institution.local", "Computer Science"),
    ("Prof. Rajiv Mishra", "rajiv.mishra@demo.institution.local", "Commerce"),
]

ROOM_DATA = [
    ("CS-Lab-A101", "Main Block", "1", 40, "Lab"),
    ("CS-Lab-A102", "Main Block", "1", 35, "Lab"),
    ("Lecture Hall B201", "Main Block", "2", 120, "Auditorium"),
    ("Lecture Hall B202", "Main Block", "2", 80, "Classroom"),
    ("Classroom C301", "Annex Block", "3", 60, "Classroom"),
    ("Classroom C302", "Annex Block", "3", 60, "Classroom"),
    ("Seminar Hall D101", "Annex Block", "1", 100, "Auditorium"),
    ("Commerce Lab E201", "Commerce Wing", "2", 45, "Lab"),
]

BOOK_DATA = [
    ("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033848", "Computer Science", "MIT Press", "4th", 2022, 8),
    ("Clean Code", "Robert C. Martin", "978-0132350884", "Computer Science", "Pearson", "1st", 2008, 5),
    ("Design Patterns", "Gang of Four", "978-0201633610", "Computer Science", "Addison-Wesley", "1st", 1994, 4),
    ("The Pragmatic Programmer", "David Thomas", "978-0135957059", "Computer Science", "Addison-Wesley", "2nd", 2019, 6),
    ("Computer Networks", "Andrew Tanenbaum", "978-0132126953", "Computer Science", "Pearson", "5th", 2010, 5),
    ("Operating System Concepts", "Abraham Silberschatz", "978-1119800361", "Computer Science", "Wiley", "10th", 2018, 4),
    ("Financial Accounting", "T.S. Grewal", "978-8194702313", "Commerce", "S. Chand", "2nd", 2020, 7),
    ("Business Economics", "H.L. Ahuja", "978-8131808092", "Commerce", "S. Chand", "14th", 2019, 6),
    ("Corporate Law", "N.D. Kapoor", "978-8176925372", "Commerce", "Sultan Chand", "1st", 2021, 5),
    ("Cost Accounting", "B.M. Lall Nigam", "978-8120349957", "Commerce", "PHI Learning", "2nd", 2018, 4),
    ("Principles of Management", "P.C. Tripathi", "978-8120351967", "Management", "PHI Learning", "6th", 2020, 5),
    ("Marketing Management", "Philip Kotler", "978-0134648590", "Management", "Pearson", "16th", 2021, 6),
    ("Human Resource Management", "Gary Dessler", "978-0135399828", "Management", "Pearson", "14th", 2020, 4),
    ("Business Communication", "R.K. Madhukar", "978-8120351233", "Management", "PHI Learning", "3rd", 2019, 5),
    ("English Poetry: A Selection", "Nissim Ezekiel (ed.)", "978-8129126412", "English Literature", "Oxford India", "3rd", 2017, 8),
    ("Modern English Prose", "R.K. Sinha (ed.)", "978-8125915348", "English Literature", "Vikas", "2nd", 2016, 6),
    ("An Introduction to Linguistics", "Stephanie Plum stock", "978-1405191128", "English Literature", "Wiley-Blackwell", "1st", 2011, 4),
    ("The Art of Creative Writing", "Lucien Stryk", "978-0226778310", "English Literature", "University of Chicago", "1st", 2013, 3),
    ("Data Communications and Networking", "Behrouz Forouzan", "978-0073376226", "Computer Science", "McGraw-Hill", "5th", 2013, 5),
    ("Python Crash Course", "Eric Matthes", "978-1593279288", "Computer Science", "No Starch Press", "3rd", 2023, 7),
    ("Machine Learning with Python", "IBM", "978-1644594179", "Computer Science", "O'Reilly", "1st", 2024, 4),
    ("Advanced Java Programming", "John DeNero", "978-1492088936", "Computer Science", "O'Reilly", "2nd", 2021, 3),
    ("Indian Economy", "Misra & Puri", "978-8120352223", "Commerce", "Vikas", "12th", 2020, 5),
    ("Business Ethics", "C.S.G.R. Kuppuswamy", "978-8120348937", "Management", "PHI Learning", "1st", 2019, 3),
    ("Indian Writing in English", "Rajiv Ayyangar", "978-8125055143", "English Literature", "Orient Longman", "1st", 2015, 4),
    ("Statistics for Business", "David R. Anderson", "978-1305585317", "Commerce", "Cengage", "13th", 2018, 5),
    ("Digital Electronics", "Morris Mano", "978-0132624282", "Computer Science", "Pearson", "5th", 2016, 3),
    ("Web Development with Django", "William S. Vincent", "978-1680502398", "Computer Science", "Pragmatic Bookshelf", "2nd", 2022, 4),
    ("Principles of Microeconomics", "N. Gregory Mankiw", "978-0357038314", "Commerce", "Cengage", "9th", 2020, 6),
    ("Entrepreneurship Development", "C.B. Gupta", "978-8120352445", "Management", "PHI Learning", "4th", 2019, 3),
    ("Sociolinguistics", "Rajend Mesthrie", "978-0748638543", "English Literature", "Edinburgh University", "2nd", 2011, 2),
    ("Compiler Design", "Rajiv Malhotra", "978-8120350588", "Computer Science", "PHI Learning", "1st", 2018, 3),
    ("Security Analysis", "Benjamin Graham", "978-0070244153", "Commerce", "Tata McGraw-Hill", "6th", 2019, 4),
    ("Supply Chain Management", "Sunil Chopra", "978-0134739045", "Management", "Pearson", "7th", 2019, 3),
]

# ─── Helper Functions ────────────────────────────────────────────────────────

def _name_exists(doctype, filters):
    return frappe.db.exists(doctype, filters)

def _get_or_create(doctype, filters, defaults):
    existing = frappe.db.exists(doctype, filters)
    if existing:
        return existing
    doc = frappe.get_doc({"doctype": doctype, **defaults})
    doc.insert(ignore_permissions=True)
    return doc.name

def _random_name(pool, used):
    available = [n for n in pool if n not in used]
    if not available:
        available = pool
    name = random.choice(available)
    used.add(name)
    return name

def _demo_email(first, last):
    return f"{first.lower().replace(' ', '.')}@{DEMO_EMAIL_DOMAIN}"

def _indian_phone():
    return f"+91-{random.choice([7,8,9])}{random.randint(100000000, 999999999)}"

def _past_date(weeks_back):
    return add_days(today(), -weeks_back * 7)

def _random_date_in_range(start_weeks_back, end_weeks_back):
    start = getdate(add_days(today(), -start_weeks_back * 7))
    end = getdate(add_days(today(), -end_weeks_back * 7))
    delta = (end - start).days
    if delta <= 0:
        return str(start)
    return str(add_days(start, random.randint(0, delta)))


# ─── PHASE 1: Foundational Data ─────────────────────────────────────────────

def generate_academic_data():
    print("\n[Phase 1] Academic Years, Terms, Programs, Courses, Rooms, Instructors...")

    # Academic Years
    ay_current = _get_or_create("Academic Year", {"academic_year_name": "2026-2027"},
        {"academic_year_name": "2026-2027", "year_start_date": "2026-06-01", "year_end_date": "2027-04-30"})
    ay_prev = _get_or_create("Academic Year", {"academic_year_name": "2025-2026"},
        {"academic_year_name": "2025-2026", "year_start_date": "2025-06-01", "year_end_date": "2026-04-30"})
    print(f"  Academic Years: {ay_current}, {ay_prev}")

    # Academic Terms
    terms = {}
    for ay_name, ay_label in [(ay_current, "2026-27"), (ay_prev, "2025-26")]:
        for i, (tname, start, end) in enumerate([
            (f"Term 1 {ay_label}", f"2026-06-01" if ay_label == "2026-27" else "2025-06-01",
             f"2026-09-30" if ay_label == "2026-27" else "2025-09-30"),
            (f"Term 2 {ay_label}", f"2026-10-01" if ay_label == "2026-27" else "2025-10-01",
             f"2027-04-30" if ay_label == "2026-27" else "2026-04-30"),
        ]):
            tid = _get_or_create("Academic Term", {"term_name": tname},
                {"term_name": tname, "academic_year": ay_name, "term_start_date": start, "term_end_date": end})
            terms[tname] = tid
    print(f"  Academic Terms: {len(terms)} created")

    # Programs
    programs = {}
    prog_data = [
        ("B.Sc Computer Science", "BCS", "Regular", "Department of Computer Science"),
        ("B.Com", "BCOM", "Regular", "Department of Commerce"),
        ("BBA", "BBA", "Regular", "Department of Management Studies"),
        ("B.A. English", "BA-ENG", "Regular", "Department of English"),
    ]
    for pname, pcode, ptype, dept in prog_data:
        pid = _get_or_create("Program", {"program_name": pname},
            {"program_name": pname, "program_code": pcode, "program_type": ptype, "department": dept})
        programs[pname] = pid
    print(f"  Programs: {list(programs.keys())}")

    # Courses
    courses = {}
    for prog_name, course_list in COURSES_PER_PROGRAM.items():
        for cname, ccode, credits in course_list:
            cid = _get_or_create("Course", {"course_name": cname},
                {"course_name": cname, "course_code": ccode, "program": programs[prog_name], "credits": credits})
            courses[cname] = cid
    print(f"  Courses: {len(courses)} total")

    # Rooms
    rooms = {}
    for rname, building, floor, cap, rtype in ROOM_DATA:
        rid = _get_or_create("Room", {"room_name": rname},
            {"room_name": rname, "building": building, "floor": floor, "capacity": cap, "room_type": rtype})
        rooms[rname] = rid
    print(f"  Rooms: {len(rooms)}")

    # Instructors
    instructors = {}
    for iname, iemail, idept in INSTRUCTOR_DATA:
        existing = frappe.db.get_value("Instructor", {"instructor_name": iname}, "name")
        if existing:
            instructors[iname] = existing
            continue
        doc = frappe.get_doc({
            "doctype": "Instructor",
            "instructor_name": iname,
            "email": iemail,
            "department": idept,
            "status": "Active",
        })
        doc.insert(ignore_permissions=True)
        instructors[iname] = doc.name
    print(f"  Instructors: {len(instructors)}")

    frappe.db.commit()
    return {
        "ay_current": ay_current, "ay_prev": ay_prev,
        "terms": terms, "programs": programs, "courses": courses,
        "rooms": rooms, "instructors": instructors,
    }


# ─── PHASE 2: Students, Guardians, Groups ────────────────────────────────────

def generate_students_and_guardians(academic):
    print("\n[Phase 2] Students, Guardians, Student Groups...")

    programs = academic["programs"]
    ay_current = academic["ay_current"]
    terms = academic["terms"]

    # Find current term 1
    current_term = None
    for k, v in terms.items():
        if "Term 1 2026-27" in k:
            current_term = v
            break

    # Generate Guardians first
    guardians = {}
    used_guardian_names = set()
    guardian_emails_used = set()

    # We need ~50 unique guardians (some linked to 2+ students)
    for i in range(50):
        gemail = f"guardian{i+1:02d}@{DEMO_EMAIL_DOMAIN}"

        existing = frappe.db.get_value("Guardian", {"guardian_email": gemail}, "name")
        if existing:
            guardians[gemail] = existing
            continue

        gfirst = _random_name(GUARDIAN_FIRST_NAMES, used_guardian_names)
        glast = random.choice(LAST_NAMES)
        gname = f"{gfirst} {glast}"

        doc = frappe.get_doc({
            "doctype": "Guardian",
            "guardian_name": gname,
            "guardian_email": gemail,
            "relation_to_student": random.choice(["Father", "Mother", "Guardian"]),
            "phone_number": _indian_phone(),
            "mobile_number": _indian_phone(),
            "occupation": random.choice(["Engineer", "Doctor", "Teacher", "Business", "Govt. Employee", "Retired", "Homemaker"]),
        })
        doc.insert(ignore_permissions=True)
        guardians[gemail] = doc.name
    print(f"  Guardians: {len(guardians)}")

    # Generate Students distributed across programs
    students = {}
    used_student_names = set()
    student_emails_used = set()
    guardian_emails_list = list(guardians.keys())

    # ~70 students: 20 CS, 18 Commerce, 17 BBA, 15 English
    students_per_program = {
        "B.Sc Computer Science": 20,
        "B.Com": 18,
        "BBA": 17,
        "B.A. English": 15,
    }
    prog_codes = {
        "B.Sc Computer Science": "cs",
        "B.Com": "bcom",
        "BBA": "bba",
        "B.A. English": "eng",
    }

    for prog_name, count in students_per_program.items():
        prog_id = programs[prog_name]
        pcode = prog_codes[prog_name]
        for i in range(count):
            semail = f"{pcode}{i+1:02d}@{DEMO_EMAIL_DOMAIN}"

            existing = frappe.db.get_value("Student", {"email_address": semail}, "name")
            if existing:
                students[semail] = existing
                continue

            gender = random.choice(["Male", "Female"])
            first_pool = FIRST_NAMES_M if gender == "Male" else FIRST_NAMES_F
            sfirst = _random_name(first_pool, used_student_names)
            slast = random.choice(LAST_NAMES)
            sname = f"{sfirst} {slast}"

            # Some students get same guardian (siblings)
            if i < 3 and prog_name == "B.Sc Computer Science":
                gemail = guardian_emails_list[0]
            elif i < 2 and prog_name == "B.Com":
                gemail = guardian_emails_list[1]
            else:
                gemail = random.choice(guardian_emails_list)

            dob_year = random.choice([2004, 2005, 2006])
            dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

            existing = frappe.db.get_value("Student", {"email_address": semail}, "name")
            if existing:
                students[semail] = existing
                continue

            # Status distribution: 85% Active, 5% Alumni, 5% Graduated, 5% Inactive
            status_roll = random.random()
            if status_roll < 0.85:
                status = "Active"
            elif status_roll < 0.90:
                status = "Alumni"
            elif status_roll < 0.95:
                status = "Graduated"
            else:
                status = "Inactive"

            doc = frappe.get_doc({
                "doctype": "Student",
                "first_name": sfirst,
                "last_name": slast,
                "gender": gender,
                "date_of_birth": dob,
                "email_address": semail,
                "phone_number": _indian_phone(),
                "program": prog_id,
                "academic_year": ay_current,
                "guardian": guardians[gemail],
                "status": status,
                "blood_group": random.choice(["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"]),
                "previous_school": random.choice([
                    "Delhi Public School", "Kendriya Vidyalaya", "D.A.V. Public School",
                    "St. Xavier's School", "Ryan International School", "The Doon School",
                    "Sainik School", "Jawahar Navodaya Vidyalaya",
                ]),
            })
            doc.insert(ignore_permissions=True)
            students[semail] = doc.name
    print(f"  Students: {len(students)}")

    # Student Groups for current term
    student_groups = {}
    course_list_per_program = {
        "B.Sc Computer Science": ["Programming in C", "Data Structures"],
        "B.Com": ["Financial Accounting", "Business Economics"],
        "BBA": ["Principles of Management", "Marketing Management"],
        "B.A. English": ["English Literature: Poetry", "English Literature: Prose"],
    }

    for prog_name, courses in course_list_per_program.items():
        for cname in courses:
            gname = f"{prog_name} - {cname} - Term 1"
            existing = frappe.db.get_value("Student Group", {"group_name": gname}, "name")
            if existing:
                student_groups[gname] = existing
                continue

            doc = frappe.get_doc({
                "doctype": "Student Group",
                "group_name": gname,
                "program": programs[prog_name],
                "academic_year": ay_current,
                "academic_term": current_term,
                "course": academic["courses"][cname],
                "max_strength": 30,
                "group_based_on": "Course",
            })

            # Add students from this program
            prog_students = [s for s, v in students.items()
                           if frappe.db.get_value("Student", v, "program") == programs[prog_name]
                           and frappe.db.get_value("Student", v, "status") == "Active"]
            for semail in prog_students[:25]:
                doc.append("members", {"student": students[semail]})

            doc.insert(ignore_permissions=True)
            student_groups[gname] = doc.name
    print(f"  Student Groups: {len(student_groups)}")

    frappe.db.commit()
    return {"guardians": guardians, "students": students, "student_groups": student_groups, "current_term": current_term}


# ─── PHASE 3: Course Schedules ───────────────────────────────────────────────

def generate_schedules(academic, students_data):
    print("\n[Phase 3] Course Schedules...")

    rooms = list(academic["rooms"].values())
    instructors = list(academic["instructors"].values())
    groups = students_data["student_groups"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = list(range(9, 16))  # 9 AM to 3 PM

    count = 0
    # Track used room+day+hour slots globally to avoid double-booking
    used_room_slots = set()
    # Track used instructor+day+hour slots
    used_instructor_slots = set()

    for gname, gid in groups.items():
        num_sessions = random.randint(2, 3)
        available_hours = hours.copy()
        random.shuffle(available_hours)

        for session_idx in range(num_sessions):
            if not available_hours:
                break

            placed = False
            random.shuffle(days)
            for day in days:
                if placed:
                    break
                random.shuffle(available_hours)
                for hour in available_hours[:]:
                    room = random.choice(rooms)
                    instructor = random.choice(instructors)

                    room_slot = (room, day, hour)
                    instr_slot = (instructor, day, hour)

                    if room_slot in used_room_slots or instr_slot in used_instructor_slots:
                        continue

                    # Check existing DB too
                    existing = frappe.db.exists("Course Schedule", {
                        "student_group": gid, "day_of_week": day, "from_time": f"{hour:02d}:00:00"
                    })
                    if existing:
                        continue

                    course_name = gname.split(" - ")[1] if " - " in gname else None
                    course_id = academic["courses"].get(course_name)

                    try:
                        doc = frappe.get_doc({
                            "doctype": "Course Schedule",
                            "course": course_id,
                            "student_group": gid,
                            "instructor": instructor,
                            "room": room,
                            "day_of_week": day,
                            "from_time": f"{hour:02d}:00:00",
                            "to_time": f"{hour+1:02d}:00:00",
                        })
                        doc.insert(ignore_permissions=True)
                        used_room_slots.add(room_slot)
                        used_instructor_slots.add(instr_slot)
                        available_hours.remove(hour)
                        count += 1
                        placed = True
                        break
                    except Exception:
                        continue
    frappe.db.commit()
    print(f"  Course Schedules: {count}")


# ─── PHASE 4: Attendance ─────────────────────────────────────────────────────

def generate_attendance(academic, students_data):
    print("\n[Phase 4] Attendance (last 5 weeks)...")

    groups = students_data["student_groups"]
    instructors = academic["instructors"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    att_count = 0
    staff_count = 0

    # Student Attendance - last 5 weeks
    for week in range(1, 6):
        week_start = add_days(today(), -week * 7)
        for day_offset in range(5):  # Mon-Fri
            att_date = add_days(week_start, day_offset)
            day_name = days[day_offset]

            for gname, gid in groups.items():
                # Check if there's a course schedule for this group on this day
                schedule = frappe.db.get_value("Course Schedule",
                    {"student_group": gid, "day_of_week": day_name}, "name")
                if not schedule:
                    continue

                members = frappe.get_all("Student Group Member",
                    filters={"parent": gid}, pluck="student")

                for student in members:
                    existing = frappe.db.exists("Student Attendance", {
                        "student": student, "student_group": gid,
                        "attendance_date": str(att_date)
                    })
                    if existing:
                        continue

                    # 85-90% present, rest spread across Absent/Late/Excused
                    roll = random.random()
                    if roll < 0.87:
                        status = "Present"
                    elif roll < 0.93:
                        status = "Absent"
                    elif roll < 0.97:
                        status = "Late"
                    else:
                        status = "Excused"

                    doc = frappe.get_doc({
                        "doctype": "Student Attendance",
                        "student": student,
                        "student_group": gid,
                        "course_schedule": schedule,
                        "attendance_date": str(att_date),
                        "status": status,
                    })
                    doc.insert(ignore_permissions=True)
                    att_count += 1

    # Staff Attendance
    for week in range(1, 6):
        week_start = add_days(today(), -week * 7)
        for day_offset in range(5):
            att_date = add_days(week_start, day_offset)

            for iname, iid in instructors.items():
                existing = frappe.db.exists("Staff Attendance", {
                    "instructor": iid, "attendance_date": str(att_date)
                })
                if existing:
                    continue

                roll = random.random()
                status = "Present" if roll < 0.92 else ("Absent" if roll < 0.96 else "Half Day")

                doc = frappe.get_doc({
                    "doctype": "Staff Attendance",
                    "instructor": iid,
                    "attendance_date": str(att_date),
                    "status": status,
                })
                doc.insert(ignore_permissions=True)
                staff_count += 1

    frappe.db.commit()
    print(f"  Student Attendance: {att_count}")
    print(f"  Staff Attendance: {staff_count}")


# ─── PHASE 5: Grading Scale + Assessment ────────────────────────────────────

def generate_examination(academic, students_data):
    print("\n[Phase 5] Grading Scale, Assessment Groups, Plans, Results...")

    courses = academic["courses"]
    groups = students_data["student_groups"]
    ay_current = academic["ay_current"]
    current_term = students_data["current_term"]
    instructors = list(academic["instructors"].values())

    # Grading Scale
    gs_name = "Standard Grading"
    existing_gs = frappe.db.get_value("Grading Scale", {"scale_name": gs_name}, "name")
    if not existing_gs:
        gs = frappe.get_doc({
            "doctype": "Grading Scale",
            "scale_name": gs_name,
            "intervals": [
                {"grade_code": "A+", "threshold_percent": 90, "grade_description": "Outstanding"},
                {"grade_code": "A", "threshold_percent": 80, "grade_description": "Excellent"},
                {"grade_code": "B+", "threshold_percent": 70, "grade_description": "Very Good"},
                {"grade_code": "B", "threshold_percent": 60, "grade_description": "Good"},
                {"grade_code": "C", "threshold_percent": 50, "grade_description": "Average"},
                {"grade_code": "D", "threshold_percent": 40, "grade_description": "Below Average"},
                {"grade_code": "F", "threshold_percent": 0, "grade_description": "Fail"},
            ],
        })
        gs.insert(ignore_permissions=True)
        frappe.db.commit()
    grading_scale = existing_gs or gs.name
    print(f"  Grading Scale: {grading_scale}")

    # Assessment Groups (2-3 per term)
    ag_groups = {}
    ag_data = [
        (f"Unit Test 1 - Term 1 2026-27", current_term, 0),
        (f"Mid Term - Term 1 2026-27", current_term, 1),
        (f"Final - Term 1 2026-27", current_term, 1),  # published
    ]
    for agname, term_id, published in ag_data:
        existing = frappe.db.get_value("Assessment Group", {"group_name": agname}, "name")
        if existing:
            ag_groups[agname] = existing
            continue
        doc = frappe.get_doc({
            "doctype": "Assessment Group",
            "group_name": agname,
            "academic_term": term_id,
            "results_published": published,
            "weightage_percent": 33 if "Unit" in agname else (34 if "Mid" in agname else 33),
        })
        doc.insert(ignore_permissions=True)
        ag_groups[agname] = doc.name
    frappe.db.commit()
    print(f"  Assessment Groups: {list(ag_groups.keys())}")

    # Assessment Plans + Results
    plan_count = 0
    result_count = 0
    grading_intervals = frappe.get_all("Grading Interval",
        filters={"parent": grading_scale}, fields=["grade_code", "threshold_percent"],
        order_by="threshold_percent desc")

    for gname, gid in groups.items():
        parts = gname.split(" - ")
        if len(parts) < 2:
            continue
        cname = parts[1]
        cid = courses.get(cname)
        if not cid:
            continue

        members = frappe.get_all("Student Group Member",
            filters={"parent": gid}, pluck="student")
        if not members:
            continue

        instructor = random.choice(instructors)

        for agname, agid in ag_groups.items():
            existing_plan = frappe.db.exists("Assessment Plan", {
                "assessment_group": agid, "course": cid, "student_group": gid
            })
            if existing_plan:
                plan_name = existing_plan
            else:
                max_marks = random.choice([50, 75, 100])
                passing_marks = int(max_marks * 0.4)

                doc = frappe.get_doc({
                    "doctype": "Assessment Plan",
                    "assessment_group": agid,
                    "course": cid,
                    "student_group": gid,
                    "max_marks": max_marks,
                    "passing_marks": passing_marks,
                    "grading_scale": grading_scale,
                    "exam_date": str(_random_date_in_range(3, 1)),
                    "instructor": instructor,
                })
                doc.insert(ignore_permissions=True)
                plan_name = doc.name
                plan_count += 1

            # Assessment Results - bell curve distribution
            for student in members:
                existing_result = frappe.db.exists("Assessment Result", {
                    "assessment_plan": plan_name, "student": student
                })
                if existing_result:
                    continue

                # Bell curve: mean ~62%, std ~15
                max_marks_val = frappe.db.get_value("Assessment Plan", plan_name, "max_marks")
                passing_marks_val = frappe.db.get_value("Assessment Plan", plan_name, "passing_marks")

                raw_pct = random.gauss(62, 15)
                raw_pct = max(15, min(98, raw_pct))
                marks = int(max_marks_val * raw_pct / 100)

                # Calculate grade
                grade = "F"
                for interval in grading_intervals:
                    if marks >= interval.threshold_percent:
                        grade = interval.grade_code
                        break

                status = "Pass" if marks >= passing_marks_val else "Fail"

                doc = frappe.get_doc({
                    "doctype": "Assessment Result",
                    "assessment_plan": plan_name,
                    "student": student,
                    "marks_obtained": marks,
                })
                doc.insert(ignore_permissions=True)
                result_count += 1

    frappe.db.commit()
    print(f"  Assessment Plans: {plan_count}")
    print(f"  Assessment Results: {result_count}")


# ─── PHASE 6: Fees ──────────────────────────────────────────────────────────

def generate_fees(academic, students_data):
    print("\n[Phase 6] Fee Categories, Structures, Schedules, Fees, Payments...")

    programs = academic["programs"]
    ay_current = academic["ay_current"]

    # Fee Categories
    categories = {}
    for cname in ["Tuition Fee", "Lab Fee", "Library Fee", "Transport Fee"]:
        cid = _get_or_create("Fee Category", {"category_name": cname},
            {"category_name": cname, "description": f"Annual {cname}"})
        categories[cname] = cid
    print(f"  Fee Categories: {list(categories.keys())}")

    # Fee Structures per program
    structures = {}
    fee_amounts = {
        "B.Sc Computer Science": {"Tuition Fee": 75000, "Lab Fee": 15000, "Library Fee": 5000},
        "B.Com": {"Tuition Fee": 55000, "Library Fee": 4000},
        "BBA": {"Tuition Fee": 80000, "Library Fee": 5000, "Transport Fee": 12000},
        "B.A. English": {"Tuition Fee": 45000, "Library Fee": 3000},
    }
    for prog_name, amounts in fee_amounts.items():
        sname = f"{prog_name} - 2026-27"
        existing = frappe.db.get_value("Fee Structure", {"structure_name": sname}, "name")
        if existing:
            structures[prog_name] = existing
            continue

        components = []
        total = 0
        for cat_name, amt in amounts.items():
            components.append({"fee_category": categories[cat_name], "amount": amt})
            total += amt

        doc = frappe.get_doc({
            "doctype": "Fee Structure",
            "structure_name": sname,
            "program": programs[prog_name],
            "academic_year": ay_current,
            "total_amount": total,
            "components": components,
        })
        doc.insert(ignore_permissions=True)
        structures[prog_name] = doc.name
    frappe.db.commit()
    print(f"  Fee Structures: {len(structures)}")

    # Fee Schedules
    schedules = {}
    for prog_name, struct_name in structures.items():
        existing = frappe.db.get_value("Fee Schedule", {"fee_structure": struct_name}, "name")
        if existing:
            schedules[prog_name] = existing
            continue

        # Get active students in this program
        prog_id = programs[prog_name]
        prog_students = frappe.get_all("Student",
            filters={"program": prog_id, "status": "Active"}, pluck="name")

        applicable = []
        for s in prog_students:
            applicable.append({"student": s, "included": 1})

        if not applicable:
            continue

        doc = frappe.get_doc({
            "doctype": "Fee Schedule",
            "fee_structure": struct_name,
            "due_date": "2026-09-30",
            "applicable_students": applicable,
        })
        doc.insert(ignore_permissions=True)
        schedules[prog_name] = doc.name
    frappe.db.commit()
    print(f"  Fee Schedules: {len(schedules)}")

    # Generate Fees using the API
    fee_count = 0
    for prog_name, sched_name in schedules.items():
        existing_fees = frappe.get_all("Fees", filters={"fee_schedule": sched_name}, pluck="name")
        if existing_fees:
            fee_count += len(existing_fees)
            continue

        try:
            result = frappe.call(
                "institution_erp.api.generate_fees_from_schedule",
                fee_schedule_name=sched_name
            )
            if result and result.get("created"):
                fee_count += result["created"]
        except Exception as e:
            print(f"  Error generating fees for {prog_name}: {e}")
    frappe.db.commit()
    print(f"  Fees generated: {fee_count}")

    # Create Fee Payments (60% paid, 25% partial, 10% unpaid, 5% overdue)
    all_fees = frappe.get_all("Fees", pluck="name")
    pay_count = 0
    disc_count = 0

    for i, fee_name in enumerate(all_fees):
        fee = frappe.get_doc("Fees", fee_name)
        roll = random.random()

        if roll < 0.60:
            # Full payment
            pay_amount = fee.total_amount
            new_status = "Paid"
        elif roll < 0.85:
            # Partial payment
            pay_amount = int(fee.total_amount * random.uniform(0.3, 0.7))
            new_status = "Partially Paid"
        elif roll < 0.95:
            # Unpaid - no payment
            continue
        else:
            # Overdue - no payment, but set due_date in the past
            frappe.db.set_value("Fees", fee_name, "due_date", str(add_days(today(), -random.randint(15, 45))))
            frappe.db.commit()
            continue

        if pay_amount <= 0:
            continue

        # Check if payment already exists
        existing_pay = frappe.db.exists("Fee Payment", {"fees": fee_name})
        if existing_pay:
            continue

        # Create Fee Payment as draft
        doc = frappe.get_doc({
            "doctype": "Fee Payment",
            "fees": fee_name,
            "student": fee.student,
            "payment_date": str(add_days(today(), -random.randint(1, 30))),
            "amount": pay_amount,
            "payment_mode": random.choice(["Cash", "Bank Transfer", "UPI", "Card"]),
            "reference_number": f"DEMO-REF-{random.randint(10000, 99999)}",
        })
        doc.insert(ignore_permissions=True)

        # Update parent Fees directly via SQL to avoid read-only constraint
        new_paid = float(fee.paid_amount or 0) + pay_amount
        new_outstanding = max(0, float(fee.total_amount) - new_paid - float(fee.discount_amount or 0))
        frappe.db.sql("""
            UPDATE `tabFees`
            SET paid_amount = %s, outstanding_amount = %s, status = %s
            WHERE name = %s
        """, (new_paid, new_outstanding, new_status, fee_name))
        pay_count += 1

        # Fee Discounts (a few)
        if i < 5 and random.random() < 0.4:
            disc_val = random.choice([500, 1000, 5, 10])
            disc_type = random.choice(["Percentage", "Fixed Amount"])
            disc_amount = (float(fee.total_amount) * disc_val) / 100 if disc_type == "Percentage" else disc_val
            new_outstanding2 = max(0, float(fee.total_amount) - new_paid - disc_amount)
            frappe.db.sql("""
                UPDATE `tabFees`
                SET discount_amount = %s, outstanding_amount = %s
                WHERE name = %s
            """, (disc_amount, new_outstanding2, fee_name))
            disc_count += 1

    frappe.db.commit()
    print(f"  Fee Payments: {pay_count}")
    print(f"  Fee Discounts: {disc_count}")


# ─── PHASE 7: Library ───────────────────────────────────────────────────────

def generate_library(students_data):
    print("\n[Phase 7] Book Categories, Library Items, Memberships, Transactions...")

    # Book Categories
    categories = {}
    for cname in ["Computer Science", "Commerce", "Management", "English Literature", "General Reference"]:
        cid = _get_or_create("Book Category", {"category_name": cname},
            {"category_name": cname, "description": f"{cname} books"})
        categories[cname] = cid
    frappe.db.commit()

    # Library Items
    items = {}
    for title, author, isbn, cat, pub, edition, year, copies in BOOK_DATA:
        existing = frappe.db.get_value("Library Item", {"isbn": isbn}, "name")
        if existing:
            items[isbn] = existing
            continue

        doc = frappe.get_doc({
            "doctype": "Library Item",
            "title": title,
            "author": author,
            "isbn": isbn,
            "book_category": cat,
            "publisher": pub,
            "edition": edition,
            "published_year": year,
            "total_copies": copies,
        })
        doc.insert(ignore_permissions=True)
        items[isbn] = doc.name
    frappe.db.commit()
    print(f"  Library Items: {len(items)}")

    # Library Memberships for ~60% of active students
    active_students = frappe.get_all("Student", filters={"status": "Active"}, pluck="name")
    members = {}
    for student in active_students[:45]:
        existing = frappe.db.get_value("Library Membership", {"student": student}, "name")
        if existing:
            members[student] = existing
            continue
        doc = frappe.get_doc({
            "doctype": "Library Membership",
            "student": student,
            "issue_date": str(add_days(today(), -120)),
            "valid_upto": str(add_days(today(), 180)),
            "max_books_allowed": 3,
        })
        doc.insert(ignore_permissions=True)
        members[student] = doc.name
    frappe.db.commit()
    print(f"  Library Memberships: {len(members)}")

    # Library Transactions - mix of issued and returned
    item_list = list(items.values())
    tx_count = 0
    fine_count = 0

    for student, mem_name in list(members.items())[:30]:
        num_borrows = random.randint(1, 2)
        for _ in range(num_borrows):
            item = random.choice(item_list)

            existing_open = frappe.db.exists("Library Transaction", {
                "student": student, "library_item": item, "status": "Issued"
            })
            if existing_open:
                continue

            avail = frappe.db.get_value("Library Item", item, "available_copies")
            if not avail or avail <= 0:
                continue

            issue_date = str(_random_date_in_range(8, 2))
            due_date = str(add_days(getdate(issue_date), 14))

            try:
                issue_doc = frappe.get_doc({
                    "doctype": "Library Transaction",
                    "student": student,
                    "library_item": item,
                    "transaction_type": "Issue",
                    "transaction_date": issue_date,
                    "due_date": due_date,
                })
                issue_doc.insert(ignore_permissions=True)
                issue_doc.submit()
                tx_count += 1
            except Exception:
                continue

            # 70% returned, 30% still issued
            if random.random() < 0.70:
                return_date = str(add_days(getdate(issue_date), random.randint(10, 25)))
                is_late = getdate(return_date) > getdate(due_date)

                return_doc = frappe.get_doc({
                    "doctype": "Library Transaction",
                    "student": student,
                    "library_item": item,
                    "transaction_type": "Return",
                    "transaction_date": return_date,
                    "return_date": return_date,
                    "due_date": due_date,
                })
                return_doc.insert(ignore_permissions=True)
                return_doc.submit()
                tx_count += 1

                if is_late:
                    fine_count += 1

    frappe.db.commit()
    print(f"  Library Transactions: {tx_count}")
    print(f"  With fines (overdue): {fine_count}")


# ─── PHASE 8: Hostel ────────────────────────────────────────────────────────

def generate_hostel(students_data):
    print("\n[Phase 8] Hostels, Rooms, Allocations...")

    # Hostels
    hostel_data = [
        ("Sunrise Hostel", "Boys", "Dr. Priya Sharma", "123 College Road, Chennai"),
        ("Moonlight Hostel", "Girls", "Prof. Deepak Nair", "456 University Avenue, Chennai"),
    ]
    hostels = {}
    for hname, htype, warden, addr in hostel_data:
        existing = frappe.db.get_value("Hostel", {"hostel_name": hname}, "name")
        if existing:
            hostels[hname] = existing
            continue
        # Find instructor for warden
        warden_inst = frappe.db.get_value("Instructor", {"instructor_name": warden}, "name")
        doc = frappe.get_doc({
            "doctype": "Hostel",
            "hostel_name": hname,
            "hostel_type": htype,
            "warden": warden_inst,
            "address": addr,
        })
        doc.insert(ignore_permissions=True)
        hostels[hname] = doc.name
    frappe.db.commit()
    print(f"  Hostels: {list(hostels.keys())}")

    # Rooms
    rooms = {}
    room_configs = [
        ("Sunrise Hostel", [
            ("A-101", "Single", 1), ("A-102", "Single", 1), ("A-103", "Double", 2),
            ("A-104", "Double", 2), ("A-105", "Dormitory", 6),
            ("B-201", "Single", 1), ("B-202", "Double", 2), ("B-203", "Double", 2),
            ("B-204", "Dormitory", 6), ("B-205", "Dormitory", 6),
        ]),
        ("Moonlight Hostel", [
            ("C-101", "Single", 1), ("C-102", "Single", 1), ("C-103", "Double", 2),
            ("C-104", "Double", 2), ("C-105", "Dormitory", 6),
            ("D-201", "Single", 1), ("D-202", "Double", 2), ("D-203", "Double", 2),
            ("D-204", "Dormitory", 6),
        ]),
    ]
    for hname, hrooms in room_configs:
        hid = hostels[hname]
        for rnum, rtype, cap in hrooms:
            existing = frappe.db.get_value("Hostel Room", {"hostel": hid, "room_number": rnum}, "name")
            if existing:
                rooms[f"{hname}-{rnum}"] = existing
                continue
            doc = frappe.get_doc({
                "doctype": "Hostel Room",
                "hostel": hid,
                "room_number": rnum,
                "room_type": rtype,
                "capacity": cap,
            })
            doc.insert(ignore_permissions=True)
            rooms[f"{hname}-{rnum}"] = doc.name
    frappe.db.commit()
    print(f"  Hostel Rooms: {len(rooms)}")

    # Allocations for ~35% of active students
    active_students = frappe.get_all("Student", filters={"status": "Active"}, pluck="name")
    alloc_count = 0
    room_list = list(rooms.values())

    for student in active_students[:25]:
        existing = frappe.db.get_value("Hostel Room Allocation",
            {"student": student, "status": "Active"}, "name")
        if existing:
            alloc_count += 1
            continue

        room = random.choice(room_list)
        try:
            doc = frappe.get_doc({
                "doctype": "Hostel Room Allocation",
                "student": student,
                "hostel_room": room,
                "allocation_date": str(add_days(today(), -random.randint(30, 90))),
            })
            doc.insert(ignore_permissions=True)
            alloc_count += 1
        except Exception:
            pass  # Room might be full

    frappe.db.commit()
    print(f"  Hostel Room Allocations: {alloc_count}")


# ─── PHASE 9: Transport ─────────────────────────────────────────────────────

def generate_transport(students_data):
    print("\n[Phase 9] Vehicles, Routes, Allocations...")

    # Vehicles
    vehicle_data = [
        ("TN-01-AB-1234", 40, "Ramanathan K.", "+91-9876543210"),
        ("TN-01-CD-5678", 35, "Selvam M.", "+91-9876543211"),
        ("TN-01-EF-9012", 50, "Murugan S.", "+91-9876543212"),
        ("TN-01-GH-3456", 30, "Anand P.", "+91-9876543213"),
        ("TN-01-IJ-7890", 45, "Venkatesh R.", "+91-9876543214"),
    ]
    vehicles = {}
    for vnum, cap, dname, dphone in vehicle_data:
        existing = frappe.db.get_value("Vehicle", {"vehicle_number": vnum}, "name")
        if existing:
            vehicles[vnum] = existing
            continue
        doc = frappe.get_doc({
            "doctype": "Vehicle",
            "vehicle_number": vnum,
            "capacity": cap,
            "driver_name": dname,
            "driver_phone": dphone,
            "status": "Active",
        })
        doc.insert(ignore_permissions=True)
        vehicles[vnum] = doc.name
    frappe.db.commit()
    print(f"  Vehicles: {len(vehicles)}")

    # Routes with stops
    route_data = [
        ("Route A - T. Nagar", "TN-01-AB-1234", 8000, [
            ("T. Nagar Bus Stand", 1, "07:30:00"),
            ("Adyar Gate", 2, "07:45:00"),
            ("College Main Gate", 3, "08:15:00"),
        ]),
        ("Route B - Velachery", "TN-01-CD-5678", 7500, [
            ("Velachery Metro", 1, "07:15:00"),
            ("Guindy Junction", 2, "07:40:00"),
            ("College Main Gate", 3, "08:10:00"),
        ]),
        ("Route C - Tambaram", "TN-01-EF-9012", 9000, [
            ("Tambaram Bus Depot", 1, "06:45:00"),
            ("Chrompet", 2, "07:05:00"),
            ("Pallavaram", 3, "07:25:00"),
            ("College Main Gate", 4, "08:00:00"),
        ]),
        ("Route D - Anna Nagar", "TN-01-GH-3456", 8500, [
            ("Anna Nagar West", 1, "07:00:00"),
            ("Aminjikarai", 2, "07:20:00"),
            ("College Main Gate", 3, "08:00:00"),
        ]),
        ("Route E - OMR", "TN-01-IJ-7890", 7000, [
            ("Thiruvanmiyur", 1, "07:10:00"),
            ("Sholinganallur", 2, "07:30:00"),
            ("College Main Gate", 3, "08:05:00"),
        ]),
    ]
    routes = {}
    for rname, vnum, fee, stops in route_data:
        existing = frappe.db.get_value("Transport Route", {"route_name": rname}, "name")
        if existing:
            routes[rname] = existing
            continue
        doc = frappe.get_doc({
            "doctype": "Transport Route",
            "route_name": rname,
            "vehicle": vehicles[vnum],
            "fee_amount": fee,
            "stops": [{"stop_name": s[0], "stop_order": s[1], "pickup_time": s[2]} for s in stops],
        })
        doc.insert(ignore_permissions=True)
        routes[rname] = doc.name
    frappe.db.commit()
    print(f"  Transport Routes: {len(routes)}")

    # Allocations for ~25% of active students
    active_students = frappe.get_all("Student", filters={"status": "Active"}, pluck="name")
    route_list = list(routes.values())
    alloc_count = 0

    for student in active_students[:18]:
        existing = frappe.db.get_value("Student Transport Allocation",
            {"student": student, "status": "Active"}, "name")
        if existing:
            alloc_count += 1
            continue

        route = random.choice(route_list)
        route_doc = frappe.get_doc("Transport Route", route)
        stops = [s.stop_name for s in route_doc.stops]
        pickup = stops[0] if stops else "College Main Gate"

        try:
            doc = frappe.get_doc({
                "doctype": "Student Transport Allocation",
                "student": student,
                "transport_route": route,
                "pickup_stop": pickup,
                "allocation_date": str(add_days(today(), -60)),
            })
            doc.insert(ignore_permissions=True)
            alloc_count += 1
        except Exception:
            pass  # Vehicle might be full

    frappe.db.commit()
    print(f"  Student Transport Allocations: {alloc_count}")


# ─── PHASE 10: Communication ─────────────────────────────────────────────────

def generate_communication(students_data):
    print("\n[Phase 10] Notices, Feedback...")

    programs = frappe.get_all("Program", pluck="name")
    groups = students_data["student_groups"]
    active_students = frappe.get_all("Student", filters={"status": "Active"}, pluck="name")
    student_emails = frappe.get_all("Student", filters={"status": "Active"}, fields=["name", "email_address"])

    # Notices
    notice_data = [
        ("Semester Examination Schedule Released", "All", None, None,
         "<p>The schedule for Even Semester examinations has been released. Please check the examination notice board for detailed timetables.</p>"),
        ("Annual Day Celebration", "All", None, None,
         "<p>The Annual Day Celebration will be held on 15th March 2027. All students are cordially invited to attend.</p>"),
        ("B.Sc CS - Hackathon Registration Open", "Student Group-wise", None,
         "B.Sc Computer Science - Programming in C - Term 1",
         "<p>Registration for the inter-college hackathon is now open. Teams of 3-4 members can register through the CS department.</p>"),
        ("B.Com - Industrial Visit to Factory", "Program-wise", "B.Com", None,
         "<p>B.Com students will visit manufacturing units on 20th February. Consent forms must be submitted by 15th February.</p>"),
        ("Library Hours Extended During Exams", "All", None, None,
         "<p>The library will remain open until 8 PM during the examination period starting March 1st.</p>"),
        ("Hostel Mess Menu Update", "All", None, None,
         "<p>The hostel mess menu has been updated based on student feedback. New menu effective from next Monday.</p>"),
        ("BBA - Placement Drive by TCS", "Program-wise", "BBA", None,
         "<p>TCS campus placement drive for BBA students will be conducted on 25th February. Pre-placement talk at 10 AM.</p>"),
        ("Sports Day - Inter-Department Tournament", "All", None, None,
         "<p>Annual sports day will be conducted on 10th March. Events include cricket, football, badminton, and athletics.</p>"),
        ("B.A. English - Literary Fest", "Program-wise", "B.A. English", None,
         "<p>The annual literary fest 'Wordsmith' will be held on 5th March. Events include debate, poetry recitation, and creative writing.</p>"),
        ("Fee Payment Deadline Reminder", "All", None, None,
         "<p>This is a reminder that the last date for fee payment without late fee is 15th February. Please clear your dues promptly.</p>"),
    ]

    for title, aud_type, target_prog, target_group, body in notice_data:
        existing = frappe.db.get_value("Notice", {"title": title}, "name")
        if existing:
            continue

        doc = frappe.get_doc({
            "doctype": "Notice",
            "title": title,
            "body": body,
            "audience_type": aud_type,
            "target_program": target_prog if aud_type == "Program-wise" else None,
            "target_student_group": target_group if aud_type == "Student Group-wise" else None,
            "publish_date": str(add_days(today(), -random.randint(5, 30))),
            "status": "Published",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # Call dispatch_notice to create Communication Logs
        try:
            frappe.call("institution_erp.api.dispatch_notice", notice_name=doc.name)
        except Exception:
            pass

    notice_count = frappe.db.count("Notice")
    print(f"  Notices: {notice_count}")

    # Feedback
    feedback_data = [
        ("Wi-Fi connectivity issues in CS Lab", "Facility", "Open"),
        ("Request for additional library books on Python", "Academic", "In Progress"),
        ("Bus route C timing is too early", "Administrative", "Resolved"),
        ("Mess food quality needs improvement", "Facility", "Open"),
        ("Instructor not available during office hours", "Academic", "In Progress"),
        ("Sports equipment in bad condition", "Facility", "Resolved"),
        ("Request for placement training workshop", "Academic", "Open"),
        ("Hostel room maintenance issues", "Facility", "Open"),
        ("Exam schedule conflict with placement drive", "Administrative", "Closed"),
        ("Need more practice sessions for programming", "Academic", "In Progress"),
        ("Library AC not working properly", "Facility", "Resolved"),
        ("Suggestion for guest lecture series", "Academic", "Closed"),
        ("Transport bus frequency should increase", "Administrative", "Open"),
        ("Lab software needs updating", "Academic", "In Progress"),
        ("Canteen prices are too high", "Facility", "Closed"),
    ]

    fb_count = 0
    for subject, category, status in feedback_data:
        existing = frappe.db.get_value("Feedback", {"subject": subject}, "name")
        if existing:
            fb_count += 1
            continue

        student = random.choice(active_students[:20])
        fb_doc = frappe.get_doc({
            "doctype": "Feedback",
            "student": student,
            "category": category,
            "subject": subject,
            "description": f"<p>{subject}. This requires attention from the administration.</p>",
            "status": status,
            "raised_date": str(add_days(today(), -random.randint(1, 20))),
            "resolution_notes": "<p>Issue has been addressed.</p>" if status in ["Resolved", "Closed"] else None,
        })
        fb_doc.insert(ignore_permissions=True)
        fb_count += 1

    frappe.db.commit()
    print(f"  Feedback: {fb_count}")


# ─── PHASE 11: Admission Pipeline ───────────────────────────────────────────

def generate_admissions(academic, students_data):
    print("\n[Phase 11] Admission Inquiries, Student Applicants...")

    programs = academic["programs"]
    prog_list = list(programs.keys())

    # Admission Inquiries (15-20)
    inquiry_data = [
        ("Meera Krishnamurthy", "Female", "Father: Krishnamurthy T.", prog_list[0], "Open"),
        ("Rohan Deshpande", "Male", "Father: Anil Deshpande", prog_list[1], "Converted"),
        ("Shruti Agarwal", "Female", "Mother: Sunita Agarwal", prog_list[2], "Follow-up"),
        ("Karthik Subramanian", "Male", "Father: Subramanian V.", prog_list[3], "Open"),
        ("Nisha Rajan", "Female", "Father: Rajan P.", prog_list[0], "Converted"),
        ("Amitabh Bose", "Male", "Father: Sanjay Bose", prog_list[1], "Closed"),
        ("Pooja Venkatesh", "Female", "Mother: Lakshmi Venkatesh", prog_list[2], "Open"),
        ("Rajat Malhotra", "Male", "Father:.VK Malhotra", prog_list[0], "Converted"),
        ("Divya Nair", "Female", "Father: Gopinath Nair", prog_list[3], "Follow-up"),
        ("Vikram Thakur", "Male", "Father: Rajesh Thakur", prog_list[1], "Open"),
        ("Sneha Kulkarni", "Female", "Mother: Asha Kulkarni", prog_list[2], "Converted"),
        ("Aditya Rao", "Male", "Father: Mohan Rao", prog_list[0], "Open"),
        ("Meghna Banerjee", "Female", "Father: Pranab Banerjee", prog_list[3], "Closed"),
        ("Siddharth Jain", "Male", "Father: Mahaveer Jain", prog_list[1], "Follow-up"),
        ("Ankita Chatterjee", "Female", "Mother: Rita Chatterjee", prog_list[2], "Converted"),
        ("Prateek Sinha", "Male", "Father: Ashok Sinha", prog_list[0], "Open"),
        ("Ishita Bhatt", "Female", "Father: Navin Bhatt", prog_list[3], "Open"),
        ("Nikhil Gupta", "Male", "Father: Ramesh Gupta", prog_list[1], "Converted"),
    ]

    for name, gender, remarks, program, status in inquiry_data:
        existing = frappe.db.get_value("Admission Inquiry", {"applicant_name": name}, "name")
        if existing:
            continue

        doc = frappe.get_doc({
            "doctype": "Admission Inquiry",
            "applicant_name": name,
            "date_of_birth": f"{random.choice([2004,2005,2006])}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "gender": gender,
            "guardian_name": name.split()[0] + "'s Parent",
            "guardian_phone": _indian_phone(),
            "program_interested": program,
            "source": random.choice(["Website", "Walk-in", "Referral", "Advertisement"]),
            "inquiry_date": str(add_days(today(), -random.randint(1, 45))),
            "status": status,
            "remarks": remarks,
        })
        doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Admission Inquiries: {frappe.db.count('Admission Inquiry')}")

    # Student Applicants (10-15)
    applicant_data = [
        ("Aditi Varma", "Female", prog_list[0], "Approved", "Approved"),
        ("Rahul Bhat", "Male", prog_list[1], "Approved", "Approved"),
        ("Tanvi Kulkarni", "Female", prog_list[2], "Under Review", "Under Review"),
        ("Siddharth Pillai", "Male", prog_list[3], "Approved", "Approved"),
        ("Riya Menon", "Female", prog_list[0], "Applied", "Applied"),
        ("Karan Bajaj", "Male", prog_list[1], "Under Review", "Under Review"),
        ("Pallavi Deshmukh", "Female", prog_list[2], "Rejected", "Rejected"),
        ("Mohit Srivastava", "Male", prog_list[0], "Waitlisted", "Waitlisted"),
        ("Nandini Hegde", "Female", prog_list[3], "Applied", "Applied"),
        ("Tarun Chopra", "Male", prog_list[1], "Approved", "Approved"),
        ("Sonal Dixit", "Female", prog_list[2], "Under Review", "Under Review"),
        ("Arvind Kejriwal", "Male", prog_list[0], "Draft", "Draft"),
        ("Meghna Chakraborty", "Female", prog_list[3], "Approved", "Approved"),
    ]

    for name, gender, program, status, wf_state in applicant_data:
        existing = frappe.db.get_value("Student Applicant", {"applicant_name": name}, "name")
        if existing:
            continue

        doc = frappe.get_doc({
            "doctype": "Student Applicant",
            "applicant_name": name,
            "date_of_birth": f"{random.choice([2004,2005,2006])}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "gender": gender,
            "program": program,
            "academic_year": academic["ay_current"],
            "guardian_name": name.split()[0] + "'s Parent",
            "guardian_email": f"{name.split()[0].lower()}@{DEMO_EMAIL_DOMAIN}",
            "guardian_phone": _indian_phone(),
            "previous_school": random.choice([
                "Delhi Public School", "Kendriya Vidyalaya", "D.A.V. Public School",
                "St. Xavier's School", "Ryan International School",
            ]),
            "previous_school_marks": round(random.uniform(60, 95), 1),
            "application_date": str(add_days(today(), -random.randint(1, 30))),
            "status": "Applied",
        })
        doc.insert(ignore_permissions=True)

        # Update status and workflow_state via SQL to bypass workflow validation
        if status != "Applied":
            frappe.db.sql("""
                UPDATE `tabStudent Applicant`
                SET status = %s, workflow_state = %s
                WHERE name = %s
            """, (status, wf_state, doc.name))

    frappe.db.commit()
    print(f"  Student Applicants: {frappe.db.count('Student Applicant')}")


# ─── PHASE 12: Demo Users ───────────────────────────────────────────────────

def generate_demo_users(students_data, academic):
    print("\n[Phase 12] Demo User Accounts...")

    # Disable background job queuing to avoid QueueOverloaded
    _real_enqueue = frappe.enqueue
    frappe.enqueue = lambda *a, **kw: None

    # Staff Users
    staff_accounts = [
        ("admissions@demo.institution.local", "Admissions Officer", "Admissions"),
        ("academichead@demo.institution.local", "Academic Head", "Academic"),
        ("instructor1@demo.institution.local", "Instructor", "Instructor 1"),
        ("instructor2@demo.institution.local", "Instructor", "Instructor 2"),
        ("feemanager@demo.institution.local", "Fee Manager", "Finance"),
        ("facilitymanager@demo.institution.local", "Facility Manager", "Facilities"),
        ("comms.officer@demo.institution.local", "Communication Officer", "Communications"),
    ]

    for email, role, first_name in staff_accounts:
        existing = frappe.db.exists("User", email)
        if existing:
            # Ensure role is assigned
            user = frappe.get_doc("User", email)
            role_names = [r.role for r in user.roles]
            if role not in role_names:
                user.append("roles", {"role": role})
                user.save(ignore_permissions=True)
            continue

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "user_type": "System User",
            "send_welcome_email": 0,
        })
        user.append("roles", {"role": role})
        user.insert(ignore_permissions=True)
        user.new_password = DEMO_PASSWORD
        user.save(ignore_permissions=True)
    frappe.db.commit()

    # Admin user
    admin_email = "admin@demo.institution.local"
    if not frappe.db.exists("User", admin_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": admin_email,
            "first_name": "Administrator",
            "user_type": "System User",
            "send_welcome_email": 0,
        })
        user.append("roles", {"role": "System Manager"})
        user.insert(ignore_permissions=True)
        user.new_password = DEMO_PASSWORD
        user.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Staff/Admin accounts: {len(staff_accounts) + 1}")

    # Student portal users - pick specific students for demo
    active_students = frappe.get_all("Student", filters={"status": "Active"},
        fields=["name", "first_name", "last_name", "email_address", "program"],
        order_by="name asc")

    # "Rich" demo student - first active student
    rich_student = active_students[0] if active_students else None
    demo_students = []

    # Pick 3 students for demo
    pick_indices = [0, min(5, len(active_students)-1), min(10, len(active_students)-1)]
    for idx in pick_indices:
        if idx < len(active_students):
            demo_students.append(active_students[idx])

    for student in demo_students:
        email = f"student{demo_students.index(student)+1}@{DEMO_EMAIL_DOMAIN}"
        existing = frappe.db.exists("User", email)
        if existing:
            # Ensure Student role and permissions
            user = frappe.get_doc("User", email)
            role_names = [r.role for r in user.roles]
            if "Student" not in role_names:
                user.append("roles", {"role": "Student"})
                user.save(ignore_permissions=True)
            continue

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": student.first_name,
            "last_name": student.last_name or "",
            "user_type": "Website User",
            "send_welcome_email": 0,
        })
        user.append("roles", {"role": "Student"})
        user.insert(ignore_permissions=True)
        user.new_password = DEMO_PASSWORD
        user.save(ignore_permissions=True)

        # Add User Permission
        existing_perm = frappe.db.exists("User Permission", {
            "user": email, "allow": "Student", "for_value": student.name
        })
        if not existing_perm:
            frappe.get_doc({
                "doctype": "User Permission",
                "user": email,
                "allow": "Student",
                "for_value": student.name,
            }).insert(ignore_permissions=True)
    frappe.db.commit()

    # Guardian portal users - pick guardians linked to 2+ students
    guardians_with_multi = {}
    all_students = frappe.get_all("Student", filters={"status": "Active"}, fields=["name", "guardian"])
    for s in all_students:
        g = s.guardian
        if g not in guardians_with_multi:
            guardians_with_multi[g] = []
        guardians_with_multi[g].append(s.name)

    multi_guardians = [(g, studs) for g, studs in guardians_with_multi.items() if len(studs) >= 2]
    demo_guardians = multi_guardians[:2] if len(multi_guardians) >= 2 else list(guardians_with_multi.items())[:2]

    for i, (guardian_name, linked_students) in enumerate(demo_guardians):
        g_email = frappe.db.get_value("Guardian", guardian_name, "guardian_email")
        if not g_email:
            continue

        user_email = f"guardian{i+1}@{DEMO_EMAIL_DOMAIN}"
        existing = frappe.db.exists("User", user_email)
        if existing:
            user = frappe.get_doc("User", user_email)
            role_names = [r.role for r in user.roles]
            if "Guardian" not in role_names:
                user.append("roles", {"role": "Guardian"})
                user.save(ignore_permissions=True)
            continue

        user = frappe.get_doc({
            "doctype": "User",
            "email": user_email,
            "first_name": frappe.db.get_value("Guardian", guardian_name, "guardian_name").split()[0],
            "user_type": "Website User",
            "send_welcome_email": 0,
        })
        user.append("roles", {"role": "Guardian"})
        user.insert(ignore_permissions=True)
        user.new_password = DEMO_PASSWORD
        user.save(ignore_permissions=True)

        # User Permissions for Guardian + linked Students
        existing_perm = frappe.db.exists("User Permission", {
            "user": user_email, "allow": "Guardian", "for_value": guardian_name
        })
        if not existing_perm:
            frappe.get_doc({
                "doctype": "User Permission",
                "user": user_email,
                "allow": "Guardian",
                "for_value": guardian_name,
            }).insert(ignore_permissions=True)

        for s in linked_students:
            existing_perm = frappe.db.exists("User Permission", {
                "user": user_email, "allow": "Student", "for_value": s
            })
            if not existing_perm:
                frappe.get_doc({
                    "doctype": "User Permission",
                    "user": user_email,
                    "allow": "Student",
                    "for_value": s,
                }).insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.enqueue = _real_enqueue
    print(f"  Student portal accounts: {len(demo_students)}")
    print(f"  Guardian portal accounts: {len(demo_guardians)}")

    return {"demo_students": demo_students, "demo_guardians": demo_guardians}


# ─── MAIN ────────────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("GENERATING DEMO DATA FOR INSTITUTION ERP")
    print("=" * 60)

    random.seed(42)

    academic = generate_academic_data()
    students_data = generate_students_and_guardians(academic)
    generate_schedules(academic, students_data)
    generate_attendance(academic, students_data)
    generate_examination(academic, students_data)
    generate_fees(academic, students_data)
    generate_library(students_data)
    generate_hostel(students_data)
    generate_transport(students_data)
    generate_communication(students_data)
    generate_admissions(academic, students_data)
    demo_users = generate_demo_users(students_data, academic)

    # Summary
    print("\n" + "=" * 60)
    print("DEMO DATA GENERATION COMPLETE")
    print("=" * 60)
    counts = {
        "Academic Year": frappe.db.count("Academic Year"),
        "Academic Term": frappe.db.count("Academic Term"),
        "Program": frappe.db.count("Program"),
        "Course": frappe.db.count("Course"),
        "Instructor": frappe.db.count("Instructor"),
        "Room": frappe.db.count("Room"),
        "Student": frappe.db.count("Student"),
        "Guardian": frappe.db.count("Guardian"),
        "Student Group": frappe.db.count("Student Group"),
        "Course Schedule": frappe.db.count("Course Schedule"),
        "Student Attendance": frappe.db.count("Student Attendance"),
        "Staff Attendance": frappe.db.count("Staff Attendance"),
        "Grading Scale": frappe.db.count("Grading Scale"),
        "Assessment Group": frappe.db.count("Assessment Group"),
        "Assessment Plan": frappe.db.count("Assessment Plan"),
        "Assessment Result": frappe.db.count("Assessment Result"),
        "Fee Category": frappe.db.count("Fee Category"),
        "Fee Structure": frappe.db.count("Fee Structure"),
        "Fee Schedule": frappe.db.count("Fee Schedule"),
        "Fees": frappe.db.count("Fees"),
        "Fee Payment": frappe.db.count("Fee Payment"),
        "Fee Discount": frappe.db.count("Fee Discount"),
        "Library Item": frappe.db.count("Library Item"),
        "Library Membership": frappe.db.count("Library Membership"),
        "Library Transaction": frappe.db.count("Library Transaction"),
        "Hostel": frappe.db.count("Hostel"),
        "Hostel Room": frappe.db.count("Hostel Room"),
        "Hostel Room Allocation": frappe.db.count("Hostel Room Allocation"),
        "Vehicle": frappe.db.count("Vehicle"),
        "Transport Route": frappe.db.count("Transport Route"),
        "Student Transport Allocation": frappe.db.count("Student Transport Allocation"),
        "Notice": frappe.db.count("Notice"),
        "Notice Recipient": frappe.db.count("Notice Recipient"),
        "Communication Log": frappe.db.count("Communication Log"),
        "Feedback": frappe.db.count("Feedback"),
        "Admission Inquiry": frappe.db.count("Admission Inquiry"),
        "Student Applicant": frappe.db.count("Student Applicant"),
    }
    for dt, cnt in counts.items():
        print(f"  {dt}: {cnt}")
    print("=" * 60)
