# Institution ERP

A comprehensive Student Information System and Institution Management ERP built on Frappe v16.

## Features

### Academics (Stage 1-2)
- **Programs & Courses**: Define academic programs with courses, credit hours, and prerequisites
- **Course Scheduling**: Schedule courses with instructors and rooms
- **Assessment Framework**: Assessment Groups, Grading Scales, Assessment Plans, and Assessment Results

### Student Information System (Stage 3)
- **Students**: Full student lifecycle with naming series (STU-.YYYY.-.#####)
- **Guardians**: Guardian records linked to students with relation tracking

### Admissions (Stage 3)
- **Inquiry → Applicant → Enrollment**: Complete admissions pipeline
- **Entrance Tests**: Test management with results and scoring
- **Fee Structures**: Program-linked fee structures with component breakdowns

### Attendance (Stage 4)
- **Student Attendance**: Daily course-level attendance with status (Present/Absent/Late/Excused)
- **Staff Attendance**: Employee attendance tracking

### Examination (Stage 4)
- **Assessment Results**: Student score recording with grade auto-calculation via Grading Scale

### Fees (Stage 5)
- **Fee Generation**: Bulk fee creation from Fee Schedules
- **Fee Payments**: Track payments with receipt numbers
- **Discounts**: Fee Discounts with approval workflow
- **Status Tracking**: unpaid → partially_paid → paid → overdue

### Library (Stage 6)
- **Book Categories**: Classification and metadata
- **Library Items**: Individual book copies with barcode and availability tracking
- **Library Membership**: Member registration with expiry
- **Library Transactions**: Issue/Return with fine calculation (₹5/day overdue)

### Hostel (Stage 6)
- **Hostels**: Hostel definitions with capacity and warden
- **Hostel Rooms**: Room management with type and rent
- **Room Allocations**: Student room assignments with date tracking

### Transport (Stage 6)
- **Vehicles**: Vehicle registry with capacity and driver info
- **Transport Routes**: Routes with stops and per-stop fees
- **Student Transport Allocations**: Route assignments for students

### Communication (Stage 7)
- **Notices**: Institutional notices with audience targeting (All/Students/Staff/Parents/Custom)
- **Communication Log**: Track emails, SMS, calls, and other communications
- **Feedback**: Multi-category feedback with priority and status tracking
- **Dashboard**: Institution Overview with charts and number cards

### Portal Access (Stage 8)
- **Student Portal**: Students can view their own records (attendance, fees, grades)
- **Guardian Portal**: Guardians can view records for all linked students
- **Permission Scoping**: Row-level security via `permission_query_conditions`

## Tech Stack

- **Framework**: Frappe v16
- **Database**: MariaDB / MySQL
- **Backend**: Python
- **Frontend**: Frappe UI (Desk) + Web Portal

## Installation

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed installation instructions.

## Testing

All stages include end-to-end tests:

```bash
bench --site institution.localhost execute institution_erp.e2e_test.execute        # Stage 1-2
bench --site institution.localhost execute institution_erp.e2e_test_stage3.execute  # Stage 3
bench --site institution.localhost execute institution_erp.e2e_test_stage4.execute  # Stage 4
bench --site institution.localhost execute institution_erp.e2e_test_stage5.execute  # Stage 5
bench --site institution.localhost execute institution_erp.e2e_test_stage6.execute  # Stage 6
bench --site institution.localhost execute institution_erp.e2e_test_stage7.execute  # Stage 7
bench --site institution.localhost execute institution_erp.e2e_test_stage8.execute  # Stage 8
```

## Architecture

```
institution_erp/
├── academics/          # Programs, Courses, Schedules, Assessment
├── sis/                # Students, Guardians
├── admissions/         # Inquiry, Applicant, Entrance Tests
├── attendance/         # Student & Staff Attendance
├── examination/        # Assessment Results
├── fees/               # Fees, Payments, Discounts
├── library/            # Books, Memberships, Transactions
├── hostel/             # Hostels, Rooms, Allocations
├── transport/          # Vehicles, Routes, Allocations
├── communication/      # Notices, Logs, Feedback, Dashboard
├── api.py              # Whitelisted methods & permission_query_conditions
├── setup_roles.py      # Custom role creation
├── hooks.py            # Frappe hooks
└── e2e_test*.py        # End-to-end tests
```

## License

Proprietary — Institution ERP
