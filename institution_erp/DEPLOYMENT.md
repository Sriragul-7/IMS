# Institution ERP — Deployment Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- MariaDB 10.6+ or MySQL 8.0+
- Redis
- Frappe Bench CLI

## Quick Start

```bash
# Clone and setup bench
bench init frappe-bench
cd frappe-bench
bench get-app /path/to/institution_erp
bench new-site institution.localhost
bench --site institution.localhost install-app institution_erp
bench --site institution.localhost execute institution_erp.setup_roles.execute
bench --site institution.localhost execute institution_erp.api.backfill_student_status
bench --site institution.localhost migrate
bench start
```

## Post-Install Setup

### 1. Create Roles
Roles are auto-created by `setup_roles.execute`:
- Admissions Officer, Academic Head, Instructor
- Fee Manager, Facility Manager, Communication Officer
- Student, Guardian (portal roles)

### 2. Create Portal Users
```python
import frappe
from institution_erp.api import ensure_all_guardian_users, ensure_all_student_users
ensure_all_guardian_users()  # Creates Users + User Permissions for Guardians
ensure_all_student_users()   # Creates Users + User Permissions for Students
```

### 3. Backfill Student Status
```python
from institution_erp.api import backfill_student_status
backfill_student_status()  # Sets all existing Students to status=Active
```

### 4. Generate Test Data
```bash
bench --site institution.localhost execute institution_erp.generate_test_data.execute
bench --site institution.localhost execute institution_erp.generate_test_data_stage5.execute
bench --site institution.localhost execute institution_erp.generate_test_data_stage6.execute
bench --site institution.localhost execute institution_erp.generate_test_data_stage7.execute
```

## Module Inventory

| Module | DocTypes | Key Features |
|--------|----------|--------------|
| Academics | 10 | Program, Course, Course Schedule, Course Instructor, Room, Academic Year, Academic Term, Assessment Group, Grading Scale, Assessment Plan |
| SIS | 2 | Student, Guardian |
| Admissions | 5 | Admission Inquiry, Student Applicant, Entrance Test, Entrance Test Result, Fee Structure |
| Attendance | 2 | Student Attendance, Staff Attendance |
| Examination | 5 | Assessment Result + Exam DocTypes |
| Fees | 9 | Fees, Fee Payment, Fee Schedule, Fee Category, Fee Discount, Fee Structure |
| Library | 4 | Book Category, Library Item, Library Membership, Library Transaction |
| Hostel | 3 | Hostel, Hostel Room, Hostel Room Allocation |
| Transport | 4 | Vehicle, Transport Route, Route Stop (child), Student Transport Allocation |
| Communication | 4 | Notice, Notice Recipient, Communication Log, Feedback |

**Total: 48 DocTypes**

## Custom Roles (10)

| Role | Desk Access | Purpose |
|------|-------------|---------|
| Admissions Officer | Yes | Manages admissions pipeline |
| Academic Head | Yes | Oversees academics, read-only elsewhere |
| Instructor | Yes | Manages assessments, attendance |
| Fee Manager | Yes | Full CRUD on fee DocTypes |
| Facility Manager | Yes | Library, Hostel, Transport management |
| Communication Officer | Yes | Notices, Communication Log |
| Student | No | Portal role — read-only on own data |
| Guardian | No | Portal role — read-only on linked students |
| System Manager | Yes | Full access (Frappe built-in) |
| Administrator | Yes | Superuser (Frappe built-in) |

## Permission Scoping

Portal roles (Student, Guardian) are scoped via `permission_query_conditions` in `api.py`:
- **Student**: Sees only own records (matching `student` field)
- **Guardian**: Sees records for all linked students (via Guardian doctype)
- **Staff roles**: Scoped by Department or full access depending on role

## Running Tests

```bash
bench --site institution.localhost execute institution_erp.e2e_test.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage3.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage4.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage5.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage6.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage7.execute
bench --site institution.localhost execute institution_erp.e2e_test_stage8.execute
```

## Troubleshooting

- **Missing roles**: Run `bench --site institution.localhost execute institution_erp.setup_roles.execute`
- **Number Card counts wrong**: Run `bench --site institution.localhost execute institution_erp.api.backfill_student_status` then `bench --site institution.localhost migrate`
- **Portal users not seeing data**: Ensure `ensure_all_guardian_users()` / `ensure_all_student_users()` were called and User Permissions were created

## Frontend Rebuild Process

After ANY change to portal source files (`portal/src/**/*.vue`, `portal/src/**/*.js`, `portal/vite.config.js`), you must rebuild and deploy:

```bash
# One-command rebuild (from app root)
cd apps/institution_erp && npm run build && rm -rf institution_erp/public/portal && cp -r public/portal institution_erp/public/portal && bench --site institution.localhost clear-cache
```

This does:
1. `npm run build` — Vite compiles Vue sources to `public/portal/` (stable filenames: `portal.css`, `portal.js`)
2. `rm -rf + cp -r` — Deploys built assets to Frappe's public directory
3. `clear-cache` — Ensures Frappe serves the updated template (CSS link, JS link, brand strings)

**Important:** The Vite config uses stable output filenames (`portal.css`, `portal.js`) so the template's `<link>` and `<script>` tags don't need updating after each build. The CSS `<link>` tag in `institution-portal.html` must always reference `portal.css` — if it's missing, the portal renders unstyled.

## Desk Theming (Phase 3)

The Frappe Desk is rebranded via a custom CSS file injected through Frappe's `app_include_css` hook:

**Mechanism:**
- `hooks.py` → `app_include_css = ["/assets/institution_erp/css/inter-font.css", "/assets/institution_erp/css/desk-theme.css"]`
- Frappe loads these CSS files on every Desk page automatically
- No template modification needed — the hook system handles injection

**What desk-theme.css does:**
- Self-hosted Inter font via `@font-face` declarations (4 weights: 400, 500, 600, 700)
- CSS custom properties for BIT brand colors (`--bit-primary: #1e40af`, etc.)
- Font family override across all Desk elements (body, forms, buttons, modals, dropdowns)
- Button primary color override to BIT blue
- Form focus ring styling
- Border radius consistency (8px buttons/inputs, 14px modals)
- Sidebar active state highlighting
- Smooth transitions on interactive elements

**Font files location:** `institution_erp/public/fonts/inter-{400,500,600,700}.woff2`

**To modify desk theming:** Edit `institution_erp/public/css/desk-theme.css` — changes take effect after `bench clear-cache` (no rebuild needed since it's a static CSS file, not compiled by Vite).
