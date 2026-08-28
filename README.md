# Institution ERP

A comprehensive Student Information System and institution management platform for **Bannari Amman Institute of Technology (BIT)**, built on Frappe v16. Covers the full student lifecycle from admissions inquiry through graduation, including academics, attendance, examinations, fees, library, hostel, transport, and institutional communication.

## System at a Glance

| Metric | Count |
|--------|-------|
| DocTypes | 48 |
| Modules | 10 |
| Custom Roles | 8 |
| Script Reports | 6 |
| Number Cards | 5 |
| Dashboard Charts | 2 |
| Whitelisted API Methods | 11 |
| Login Tests (passing) | 42/42 (3 runs) |
| API Verification (passing) | 26/26 |

## Modules

| Module | DocTypes | Purpose |
|--------|----------|---------|
| Academics | 10 | Programs, courses, scheduling, instructor assignment, student groups |
| SIS | 2 | Student and Guardian master records |
| Admissions | 5 | Inquiry → application → entrance test → approval → auto Student/Guardian creation |
| Attendance | 2 | Student attendance by group, staff attendance by instructor |
| Examination | 5 | Assessment plans, grading scales, bulk marks entry, result publication |
| Fees | 9 | Fee structures, schedules, invoices, payments, discounts, dues reporting |
| Library | 4 | Book catalog, membership, issue/return with fine calculation |
| Hostel | 3 | Hostel/room management, occupancy tracking, student allocation |
| Transport | 4 | Vehicle registry, routes with stops, student transport allocation |
| Communication | 4 | Notices, audience-targeted dispatch, feedback, institutional dashboard |

## Custom Roles

| Role | Access | Primary Modules |
|------|--------|----------------|
| System Manager | Desk — full | All modules |
| Academic Head | Desk — read all, write academics/exam | Academics, Examination |
| Admissions Officer | Desk — full CRUD | Admissions |
| Instructor | Desk — attendance, assessment | Academics, Attendance, Examination |
| Fee Manager | Desk — full CRUD | Fees |
| Facility Manager | Desk — full CRUD | Library, Hostel, Transport |
| Communication Officer | Desk — full on notices/logs | Communication |
| Student | Portal — read-only own records | All modules (scoped) |
| Guardian | Portal — read-only linked students | All modules (scoped) |

## Architecture

### Hybrid Model

The system uses a hybrid approach:

- **Vue 3 + Vite Portal** (`/institution-portal`) — Single-page application for Student and Guardian roles. Hash-based routing, responsive design, child switcher for guardians with multiple enrolled students. Served via Frappe's web page system with CSRF token injection.
- **Staff Cockpits** — Role-specific Vue cockpit pages for high-frequency staff actions (InstructorCockpit, FeeManagerCockpit, FacilityManagerCockpit, CommunicationCockpit, AdmissionsCockpit, AcademicHeadCockpit, AdminCockpit).
- **Frappe Desk** — Re-themed desk for full CRUD operations on all DocTypes, used by all staff roles.

### Design System

- **Design Tokens** — Custom CSS custom properties for colors, spacing, border radius, and shadows.
- **Base Components** — `StatCard`, `StatusBadge`, `EmptyState`, `PageHeader` for consistent UI patterns.
- **Desk Theming** — `desk-theme.css` injected via `app_include_css` hook. Inter font (self-hosted, no CDN), BIT primary color (`#2563eb`), consistent border radius and transitions across all desk views.
- **Self-hosted Inter font** — No external CDN dependency.

### Permission Model

Row-level security via `permission_query_conditions` covering 19 DocTypes with 16 condition functions. Students see only their own records; Guardians see all linked students; staff roles see scoped or full data depending on role.

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench --site institution.localhost install-app institution_erp
```

## Demo Data

The app ships with a full demo dataset:

- **79 students** across multiple programs
- **12 instructors**
- **14 demo accounts** (8 staff + 4 student + 2 guardian)

### Demo Credentials

All accounts use password: **`Demo@2026`**

**Staff accounts** (desk access):

| Email | Role |
|-------|------|
| `admin@demo.institution.local` | System Manager |
| `admissions@demo.institution.local` | Admissions Officer |
| `academichead@demo.institution.local` | Academic Head |
| `instructor1@demo.institution.local` | Instructor |
| `instructor2@demo.institution.local` | Instructor |
| `feemanager@demo.institution.local` | Fee Manager |
| `facilitymanager@demo.institution.local` | Facility Manager |
| `comms.officer@demo.institution.local` | Communication Officer |

**Student accounts** (portal access):

| Email | Demo Note |
|-------|-----------|
| `richdemo@demo.institution.local` | Fully populated — use this for demo |
| `student1@demo.institution.local` | Basic student account |
| `student2@demo.institution.local` | Basic student account |
| `student3@demo.institution.local` | Basic student account |

**Guardian accounts** (portal access):

| Email | Demo Note |
|-------|-----------|
| `guardian1@demo.institution.local` | 2 children — use this for demo |
| `guardian2@demo.institution.local` | 3 children — larger family switching |

### Regenerating Demo Data

```bash
bench --site institution.localhost execute institution_erp.generate_demo_data.run
```

### Resetting Demo Data

```bash
bench --site institution.localhost execute institution_erp.reset_demo_data.run
```

## Build & Development

### Build the Vue Portal

```bash
cd apps/institution_erp/institution_erp/public/portal
npm install
npm run build
```

### Rebuild Frappe Assets

```bash
bench --site institution.localhost build
bench --site institution.localhost clear-cache
bench --site institution.localhost restart
```

### Run Tests

```bash
bench --site institution.localhost run-tests --app institution_erp
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/institution_erp
pre-commit install
```

Pre-commit is configured to use the following tools:

- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
