# Demo Credentials — Institution ERP

All demo accounts use password: **`Demo@2026`**

**Total accounts: 14** (6 Students/Guardians + 8 Staff)

## Staff Accounts (System User — Desk Access)

| # | Email | Role | Cockpit Landing | Description |
|---|---|---|---|---|
| 1 | `admin@demo.institution.local` | System Manager | Admin Cockpit | Institution-wide mission control — aggregate stats across all modules |
| 2 | `admissions@demo.institution.local` | Admissions Officer | Admissions Cockpit | Admission inquiries, pipeline, applicant workflow |
| 3 | `academichead@demo.institution.local` | Academic Head | Academic Head Cockpit | Programs, courses, attendance overview, exam performance |
| 4 | `instructor1@demo.institution.local` | Instructor | Instructor Cockpit | Attendance summary, pending assessments, quick-mark actions |
| 5 | `instructor2@demo.institution.local` | Instructor | Instructor Cockpit | Same as instructor1, different class assignments |
| 6 | `feemanager@demo.institution.local` | Fee Manager | Fee Manager Cockpit | Fee overview, pending discounts, payment recording |
| 7 | `facilitymanager@demo.institution.local` | Facility Manager | Facility Manager Cockpit | Library items, overdue tracking, hostel occupancy |
| 8 | `comms.officer@demo.institution.local` | Communication Officer | Communication Cockpit | Notices, feedback queue, dispatch |

## Student Portal Accounts (Website User → /institution-portal)

| # | Email | Linked Student | Program | Demo Note |
|---|---|---|---|---|
| 9 | `richdemo@demo.institution.local` | STU-2026-00079 (Shweta Joshi) | B.A. English | **USE THIS FOR DEMO** — fully populated: 50 attendance, 6 results (mixed published/unpublished), 1 fee (partial), 5 library transactions (3 active), 1 feedback |
| 10 | `student1@demo.institution.local` | STU-2026-00001 | B.Sc Computer Science | Minimal data |
| 11 | `student2@demo.institution.local` | STU-2026-00007 | B.Com | Minimal data |
| 12 | `student3@demo.institution.local` | STU-2026-00015 | BBA | Minimal data |

## Guardian Portal Accounts (Website User → /institution-portal)

| # | Email | Linked Guardian | Linked Students | Demo Note |
|---|---|---|---|---|
| 13 | `guardian1@demo.institution.local` | Arun Nair | STU-2026-00040 (Vedant Verma), STU-2026-00078 (Dhruv Reddy) | **USE THIS FOR DEMO** — 2 children, child switcher works |
| 14 | `guardian2@demo.institution.local` | Piyush Hegde | STU-2026-00033, STU-2026-00038, STU-2026-00077 | 3 children — shows larger family switching |

## Login Flow by Role

- **Students/Guardians**: Login → `/institution-portal` → Vue SPA with sidebar navigation
- **Staff (Instructor, Fee Manager, etc.)**: Login → role-specific cockpit page (e.g., Instructor Cockpit) → quick actions + "Open Full Desk" link → Frappe Desk for full CRUD
- **System Manager**: Login → Admin Cockpit (institution-wide overview) → "Open Full Admin" link → Frappe Desk
- **Academic Head**: Login → Academic Head Cockpit → Desk

## Notes

- **Best demo accounts**: `richdemo@demo.institution.local` (student) and `guardian1@demo.institution.local` (guardian)
- Portal users have `desk_access = 0` and see only their own records via User Permissions
- Staff users have full desk access with role-based permission scoping
- Demo data is identifiable by the `@demo.institution.local` email domain
- Regenerate: `bench --site institution.localhost execute institution_erp.generate_demo_data.run`
- Reset: `bench --site institution.localhost execute institution_erp.reset_demo_data.run`
