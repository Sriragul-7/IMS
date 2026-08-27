# Institution ERP — Architecture Report

## 1. System Overview

Institution ERP is a comprehensive Student Information System and institution management platform built on Frappe v16 (v16.26.3). It covers the full student lifecycle from admissions inquiry through graduation, including academics, attendance, examinations, fees, library, hostel, transport, and institutional communication. The system comprises 48 DocTypes across 10 modules, with 8 custom roles (6 staff + 2 portal), 6 Script Reports, 5 Number Cards, 2 Dashboard Charts, 1 custom Dashboard, and 11 whitelisted API methods. Portal access for Students and Guardians is implemented via Frappe's `permission_query_conditions` with row-level scoping.

---

## 2. Module Map

| Module | DocTypes | Core Purpose | Key Dependencies |
|--------|----------|-------------|-----------------|
| Academics | 10 | Programs, courses, scheduling, instructor assignment, student groups | SIS (Student, Student Group Member) |
| SIS | 2 | Student and Guardian master records | — |
| Admissions | 5 | Inquiry → application → entrance test → approval → auto Student/Guardian creation | Academics (Program, Academic Year), SIS |
| Attendance | 2 | Daily student attendance by group, staff attendance by instructor | Academics (Course Schedule, Student Group), SIS |
| Examination | 5 | Assessment plans, grading scales, bulk marks entry, result publication | Academics (Course, Student Group, Grading Scale) |
| Fees | 9 | Fee structures, schedules, invoices, payments, discounts, dues reporting | SIS (Student), Academics (Academic Year, Student Group) |
| Library | 4 | Book catalog, membership, issue/return with fine calculation | SIS (Student) |
| Hostel | 3 | Hostel/room management, occupancy tracking, student allocation | SIS (Student) |
| Transport | 4 | Vehicle registry, routes with stops, student transport allocation | SIS (Student) |
| Communication | 4 | Notices, audience-targeted dispatch, feedback, institutional dashboard | SIS (Student, Guardian), Academics (Student Group, Program) |

---

## 3. DocType Reference

### 3.1 Academics (10 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Program** | `field:program_name` | program_name, program_code, department | — | — |
| **Course** | `field:course_name` | course_name, course_code, program, credits, course_type | — | — |
| **Academic Year** | `field:academic_year_name` | academic_year_name, year_start_date, year_end_date | — | — |
| **Academic Term** | `field:term_name` | term_name, academic_year, term_start_date, term_end_date | — | — |
| **Room** | `field:room_name` | room_name, building, floor, capacity, room_type | — | — |
| **Instructor** | `naming_series: INST-.####` | instructor_name, employee_id, department, email, status | Instructor Course | — |
| **Student Group** | `field:group_name` | group_name, program, academic_year, course, max_strength | Student Group Member | — |
| **Course Schedule** | `hash` | course, student_group, instructor, room, day_of_week, from_time, to_time | — | Prevents room/instructor double-booking on same day + overlapping time |
| **Instructor Course** | child | course | — | — |
| **Student Group Member** | child | student | — | — |

### 3.2 SIS (2 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Student** | `naming_series: STU-.YYYY.-.#####` | first_name, last_name, status, gender, date_of_birth, program, guardian, email_address | — | Guardian link must exist |
| **Guardian** | `format:{guardian_name}-{###}` | guardian_name, guardian_email, relation_to_student, phone_number | — | — |

### 3.3 Admissions (5 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Admission Inquiry** | `naming_series: ADM-INQ-.YYYY.-.####` | applicant_name, guardian_name, program_interested, source, status | — | — |
| **Student Applicant** | `naming_series: STU-APP-.YYYY.-.####` | applicant_name, program, academic_year, guardian_name, status, workflow_state, created_student | Applicant Document | On approval, auto-creates Guardian + Student records |
| **Entrance Test** | `field:test_name` | test_name, test_date, program, max_marks, passing_marks | — | — |
| **Entrance Test Result** | `hash` | entrance_test, student_applicant, marks_obtained, result | — | Auto-calculates Pass/Fail from entrance test passing marks |
| **Applicant Document** | child | document_type, attached_file | — | — |

### 3.4 Attendance (2 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Student Attendance** | `hash` | student, student_group, course_schedule, attendance_date, status | — | Prevents duplicate attendance per student + date + course_schedule |
| **Staff Attendance** | `hash` | instructor, attendance_date, status | — | Prevents duplicate attendance per instructor + date |

