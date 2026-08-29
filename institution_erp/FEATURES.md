# Features — Institution ERP

A complete guide to every feature in the Institution ERP system, built for **Bannari Amman Institute of Technology (BIT)**.

---

## Table of Contents

1. [Student Information Management](#1-student-information-management)
2. [Guardian Management](#2-guardian-management)
3. [Admissions Pipeline](#3-admissions-pipeline)
4. [Academic Structure](#4-academic-structure)
5. [Course Scheduling](#5-course-scheduling)
6. [Attendance Tracking](#6-attendance-tracking)
7. [Examinations & Grading](#7-examinations--grading)
8. [Fee Management](#8-fee-management)
9. [Library Management](#9-library-management)
10. [Hostel Management](#10-hostel-management)
11. [Transport Management](#11-transport-management)
12. [Communication & Notices](#12-communication--notices)
13. [Feedback & Complaints](#13-feedback--complaints)
14. [Student Portal](#14-student-portal)
15. [Guardian Portal](#15-guardian-portal)
16. [Staff Cockpits](#16-staff-cockpits)
17. [Reports & Dashboards](#17-reports--dashboards)
18. [Role-Based Access Control](#18-role-based-access-control)
19. [Institutional Dashboard](#19-institutional-dashboard)
20. [Demo Data System](#20-demo-data-system)

---

## 1. Student Information Management

**What it does:** Maintains a complete, searchable record of every student in the institution — from the moment they apply until they graduate or leave.

**How it works:**

- Every student gets a unique ID (format: `STU-2026-00001`) automatically when they are created
- Each student record stores their full name, date of birth, gender, email address, program enrollment, and linked guardian
- Students have a **status** field: Active, Inactive, or Graduated — this is used throughout the system to filter and report on current students
- The system currently holds **79 students** across 6 programs (B.Sc Computer Science, B.Com, BBA, B.A. English, BCA, MBA)

**Why it matters:**

Without a central student record, every department (admissions, academics, fees, library) would maintain separate lists that get out of sync. This single source of truth means every module in the system can look up the same student and trust the data.

---

## 2. Guardian Management

**What it does:** Links parents or guardians to their children's student records, enabling them to monitor academic progress, attendance, fees, and library activity through a dedicated portal.

**How it works:**

- Each guardian record stores the guardian's name, email, phone number, and relationship to the student (Father, Mother, Guardian)
- A guardian can be linked to **multiple students** (e.g., a parent with two children enrolled)
- When a guardian portal account is created, the system automatically grants them visibility into **all linked students' records** — attendance, results, fees, library, and notices
- Guardian records are auto-created when a Student Applicant is approved through the admissions pipeline

**Why it matters:**

Parents need to monitor their children's progress without needing their login credentials. The guardian portal gives them a read-only view of everything — grades, attendance, fees owed — with the ability to switch between children from a single account.

---

## 3. Admissions Pipeline

**What it does:** Manages the complete journey from first enquiry to enrolled student — tracking every inquiry, application, entrance test, and approval decision in a structured workflow.

**How it works:**

The admissions process flows through five stages:

1. **Admission Inquiry** — A prospective student or parent makes an enquiry. The system records their name, contact details, program of interest, and how they heard about the institution (source). Each inquiry gets a unique ID (`ADM-INQ-2026-0001`).

2. **Student Applicant** — If the inquiry converts, a formal application is created. The applicant provides documents, selects a program, and enters a workflow with four states:
   - **Draft** — Application being prepared
   - **Applied** — Formally submitted
   - **Under Review** — Being evaluated by the Admissions Officer
   - **Approved** — Accepted into the institution

3. **Entrance Test** — Optional assessments tied to specific programs. Tests have a date, maximum marks, and passing marks.

4. **Entrance Test Result** — Records the applicant's score. The system automatically calculates whether they passed or failed based on the test's passing marks threshold.

5. **Auto-Enrollment on Approval** — When an application is approved, the system automatically:
   - Creates a **Guardian** record (if one doesn't already exist)
   - Creates a **Student** record with status "Active"
   - Links the Guardian and Student together
   - No manual data entry required after approval

**The pipeline at a glance:**

```
Inquiry → Application → Entrance Test → Review → Approved → Auto-creates Student + Guardian
```

**Why it matters:**

Manual admissions processes lose inquiries, forget follow-ups, and require re-entering the same data multiple times. This pipeline ensures every inquiry is tracked, every application follows the same process, and approved students are immediately enrolled without duplicate data entry.

---

## 4. Academic Structure

**What it does:** Organizes the institution's academic offerings into a hierarchy of programs, courses, and academic years — the foundation that every other module depends on.

**How it works:**

- **Programs** — The degree or diploma offered (e.g., B.Sc Computer Science, B.A. English, MBA). Each program has a name, code, and department.
- **Courses** — Individual subjects within a program (e.g., "English Literature: Prose" within B.A. English). Each course has credits, a course type (Core, Elective, Lab), and belongs to exactly one program.
- **Academic Years** — Time periods (e.g., "2026-2027") that group terms, fee schedules, and assessment plans.
- **Academic Terms** — Subdivisions within a year (e.g., "Term 1", "Term 2") with start and end dates.
- **Rooms** — Physical spaces with building, floor, capacity, and room type (Classroom, Lab, Seminar Hall).

**The hierarchy:**

```
Program → Course → Student Group → Course Schedule
```

**Current data:** 6 programs, 17 courses, 2 academic years, 5 terms, and multiple rooms configured.

**Why it matters:**

Everything else in the system — attendance, assessments, fees, scheduling — references this structure. Without a clean academic hierarchy, you can't answer basic questions like "Which courses does this program have?" or "How many students are in this group?"

---

## 5. Course Scheduling

**What it does:** Creates and manages the timetable of when and where each course is taught, including which instructor teaches which group in which room at what time.

**How it works:**

- A **Course Schedule** links a course, student group, instructor, room, day of week, and time slot
- The system **prevents double-booking**: if Room A is scheduled for B.Sc CS on Monday 9-10 AM, no other course can use that room at the same time
- Similarly, an instructor cannot be assigned to two overlapping sessions
- **Student Groups** are subsets of a program's students (e.g., "B.A. English - Prose - Term 1") — attendance and assessments are tracked at the group level

**Current data:** 79 scheduled course sessions across all programs.

**Why it matters:**

Timetable conflicts are a common headache in institutions. The system's collision detection prevents two classes from being assigned the same room or instructor at the same time, eliminating scheduling errors before they happen.

---

## 6. Attendance Tracking

**What it does:** Records daily attendance for students in each course session, and for staff (instructors) — providing a complete attendance picture across the institution.

**How it works:**

### Student Attendance

- An instructor marks attendance for a student group on a specific date
- Each student is marked as **Present**, **Absent**, **Late**, or **Excused**
- The system prevents **duplicate attendance** — you cannot mark the same student twice for the same date and course schedule
- Bulk marking is supported: the instructor selects a group, picks a date, and marks all students at once
- Attendance is tracked at the **group level** — each student group has its own attendance records

### Staff Attendance

- Instructors and staff have their own attendance tracking
- Status options: **Present**, **Absent**, **Half Day**, **On Leave**
- Same duplicate-prevention logic applies

### What students see

- In the portal, students see their complete attendance history with colored badges (green for Present, red for Absent, amber for Late, purple for Excused)
- A summary shows total days, present count, absent count, and an **attendance percentage**
- The dashboard displays an SVG donut chart showing the attendance breakdown visually

**Current data:** 2,500+ attendance records across all groups.

**Why it matters:**

Attendance is often the first thing parents ask about. Instead of digging through paper registers or spreadsheets, instructors mark attendance in seconds and students/parents can see it instantly in the portal. The duplicate-prevention ensures data integrity.

---

## 7. Examinations & Grading

**What it does:** Manages the complete examination lifecycle — from defining grading scales and assessment plans to entering marks, calculating grades, and publishing results.

**How it works:**

### Grading Scale

- Defines how marks map to grades (e.g., 90-100% = A+, 80-89% = A, etc.)
- Each scale has multiple **Grading Intervals** with threshold percentages and grade codes
- The system prevents overlapping thresholds

### Assessment Group

- Groups related assessments together (e.g., "Term 1 Examinations")
- Has a **results_published** flag — this is the critical control that determines whether students can see their marks

### Assessment Plan

- Links a specific course, student group, grading scale, maximum marks, and passing marks
- Validates that passing marks are less than maximum marks

### Assessment Result (Marks Entry)

- An instructor enters marks for each student in a group
- Bulk entry is supported: select an assessment plan, enter marks for all students at once
- The system **automatically calculates the grade** based on the grading scale
- It **automatically determines Pass/Fail** based on whether marks meet the passing threshold
- **Duplicate prevention**: a student cannot have two results for the same assessment plan

### Results Publication Gating

This is a standout feature:

- When an Assessment Group has `results_published = 0`, students **cannot see their marks** in the portal — they see a blue banner saying "Results Not Yet Published"
- When an instructor or academic head sets `results_published = 1`, the marks instantly become visible to students
- This ensures students only see marks after the institution has officially reviewed and released them

**Current data:** 24 assessment plans, 300+ assessment results across all groups.

**Why it matters:**

Without publication gating, students would see marks the instant an instructor enters them — before grades are finalized, before other instructors have finished, before the institution has reviewed the results. The gating mechanism ensures a controlled, official release of results.

---

## 8. Fee Management

**What it does:** Handles the complete financial lifecycle — from defining fee structures and generating invoices to recording payments, applying discounts, and tracking outstanding dues.

**How it works:**

### Fee Category

- Classifies types of fees (e.g., "Tuition Fee", "Library Fine", "Hostel Fee")

### Fee Structure

- Defines what fees apply to a program for an academic year
- Contains multiple **Fee Components** (e.g., Tuition: ₹40,000 + Library: ₹2,000 + Lab: ₹5,000)
- The system automatically sums the components to calculate the total

### Fee Schedule

- Generates a list of students who should receive invoices from a fee structure
- Links to a specific student group and due date

### Fees (Invoice)

- The actual invoice sent to a student
- Tracks total amount, discount amount, paid amount, and **outstanding amount**
- Status is automatically computed: **Paid** (outstanding = 0), **Partial** (some paid), **Unpaid** (nothing paid), or **Overdue** (past due date with outstanding balance)
- The system **automatically recomputes** the paid amount and status every time a payment is made or the record is validated

### Fee Payment

- Records an individual payment against a fee invoice
- Validates that the payment amount does not exceed the outstanding balance
- On submission, automatically updates the parent Fee record's paid amount and status

### Fee Discount

- Allows applying discounts to fee invoices (percentage or fixed amount)
- Goes through an approval workflow: **Pending → Approved → Applied**
- When approved, the discount amount is automatically set on the linked Fee record

### Fee Dues Report

- A report that lists all fees with outstanding amounts, filterable by academic year, program, and status
- Helps the Fee Manager identify which students owe money

**Current data:** 51 fee records across all students.

**Why it matters:**

Fee management in institutions is error-prone — manually tracking who paid what, calculating outstanding balances, and applying discounts. This system automates the entire flow: when a payment is recorded, the invoice automatically updates. When a discount is approved, it's automatically applied. The Fee Dues Report gives instant visibility into outstanding collections.

---

## 9. Library Management

**What it does:** Manages the complete library operations — book catalog, student membership, issuing and returning books, and automatic fine calculation for overdue returns.

**How it works:**

### Book Catalog

- **Book Category** classifies books (e.g., "Fiction", "Textbook", "Reference")
- **Library Item** represents a specific book with title, author, ISBN, category, total copies, and **available copies**
- Available copies are automatically managed: decremented on issue, incremented on return

### Library Membership

- Each student must have an **active membership** to borrow books
- Membership specifies: maximum books allowed, validity period (start and end dates)
- The system checks that the membership hasn't expired before allowing a book issue

### Book Issue

- When a book is issued, the system validates:
  - Copies are available
  - The student has an active membership
  - The student hasn't exceeded their maximum books limit
- On successful issue, available copies are decremented

### Book Return

- When a book is returned, the system:
  - Validates that an open issue exists for that student and book
  - Calculates if the book is overdue (based on due date)
  - If overdue, calculates a **fine of ₹5 per day**
  - Increments available copies
  - If a fine applies, **automatically creates a Fees record** for the student

### What students see

- Currently checked-out books with due dates and Active/Overdue status
- Complete transaction history
- Overdue items highlighted in red

**Current data:** 34 library items, 5 active memberships, multiple transactions.

**Why it matters:**

Manual library management requires tracking who has which book, when it's due, and who owes fines. This system automates all of it — the available copy count is always accurate, overdue fines are calculated automatically, and students can see their library status in the portal without visiting the library desk.

---

## 10. Hostel Management

**What it does:** Manages hostel buildings, rooms, occupancy tracking, and student room allocations.

**How it works:**

### Hostel

- Represents a hostel building with name, type (Boys/Girls/Co-ed), warden, and total capacity
- Total capacity is **automatically recalculated** from the sum of all room capacities

### Hostel Room

- Individual rooms within a hostel with room number, type (Single/Double/Triple), capacity, and occupied count
- Occupied count is automatically managed as students are allocated or vacated

### Room Allocation

- Assigns a student to a specific room
- The system validates:
  - The room is not full
  - The student doesn't already have an active allocation
- When a student vacates, the occupied count is decremented

### What the Facility Manager sees

- Per-hostel occupancy bars showing occupied vs. total capacity
- Visual progress bars making it easy to see which hostels have availability

**Why it matters:**

Manual room allocation leads to overbooking and confusion about who is in which room. The system prevents over-allocation and gives instant visibility into occupancy across all hostels.

---

## 11. Transport Management

**What it does:** Manages the institution's transport system — vehicles, routes with pickup stops, and student route allocations.

**How it works:**

### Vehicle

- Registers each vehicle with number, capacity, driver name, driver phone, and status

### Transport Route

- Defines a route with a vehicle, list of stops (in order), and fee amount
- Each stop has a name, order number, and pickup time
- No duplicate stop order values are allowed

### Student Transport Allocation

- Assigns a student to a route
- Validates that the vehicle is not at full capacity
- One active allocation per student per route

**Why it matters:**

Transport coordinators need to know which students ride which routes, whether vehicles are at capacity, and what stops are on each route. This module provides all of that in one place.

---

## 12. Communication & Notices

**What it does:** Enables the institution to publish notices and announcements targeted to specific audiences, with tracking of who received and read each notice.

**How it works:**

### Notice

- Created with a title, body (rich text), and audience type
- **Audience targeting** supports five modes:
  - **All** — Every student receives the notice
  - **Program-wise** — Only students in a specific program
  - **Group-wise** — Only students in a specific student group
  - **Role-wise** — Only users with a specific role
  - **Individual** — A specific student
- When a notice is published, the system **automatically resolves the audience** and creates individual **Notice Recipient** records — one per targeted student
- Notices have publish and expiry dates, and a status (Draft, Published, Expired)

### Notice Recipient

- Tracks which student received which notice
- Records whether the student has read the notice (read_status, read_on timestamp)

### Communication Log

- When a notice is dispatched, Communication Log entries are created for each recipient
- Each log entry records: recipient type, recipient name, channel (Email/SMS), message summary, status, and sent timestamp

**Current data:** 10 published notices with 80+ recipients.

**Why it matters:**

Institutions need to communicate with students — exam schedules, holiday announcements, event notifications. Without audience targeting, every notice goes to everyone, creating noise. This system lets the Communication Officer send the right notice to the right people, and track who received it.

---

## 13. Feedback & Complaints

**What it does:** Provides a structured channel for students and guardians to submit feedback, complaints, or suggestions — and for the institution to track and resolve them.

**How it works:**

- Students and guardians can submit feedback through the portal
- Each submission includes: category (Academic, Facility, Service, General), subject, and detailed description
- Feedback goes through a lifecycle: **Open → In Progress → Resolved → Closed**
- When resolving or closing, the system requires **resolution notes** — ensuring every complaint has a documented resolution
- The Communication Officer sees a queue of open/pending feedback items
- The system tracks who submitted, when, and the current status

**Why it matters:**

Without a formal feedback system, complaints get lost in emails, phone calls, or hallway conversations. This system ensures every piece of feedback is recorded, assigned, tracked, and resolved — with a clear audit trail.

---

## 14. Student Portal

**What it does:** Gives every student a personal, secure dashboard showing their own attendance, results, fees, library status, notices, and feedback — accessible from any device.

**How it works:**

The portal is a modern single-page application (SPA) that loads once and navigates smoothly between sections without page reloads. It's accessible at `http://localhost:8000/institution-portal`.

### Pages available to students:

1. **Dashboard** — Overview with stat cards (attendance percentage, fee count, outstanding amount, library books), a visual donut chart for attendance, recent notices, and recent fee summaries

2. **Attendance** — Complete attendance history with summary statistics (total days, present, absent, late counts) and a percentage calculation. Each record shows date, group, and a colored status badge

3. **Results** — Assessment results displayed as cards showing course name, marks (e.g., "42 / 50"), grade, and Pass/Fail status. When results haven't been published by staff, a blue banner clearly states "Results Not Yet Published"

4. **Fees** — Fee invoices with amounts, paid amounts, outstanding amounts, and status badges (Paid in green, Partial in amber, Unpaid in red). Payment history shows each transaction with date, amount, method, and reference number

5. **Library** — Currently checked-out books displayed as cards with book title, issue date, due date, and Active/Overdue status (overdue highlighted in red). Transaction history shows all past issues and returns

6. **Notices** — Published notices displayed as expandable cards — click to read the full notice body. Shows date, title, and audience type

7. **Feedback** — Submit new feedback (category, subject, message) and view the status of previously submitted items

8. **Profile** — Student's personal information

### Key features:

- **Row-level security**: Each student can only see their own data — even if someone tried to access another student's records through the API, the system would block it
- **Responsive design**: Works on desktop, tablet, and mobile phones
- **Real-time data**: All data is fetched fresh from the server on each page load

**Why it matters:**

Instead of students lining up at the office to check their attendance or asking "What are my fees?" — they can check everything themselves, anytime, from their phone. This reduces administrative overhead and gives students ownership of their information.

---

## 15. Guardian Portal

**What it does:** Gives parents and guardians visibility into their children's academic life — attendance, results, fees, and library activity — from a single account.

**How it works:**

The guardian portal is identical to the student portal in layout and features, with one critical addition: the **Child Switcher**.

### Child Switcher

- A dropdown in the sidebar lists all children linked to the guardian
- Clicking a child's name instantly refreshes all data on the page to show that child's records
- A guardian with 2 children sees both names; clicking either switches the view
- The selected child is remembered across page navigation

### What guardians see:

- Same pages as students: Dashboard, Attendance, Results, Fees, Library, Notices, Feedback
- But the data is scoped to whichever child is currently selected
- A guardian cannot see data for students who are not linked to their guardian record

### Example:

Guardian "Arun Nair" has two children: Vedant Verma (B.Com) and Dhruv Reddy (B.A. English). When Arun logs in:
- He sees Vedant's attendance, results, and fees by default
- He clicks "Dhruv Reddy" in the child switcher
- All data updates to show Dhruv's records
- He can switch back and forth at any time

**Why it matters:**

Parents with multiple children enrolled need to monitor each child individually. Without the child switcher, they would need separate accounts for each child. This feature lets them see everything from one login, switching between children as easily as switching tabs.

---

## 16. Staff Cockpits

**What it does:** Gives each staff role a dedicated landing page showing the information and quick actions most relevant to their daily work — before they even open the full Desk.

**How it works:**

When a staff member logs in, they land on a **cockpit page** (not the generic Frappe Desk). This cockpit is customized for their specific role:

### Instructor Cockpit

- **Stats**: Number of students, assigned groups, today's classes, pending marks
- **Today's Classes**: List of today's sessions with Ongoing/Upcoming status
- **Quick Actions**: Mark Attendance, Enter Marks, View Assessment Plans
- **Pending Assessments**: Assessments that need marks entry, with due dates and an "Enter" button

### Fee Manager Cockpit

- **Stats**: Total outstanding amount, fee records count, payments today, pending discounts
- **Outstanding Fees**: List of fees with amounts and status badges
- **Quick Actions**: Record Payment, View All Fees, View Schedules
- **Pending Discounts**: Discount requests awaiting approval

### Facility Manager Cockpit

- **Stats**: Available books, active issues, overdue items (highlighted in red), hostel occupancy percentage
- **Quick Actions**: Issue Book, Return Book, View Hostel Allocations
- **Active Library Issues**: Currently issued books with due dates
- **Hostel Overview**: Per-hostel occupancy bars with visual progress indicators

### Communication Officer Cockpit

- **Stats**: Total notices, published notices, feedback queue count, communication logs
- **Quick Actions**: Create Notice, View All Notices, View Communication Logs
- **Recent Notices**: Latest notices with status indicators
- **Open Feedback**: Pending feedback items needing attention

### Admissions Officer Cockpit

- **Stats**: Total inquiries, open inquiries, under review, approved
- **Quick Actions**: New Inquiry, New Applicant, Review Applicants
- **Pipeline Funnel**: Visual 5-stage funnel showing Open → Applied → Review → Approved → Rejected
- **Recent Inquiries**: Latest inquiries with status badges

### Academic Head Cockpit

- **Stats**: Programs, students, average attendance, courses
- **Cross-Module Navigation**: Links to Students, Student Groups, Courses, Programs
- **Attendance Overview**: Per-group attendance percentages with color coding (green ≥ 80%, amber ≥ 60%, red < 60%)
- **Exam Performance**: Assessment completion status across groups

### System Manager (Admin) Cockpit

- **Stats**: Active students, staff members, average attendance, outstanding fees, programs, courses, open feedback, library active issues
- **Module Quick Access**: 8 icon links to key Desk modules (Students, Instructors, Fees, Attendance, Assessments, Library, Notices, Hostel)
- **Admissions Pipeline**: Active vs. Inactive student counts
- **System Health**: Total DocTypes, active users, open feedback (warning if > 0), outstanding fees (warning if > 0)

### Every cockpit includes:

- **"Open Full Desk" button** — Opens the full Frappe Desk in a new tab for complete CRUD operations on any DocType
- **Welcome banner** with personalized greeting and user name
- **Responsive design** — Works on desktop, tablet, and mobile

**Why it matters:**

The full Frappe Desk has hundreds of DocTypes and can be overwhelming for daily use. Cockpits distill each role's most important information and actions into a single, focused page. An instructor doesn't need to see Hostel management — they need to see today's classes and pending marks. A Fee Manager doesn't need to see Attendance — they need to see outstanding dues. Cockpits make the system feel purpose-built for each role, not generic.

---

## 17. Reports & Dashboards

**What it does:** Provides pre-built reports and visual dashboards for institutional analysis — no manual spreadsheet work needed.

### Script Reports (6)

1. **Fee Dues Report** — Lists all fees with outstanding amounts, filterable by academic year, program, and payment status. Helps identify which students owe money.

2. **Student Attendance Summary** — Shows attendance per student in a group with present, absent, late, total counts and percentages. Useful for identifying students with poor attendance.

3. **Student Result Summary** — Displays assessment results per student with marks, grade, percentage, and overall average. Helps academic heads understand class performance.

4. **Transport Route Utilization** — Shows student count per route with capacity utilization. Helps optimize transport routes.

5. **Library Circulation Report** — Lists library transactions with status (Issued, Returned, Overdue), filterable by student. Helps track library activity.

6. **Hostel Occupancy Report** — Shows room-by-room occupancy with capacity and available beds per hostel. Helps with room allocation decisions.

### Number Cards (5)

Visual summary cards on the Communication Dashboard:
- Total Active Students
- Total Outstanding Fees
- Books Currently Issued
- Hostel Occupancy (Rooms Occupied)
- Open Feedback/Complaints

### Dashboard Charts (2)

- **Fee Collection Trend** — Monthly sum of fee payments collected
- **Attendance Trend** — Monthly count of attendance records

### Institutional Dashboard

A custom dashboard combining the Number Cards and Charts into a single overview page, accessible from the Communication module.

**Why it matters:**

Raw data is useless without analysis. These reports and dashboards transform thousands of records into actionable insights — which students need attention, how much money is outstanding, how full are the hostels, and what's the attendance trend.

---

## 18. Role-Based Access Control

**What it does:** Ensures every user sees only the information they're authorized to see — students see their own data, guardians see their children's data, and staff see what their role permits.

**How it works:**

### Eight Custom Roles

| Role | Access Level | What They Can Do |
|------|-------------|-----------------|
| System Manager | Full access to everything | Institutional oversight, all modules |
| Academic Head | Read all, write academics/exam | Oversee academics, review results |
| Admissions Officer | Full CRUD on admissions | Manage inquiries, applications, approvals |
| Instructor | Attendance and assessment | Mark attendance, enter grades, view their groups |
| Fee Manager | Full CRUD on fees | Create structures, record payments, apply discounts |
| Facility Manager | Library, Hostel, Transport | Issue books, manage rooms, allocate transport |
| Communication Officer | Notices and feedback | Publish notices, manage feedback queue |
| Student | Portal only — read-only | View own attendance, results, fees, library |
| Guardian | Portal only — read-only | View linked children's data |

### How security is enforced

The system uses **two layers** of security:

1. **User Permissions** — When a portal user is created, the system creates permission records linking them to their own Student or Guardian record. This is the first filter.

2. **Row-Level Conditions** — For every database query, the system automatically adds a SQL filter:
   - Students: `WHERE student = '<their record>'`
   - Guardians: `WHERE student IN ('<child1>', '<child2>', ...)`
   - Staff: Filters based on their role and assigned groups

This means even if someone tried to access another student's data through a direct API call, the system would return empty results — the security is enforced at the database level, not just the UI.

### What this means in practice:

- A student logging in sees **only their own** attendance, results, fees, and library records
- A guardian sees **only their linked children's** records
- An instructor sees attendance and assessments **only for their assigned groups**
- A Fee Manager sees **all** fee records (their role allows full access)
- No student can ever see another student's grades, even by manipulating URLs or API calls

**Why it matters:**

Privacy and security are non-negotiable in an educational institution. A student's grades, attendance, and financial information are sensitive. This multi-layered security model ensures that data isolation is enforced at the deepest level — not just by hiding buttons in the UI, but by filtering database queries themselves.

---

## 19. Institutional Dashboard

**What it does:** Gives the System Manager and Communication Officer a bird's-eye view of the entire institution's health — student counts, financial status, library activity, and more — without navigating to individual modules.

**What it shows:**

- **Total Active Students** — How many students are currently enrolled
- **Total Outstanding Fees** — How much money is yet to be collected
- **Books Currently Issued** — Library utilization at a glance
- **Hostel Occupancy** — How many rooms are occupied
- **Open Feedback** — Number of unresolved complaints
- **Fee Collection Trend** — Monthly chart showing revenue collection over time
- **Attendance Trend** — Monthly chart showing attendance record counts

**Why it matters:**

Institutional leaders need quick answers to big questions: "How many students do we have?", "How much money is outstanding?", "Are students attending regularly?" This dashboard answers those questions in one glance, without requiring anyone to run reports or compile spreadsheets.

---

## 20. Demo Data System

**What it does:** Provides a complete, realistic dataset that makes the system feel alive during demonstrations — without requiring months of real data entry.

**What's included:**

- **79 students** across 6 programs
- **12 instructors** with course assignments
- **2,500+ attendance records** across all groups
- **300+ assessment results** with grades
- **51 fee records** with payment histories
- **34 library items** with transaction histories
- **10 published notices** with recipients
- **14 demo accounts** (8 staff + 4 students + 2 guardians) all with password `Demo@2026`

**Key demo accounts:**

| Account | What Makes It Special |
|---------|----------------------|
| `richdemo@demo.institution.local` (Student) | Fully populated — 50 attendance records, 6 results (some published, some not), fees, library transactions, feedback |
| `guardian1@demo.institution.local` (Guardian) | 2 children — demonstrates the child switcher feature |
| `admin@demo.institution.local` (System Manager) | Institution-wide overview with aggregate stats |

**Management commands:**

- Regenerate all demo data: `bench --site institution.localhost execute institution_erp.generate_demo_data.run`
- Remove all demo data: `bench --site institution.localhost execute institution_erp.reset_demo_data.run`

**Why it matters:**

A demo with an empty system is unimpressive. A demo with realistic data across all modules shows the system's true capabilities — the attendance charts have data to display, the fee reports have numbers to show, the library has books to issue. The demo data system makes this possible with a single command.

---

## Summary

| Feature Area | Key Capability | Users Who Benefit |
|-------------|---------------|-------------------|
| Student Management | Central student records with status tracking | All staff, Students, Guardians |
| Guardian Management | Multi-child portal access with child switcher | Parents, Guardians |
| Admissions Pipeline | Inquiry → Application → Approval → Auto-enrollment | Admissions Officers, Academic Heads |
| Academic Structure | Programs, Courses, Schedules with collision prevention | Instructors, Academic Heads |
| Attendance | Bulk marking, duplicate prevention, percentage calculation | Instructors, Students, Guardians |
| Examinations | Grading scales, bulk marks, results publication gating | Instructors, Students, Guardians |
| Fees | Auto-recomputing invoices, payment tracking, discount approval | Fee Managers, Students, Guardians |
| Library | Book issue/return, overdue fines, membership management | Facility Managers, Students |
| Hostel | Room allocation, occupancy tracking, capacity management | Facility Managers |
| Transport | Route management, vehicle allocation | Facility Managers |
| Communication | Audience-targeted notices, dispatch tracking | Communication Officers, Students |
| Feedback | Structured complaint tracking with resolution workflow | All users |
| Student Portal | Personal dashboard with all module data | Students |
| Guardian Portal | Multi-child monitoring from one account | Guardians |
| Staff Cockpits | Role-specific landing pages with quick actions | All staff |
| Reports & Dashboards | Pre-built analytics and visual summaries | Academic Heads, System Managers |
| Role-Based Security | Multi-layer data isolation enforced at database level | All users |
| Demo Data | Realistic dataset for demonstrations | Presenters, Evaluators |