### 3.5 Examination (5 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Grading Scale** | `field:scale_name` | scale_name | Grading Interval | Requires at least one interval; no overlapping thresholds |
| **Assessment Group** | `field:group_name` | group_name, academic_term, results_published, weightage_percent | — | — |
| **Assessment Plan** | `hash` | assessment_group, course, student_group, max_marks, passing_marks, grading_scale | — | Validates passing_marks < max_marks |
| **Assessment Result** | `hash` | assessment_plan, student, marks_obtained, percentage, grade, status | — | Validates marks ≤ max_marks; auto-calculates grade from Grading Scale; prevents duplicate per student+plan |
| **Grading Interval** | child | grade_code, threshold_percent, grade_description | — | — |

### 3.6 Fees (9 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Fee Category** | `field:category_name` | category_name | — | — |
| **Fee Structure** | `field:structure_name` | structure_name, program, academic_year, total_amount | Fee Structure Component | Requires ≥1 component; auto-sums total |
| **Fee Schedule** | `hash` | fee_structure, student_group, due_date | Fee Schedule Student | — |
| **Fees** | `naming_series: FEE-.YYYY.-.####` | student, fee_schedule, academic_year, due_date, total_amount, discount_amount, paid_amount, outstanding_amount, status | Fees Component | Recomputes paid/outstanding from Fee Payments on every validate; sets Overdue status when past due_date |
| **Fee Payment** | `naming_series: PMT-.YYYY.-.#####` | fees, student, payment_date, amount, payment_mode, reference_number | — | Validates payment ≤ outstanding; recomputes parent Fees on submit |
| **Fee Discount** | `hash` | student, fees, discount_type, discount_value, status | — | Percentage must be 0–100; on Approved, sets linked Fees.discount_amount |
| **Fee Structure Component** | child | fee_category, amount | — | — |
| **Fee Schedule Student** | child | student, included | — | — |
| **Fees Component** | child | fee_category, amount | — | — |

### 3.7 Library (4 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Book Category** | `field:category_name` | category_name | — | — |
| **Library Item** | `naming_series: LIB-BOOK-.#####` | title, author, isbn, book_category, total_copies, available_copies | — | available_copies ≤ total_copies; no negatives; on insert, sets available = total |
| **Library Membership** | `naming_series: LIB-MEM-.YYYY.-.####` | student, issue_date, valid_upto, max_books_allowed, status | — | valid_upto ≥ issue_date; max_books_allowed ≥ 1 |
| **Library Transaction** | `hash` | student, library_item, transaction_type, transaction_date, due_date, return_date, fine_amount, status | — | Issue: validates available copies, active membership, max books limit. Return: validates open issue exists; calculates overdue fine (₹5/day). On submit: adjusts available_copies; creates Fees record on late return |

### 3.8 Hostel (3 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Hostel** | `field:hostel_name` | hostel_name, hostel_type, warden, total_capacity | — | Auto-recomputes total_capacity from linked rooms |
| **Hostel Room** | `field:room_number` | hostel, room_number, room_type, capacity, occupied_count | — | capacity ≥ 1; occupied_count auto-managed |
| **Hostel Room Allocation** | `hash` | student, hostel_room, allocation_date, vacate_date, status | — | Validates room not full; one active allocation per student; recomputes occupied_count on create/vacate |

### 3.9 Transport (4 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Vehicle** | `field:vehicle_number` | vehicle_number, capacity, driver_name, driver_phone, status | — | capacity ≥ 1 |
| **Transport Route** | `field:route_name` | route_name, vehicle, fee_amount | Route Stop | No duplicate stop_order values |
| **Student Transport Allocation** | `hash` | student, transport_route, pickup_stop, allocation_date, status | — | Validates vehicle not full; one active allocation per student per route |
| **Route Stop** | child | stop_name, stop_order, pickup_time | — | — |

### 3.10 Communication (4 DocTypes)

| DocType | Naming | Key Fields | Child Tables | Notable Validation |
|---------|--------|-----------|-------------|-------------------|
| **Notice** | `naming_series: NOTICE-.YYYY.-.#####` | title, body, audience_type, target_program/student_group/role/student, publish_date, expiry_date, status | — | expiry_date ≥ publish_date. On Published, resolves audience and creates Notice Recipient records |
| **Notice Recipient** | `hash` | notice, student, recipient_type, read_status, read_on | — | — |
| **Communication Log** | `hash` | reference_notice, recipient_type, recipient, channel, message_summary, status, sent_at | — | Auto-sets sent_at on insert if status=Sent |
| **Feedback** | `naming_series: FDBK-.YYYY.-.#####` | student, guardian, category, subject, description, status, assigned_to, resolution_notes, raised_date | — | Requires at least one of Student/Guardian; requires resolution_notes when status=Resolved/Closed |

---

## 4. Roles & Permissions Matrix

### 4.1 Role Summary

| Role | Desk Access | Primary Modules | Scope |
|------|------------|----------------|-------|
| System Manager | Yes | All | Full access to everything |
| Administrator | Yes | All | Superuser |
| Academic Head | Yes | Academics, Examination, most read-only across all | Read on all; Write on academics/exam DocTypes |
| Admissions Officer | Yes | Admissions | Full CRUD on admissions pipeline |
| Instructor | Yes | Academics, Attendance, Examination | Full on attendance/assessment; read on academics |
| Fee Manager | Yes | Fees | Full CRUD on all fee DocTypes |
| Facility Manager | Yes | Library, Hostel, Transport | Full CRUD on facility DocTypes |
| Communication Officer | Yes | Communication | Full on Notice, Communication Log; read/write on Feedback |
| Student | No (portal) | — | Read-only on own records across all modules |
| Guardian | No (portal) | — | Read-only on linked students' records |

### 4.2 permission_query_conditions Coverage

| DocType | Condition Function | Bypass Roles |
|---------|-------------------|-------------|
| Student | `get_permission_query_conditions_student` | System Manager, Academic Head, Admissions Officer |
| Fees | `get_permission_query_conditions_fees` | System Manager, Fee Manager, Academic Head |
| Fee Payment | `get_permission_query_conditions_fee_payment` | System Manager, Fee Manager, Academic Head |
| Student Attendance | `get_permission_query_conditions_student_attendance` | System Manager, Academic Head |
| Staff Attendance | `get_permission_query_conditions_staff_attendance` | System Manager, Academic Head |
| Assessment Result | `get_permission_query_conditions_assessment_result` | System Manager, Academic Head |
| Assessment Plan | `get_permission_query_conditions_assessment_plan` | System Manager, Academic Head |
| Notice | `get_permission_query_conditions_notice` | System Manager, Communication Officer, Academic Head |
| Notice Recipient | `get_permission_query_conditions_notice_recipient` | System Manager, Communication Officer, Academic Head |
| Feedback | `get_permission_query_conditions_feedback` | System Manager, Communication Officer, Academic Head, Instructor |
| Communication Log | `get_permission_query_conditions_communication_log` | System Manager, Communication Officer, Academic Head |
| Library Item | `get_permission_query_conditions_library_item` | System Manager, Facility Manager, Academic Head |
| Library Membership | `get_permission_query_conditions_library_membership` | System Manager, Facility Manager, Academic Head |
| Library Transaction | `get_permission_query_conditions_library_transaction` | System Manager, Facility Manager, Academic Head |
| Hostel / Hostel Room / Hostel Room Allocation | `get_permission_query_conditions_hostel` | System Manager, Facility Manager, Academic Head |
| Vehicle / Transport Route / Student Transport Allocation | `get_permission_query_conditions_transport` | System Manager, Facility Manager, Academic Head |

### 4.3 Portal Permission Model (Student / Guardian)

The portal access system combines two mechanisms:

**User Permissions** — Created by `ensure_guardian_user()` and `ensure_student_user()` when portal Users are generated. Each Student-role User gets a `User Permission` record allowing access to their own Student record. Each Guardian-role User gets `User Permission` records for their Guardian record plus all linked Student records.

**permission_query_conditions** — SQL WHERE clauses injected by Frappe for non-bypass roles. For Student-role users, conditions resolve the user's email → Student record → filter queries to `student = '<their name>'`. For Guardian-role users, conditions resolve email → Guardian → all linked Students → filter queries to `student IN ('<child1>', '<child2>', ...)`.

The combination means:
- A Student sees only their own Fees, Attendance, Results, Library Transactions, Notices, and Feedback
- A Guardian sees all records for every Student linked to their Guardian record
- Staff roles see either all records (System Manager, Academic Head) or scoped records (Instructor sees only their groups' attendance; Fee Manager sees all fees)

---

## 5. Cross-Module Data Flows

### 5.1 Admission Pipeline

```
Admission Inquiry ──→ Student Applicant ──→ Entrance Test ──→ Entrance Test Result
      │                      │                                        │
      │                      ├──→ Draft → Applied → Under Review ────→ Approved
      │                      │                                        │
      │                      │                              on_update triggers:
      │                      │                              ┌─────────┴─────────┐
      │                      │                              │  Create Guardian   │
      │                      │                              │  Create Student    │
      │                      │                              │  Link via FK       │
      │                      │                              └───────────────────┘
```

### 5.2 Fee Lifecycle

```
Fee Category ──→ Fee Structure ──→ Fee Schedule ──→ Fees (invoice)
       │              │                  │                │
       │              │                  │         recompute_paid_and_status()
       │              │                  │                │
       │              │                  │         ┌──────┴──────┐
       │              │                  │         │ Query Fee   │
       │              │                  │         │ Payments    │
       │              │                  │         │ Compute     │
       │              │                  │         │ outstanding │
       │              │                  │         │ Set status  │
       │              │                  │         └─────────────┘
       │              │                  │                │
       │              │                  │         Fee Payment ──→ on_submit recomputes parent
       │              │                  │
       │              │                  └──→ generate_fees_from_schedule() [API]
       │              │
       │              └──→ Fee Discount (on Approved → sets discount_amount on Fees)
```

### 5.3 Assessment Flow

```
Grading Scale ──→ Assessment Group ──→ Assessment Plan
                         │                    │
                  results_published     mark_bulk_assessment_results() [API]
                         │                    │
                         │            Assessment Result
                         │                    │
                         │            calculate_grade() ←── Grading Scale intervals
                         │            calculate_status() (Pass/Fail)
                         │
                  results_published = 0 → portal users cannot see results
                  results_published = 1 → permission_query_conditions allow access
```

### 5.4 Notice & Communication Flow

```
Notice (Draft) ──→ on_update(status=Published)
                         │
                  resolve_audience_and_create_recipients()
                         │
                  ┌──────┴──────┐
                  │ By audience: │
                  │ All          │
                  │ Program-wise │
                  │ Group-wise   │
                  │ Role-wise    │
                  │ Individual   │
                  └──────┬──────┘
                         │
                  Notice Recipient (one per student)
                         │
                  dispatch_notice() [API] [stub]
                         │
                  Communication Log (Email/SMS stub)
```

### 5.5 Library Issue/Return Cycle

```
Book Category ──→ Library Item (available_copies managed)
                         │
                  Library Membership (student, valid_upto, max_books)
                         │
                  Library Transaction (Issue)
                         │
                  ├── validate: checks available_copies > 0
                  ├── validate: checks active membership
                  ├── validate: checks not exceeding max_books
                  ├── on_submit: decrements available_copies
                         │
                  Library Transaction (Return)
                         │
                  ├── validate: checks open Issue exists
                  ├── calculate: overdue fine = days_overdue × ₹5
                  ├── on_submit: increments available_copies
                  ├── on_submit: if fine > 0, auto-creates Fees record
```

---

## 6. Reports & Dashboards

### 6.1 Reports

| Report | Module | Type | Purpose |
|--------|--------|------|---------|
| Fee Dues Report | Fees | Script Report | Lists fees with outstanding amounts; filterable by Academic Year, Program, Status |
| Student Attendance Summary | Attendance | Script Report | Attendance summary per student in a group with present/absent/late/total counts and percentages |
| Student Result Summary | Examination | Script Report | Assessment results per student with marks, grade, percentage, and overall average |
| Transport Route Utilization | Transport | Script Report | Shows student count per route with capacity utilization |
| Library Circulation Report | Library | Script Report | Lists library transactions with status (Issued/Returned/Overdue), filterable by student |
| Hostel Occupancy Report | Hostel | Script Report | Shows room-by-room occupancy with capacity and available beds per hostel |

### 6.2 Number Cards

| Card | Module | What It Shows |
|------|--------|--------------|
| Total Active Students | Communication | Count of Students with status=Active |
| Total Outstanding Fees | Communication | Sum of outstanding_amount across all non-Paid Fees |
| Books Currently Issued | Communication | Count of Library Transactions with status=Issued |
| Hostel Occupancy (Rooms Occupied) | Communication | Count of Hostel Room Allocations with status=Active |
| Open Feedback/Complaints | Communication | Count of Feedback with status in (Open, In Progress) |

### 6.3 Dashboard Charts

| Chart | Module | Type | What It Shows |
|-------|--------|------|--------------|
| Fee Collection Trend | Communication | Sum | Sum of paid_amount grouped by month |
| Attendance Trend | Communication | Count | Count of Student Attendance records grouped by month |

### 6.4 Dashboard

**Institution Overview** — Custom dashboard containing:
- Charts: Fee Collection Trend, Attendance Trend
- Cards: Total Active Students, Total Outstanding Fees, Books Currently Issued, Hostel Occupancy, Open Feedback/Complaints

---

## 7. API Surface

All whitelisted methods are in `api.py`.

| Method | Stage | Purpose |
|--------|-------|---------|
| `get_students_in_group(student_group)` | 3 | Fetch all students in a Student Group with default status |
| `mark_bulk_student_attendance(student_group, attendance_date, attendance_data, course_schedule)` | 3 | Bulk-create Student Attendance records; skips duplicates |
| `mark_bulk_staff_attendance(attendance_date, attendance_data)` | 3 | Bulk-create Staff Attendance records; skips duplicates |
| `mark_bulk_assessment_results(assessment_plan, results_data)` | 4 | Bulk-create or update Assessment Results; auto-calculates grades |
| `generate_fees_from_schedule(fee_schedule_name)` | 5 | Generate Fees invoices from a Fee Schedule; skips already-generated |
| `dispatch_notice(notice_name)` | 7 | Stub dispatch: creates Communication Log entries for Published Notice recipients |
| `ensure_guardian_user(guardian_name)` | 8 | Create a Frappe User for a Guardian with Guardian role + User Permissions |
| `ensure_all_guardian_users()` | 8 | Bulk-create Users for all Guardians with email addresses |
| `ensure_student_user(student_name)` | 8 | Create a Frappe User for a Student with Student role + User Permission |
| `ensure_all_student_users()` | 8 | Bulk-create Users for all Students with email addresses |
| `backfill_student_status()` | 8 | Set status=Active for all Student records missing a status |

Internal (non-whitelisted) helper functions in `api.py`:
- `_get_portal_student(user)` — resolves a User email to a Student name
- `_get_portal_guardian_students(user)` — resolves a Guardian-role User to their linked Students
- 16 `get_permission_query_conditions_*` functions for row-level security

---

## 8. Known Limitations & Deviations

- **Library fine auto-creates a Fees record without Fee Manager review** — When a Library Transaction return calculates an overdue fine (₹5/day), it immediately creates a Fees record. In a production system, this would typically go through an approval workflow.
- **Student status field was added late in Stage 8** — Historical data semantics before Stage 8 are informal; the `status` field (default Active) was backfilled but records created before Stage 8 had no explicit status.
- **dispatch_notice is a stub** — The `dispatch_notice()` method creates Communication Log entries but does not actually send emails or SMS. Real gateway integration is future scope.
- **No ERPNext dependency** — The Fees module is entirely self-contained with its own `discount_amount` field on Fees (not modifying ERPNext totals). This is intentional to avoid ERPNext Accounts coupling.
- **Vehicle.driver_phone is Data, not Phone** — Uses Data fieldtype to avoid Frappe v16's country-code validation on Phone fields, which was causing issues with Indian phone numbers.
- **Dashboard created programmatically** — The Institution Overview Dashboard was created via `frappe.get_doc()` in test code rather than app JSON, because Frappe v16 doesn't auto-sync non-standard Dashboard instances from app JSON files.
- **4 Communication module DocType directories missing `__init__.py`** — `communication_log`, `feedback`, `notice`, `notice_recipient` directories lack `__init__.py` files (Frappe v16 does not require them for DocTypes, but they were included in all other modules for consistency).
- **Guardian naming uses `format:{guardian_name}-{###}`** — This can produce non-unique names if two guardians share the same name. The `###` suffix is a sequential counter, not a collision-safe hash.

---

## 9. Build Statistics

| Metric | Count |
|--------|-------|
| Total DocTypes | 48 |
| Child Tables (istable=1) | 8 |
| Modules | 10 |
| Custom Roles | 8 (6 staff + 2 portal) |
| Script Reports | 6 |
| Number Cards | 5 |
| Dashboard Charts | 2 |
| Custom Dashboards | 1 |
| Whitelisted API Methods | 11 |
| permission_query_conditions | 16 functions covering 19 DocTypes |
| E2E Test Files | 7 |
| Controller Files with Validation | 22 |

---

## 10. Suggested Next Steps

- **LMS Integration** — Add a Learning Management System module for course content, assignments, and online submission
- **HR/Payroll Module** — Extend Staff Attendance into a full HR module with employee profiles, leave management, and payroll
- **Payment Gateway Integration** — Replace the stub Fee Payment flow with real gateway (Razorpay, Stripe) for online fee collection
- **Real SMS/Email Gateway** — Replace the `dispatch_notice` stub with actual SMTP/Twilio integration for Notice dispatch
- **Custom-Themed Portal** — Build a branded student/guardian portal with custom CSS, dashboard widgets, and notification preferences
- **Mobile App via REST API** — Expose the existing whitelisted methods and DocType CRUD via Frappe's built-in REST API for mobile consumption
- **Batch/Section Management** — Add academic batch and section concepts for managing student cohorts across years
- **Hostel Mess Management** — Extend Hostel with mess/meal planning and attendance
