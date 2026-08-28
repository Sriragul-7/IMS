# DEMO WALKTHROUGH — Institution ERP (Bannari Amman Institute of Technology)

> **For project guide demonstration.** Rehearse in 15-20 minutes.  
> All demo accounts use password: **`Demo@2026`**  
> Portal URL: `http://localhost:8000/institution-portal`

---

## A. 60-Second Pitch (Read Aloud)

"Institution ERP is a full-stack Student Information System built on Frappe v16 with a Vue 3 portal for students, guardians, **and staff cockpits**. It covers the entire student lifecycle — from first enquiry through graduation — across 10 modules and 48 DocTypes. The system uses a **hybrid architecture**: staff log in and land on role-specific Vue cockpit pages — at-a-glance dashboards with stats, quick actions, and overview data — then click **'Open Full Desk'** to access the full Frappe CRUD interface for heavy-duty operations. Students and guardians get a dedicated SPA portal at `/institution-portal` with sidebar navigation and a guardian child-switcher. Everything is connected — approving an admission auto-creates the student record, the guardian record, and links them. Results are gated — students can't see marks until staff publish them. Fees auto-recompute when payments come in. The Vue portal uses a reusable design system — `StatCard`, `StatusBadge`, `EmptyState`, `PageHeader` components — while the Desk is rebranded with Inter font and BIT blue as the primary color. This is a working system with realistic demo data: 79 students, 12 instructors, 2,500+ attendance records, and 300+ assessment results."

---

## B. System Architecture (1 Slide)

| Layer | Technology | Details |
|-------|-----------|---------|
| **Backend** | Frappe v16.26 (Python/MySQL) | 48 DocTypes, 10 modules, 8 custom roles, 11 whitelisted API methods |
| **Staff Cockpits** | Vue 3 SPA (same build as portal) | Role-specific dashboards at `/institution-portal/<role>` — `StatCard`, `StatusBadge`, `EmptyState` design system components |
| **Student/Guardian Portal** | Vue 3 SPA | Hash-routed SPA at `/institution-portal` with sidebar navigation, child switcher for guardians |
| **Desk (Full CRUD)** | Frappe Desk (rebranded) | Inter font, BIT blue (`#1e40af`) primary color — full CRUD for staff after cockpit quick actions |
| **Security** | Row-level `permission_query_conditions` (16 functions) | User Permission portal scoping, `results_published` gating for marks visibility |
| **Design System** | 4 reusable Vue components | `StatCard` (colored stat block), `StatusBadge` (variant-colored label), `EmptyState` (empty placeholder), `PageHeader` (title + subtitle) |

**Hybrid Flow (Option C):** Staff login → Vue Cockpit (quick overview + actions) → "Open Full Desk" button → Frappe Desk (full CRUD). The cockpit is read-heavy and fast; Desk is write-heavy and comprehensive.

---

## C. Scripted Walkthrough — Staff Side

> **Tip:** Keep the browser maximized. Narrate what you're doing as you click.  
> **Key narrative:** Staff never land on Desk directly — they get a cockpit first.

---

### Step 1: Admissions Pipeline
**Login as:** `admissions@demo.institution.local`

**A. Admissions Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/admissions`
2. **Welcome banner** with greeting and "Open Full Admin" link
3. **Stats row** — 4 `StatCard` components: Total Inquiries, Open Inquiries, Under Review, Approved
4. **Admission Pipeline** — visual funnel: Open → Applied → Under Review → Approved → Rejected (with counts)
5. **Recent Inquiries** — list with `StatusBadge` per inquiry (Open, Converted, Closed)
6. **Quick Actions** — "New Inquiry", "New Applicant", "Review Applicants" links (each opens Desk form in new tab)

**B. Navigate to Desk** (click "Open Full Admin" or quick action)
1. Click **Admissions** workspace in the sidebar
2. Open **Student Applicant** — show workflow states (Draft → Applied → Under Review → Approved)
3. Open an "Approved" applicant → scroll down to show auto-created **Student** and **Guardian** records
4. **What this demonstrates:** Cockpit gives at-a-glance pipeline status; Desk provides full CRUD. The admission pipeline auto-creates Student + Guardian records on approval.

---

### Step 2: Academic Structure
**Login as:** `academichead@demo.institution.local`

**A. Academic Head Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/academic-head`
2. **Welcome banner** — greeting with "Open Full Admin" link
3. **Stats row** — Programs, Students, Avg Attendance %, Courses
4. **Cross-Module Navigation** — quick links to Students, Student Groups, Courses, Programs (each opens Desk)
5. **Attendance Overview** — per-group attendance percentages (green ≥80%, amber ≥60%, red <60%)
6. **Exam Performance Snapshot** — assessment completion status badges (Complete / Incomplete)

**B. Navigate to Desk** (click a quick action or "Open Full Admin")
1. Open **Program** — show 6 programs (B.Sc CS, B.Com, BBA, B.A. English, BCA, MBA)
2. Open **Course** — show 17 courses linked to programs, with credits and course types
3. Open **Course Schedule** — show 79 scheduled sessions with instructor, room, and time slots
4. Point out: same room/instructor cannot be double-booked
5. **What this demonstrates:** Cockpit gives cross-module academic overview; Desk provides full program/course/schedule management.

---

### Step 3: Instructor View — Attendance & Marks
**Login as:** `instructor1@demo.institution.local`

**A. Instructor Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/instructor`
2. **Welcome banner** — greeting with "Open Full Admin" link
3. **Stats row** — My Students, Assigned Groups, Attendance Today, Pending Marks
4. **Today's Classes** — list of today's scheduled sessions with `StatusBadge` (Ongoing = green, Upcoming = blue)
5. **Quick Actions** — "Mark Attendance", "Enter Marks", "Assessment Plans" (each opens Desk)
6. **Pending Marks Entry** — list of assessments with due dates, "Enter" button linking to Desk

**B. Navigate to Desk** (click "Mark Attendance" or "Open Full Admin")
1. Click **My Classes** workspace
2. Show the filtered **Course Schedule** list — only this instructor's sessions appear
3. Open **Student Attendance** — records scoped to this instructor's groups
4. Navigate to **Assessment Result** — marks entry interface
5. **What this demonstrates:** Cockpit highlights today's classes and pending work; Desk gives full attendance/marks entry. Instructors see only their own classes.

---

### Step 4: Fee Management
**Login as:** `feemanager@demo.institution.local`

**A. Fee Manager Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/fees-manager`
2. **Welcome banner** — greeting with "Open Full Admin" link
3. **Stats row** — Total Outstanding, Fee Records, Payments Today, Discounts Pending
4. **Outstanding Fees** — list of unpaid/partial fees with amounts and `StatusBadge` (Paid/Partial/Unpaid)
5. **Quick Actions** — "Record Payment", "Fee Records", "Fee Schedules" (each opens Desk)
6. **Pending Discount Approvals** — list of discount requests with "Review" button

**B. Navigate to Desk** (click "Record Payment" or "Open Full Admin")
1. Open **Fee Structure** — show the structure with fee components and total amounts
2. Open **Fee Schedule** — show how schedules are generated from structures
3. Open **Fees** (invoices) — show list with status badges: Paid (green), Partial (amber), Unpaid (red)
4. Open a "Paid" fee → scroll down to show linked **Fee Payment** records
5. Open **Fee Dues Report** — show report filtering outstanding amounts by program and status
6. **What this demonstrates:** Cockpit shows outstanding at-a-glance; Desk provides full fee lifecycle management with auto-status recomputation.

---

### Step 5: Facilities — Library, Hostel, Transport
**Login as:** `facilitymanager@demo.institution.local`

**A. Facility Manager Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/facility-manager`
2. **Welcome banner** — greeting with "Open Full Admin" link
3. **Stats row** — Available Books, Active Issues, Overdue Items (red), Hostel Occupancy %
4. **Quick Actions** — "Issue Book", "Return Book", "Hostel Allocations" (each opens Desk)
5. **Library — Active Issues** — list of currently issued books with due dates (overdue highlighted in red)
6. **Hostel Overview** — per-hostel occupancy bars (occupied/total with progress bar)

**B. Navigate to Desk** (click "Issue Book" or "Open Full Admin")
1. Open **Library Item** — show book catalog with available copies
2. Open **Library Transaction** — show issue/return records with fine amounts on overdue returns
3. Open **Hostel** → **Hostel Room** — show occupancy tracking (capacity vs occupied)
4. Open **Transport Route** — show routes with stops, vehicle, and fee amount
5. **What this demonstrates:** Cockpit gives library/hostel at-a-glance; Desk provides full facility management with fine calculation.

---

### Step 6: Communication
**Login as:** `comms.officer@demo.institution.local`

**A. Communication Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/communication`
2. **Welcome banner** — greeting with "Open Full Admin" link
3. **Stats row** — Total Notices, Published, Feedback Queue, Communication Logs
4. **Quick Actions** — "Create Notice", "All Notices", "Communication Logs" (each opens Desk)
5. **Recent Notices** — list with status dots (green = Published) and `StatusBadge`
6. **Open Feedback** — list of pending feedback items with "Review" button

**B. Navigate to Desk** (click "Create Notice" or "Open Full Admin")
1. Open **Notice** — show published notices with audience targeting (All, Program-wise, Group-wise)
2. Open **Feedback** — show submitted feedback with status badges (Open=amber, In Progress=blue, Resolved=green)
3. Point to the **Communication Dashboard** — Number Cards and Charts
4. **What this demonstrates:** Cockpit surfaces notices and feedback queue; Desk provides full notice dispatch and feedback management.

---

### Step 7: System Manager — Admin Cockpit
**Login as:** `Administrator` (or any System Manager user)

**A. Admin Cockpit** (Vue — landing page)
1. After login, browser lands on `/institution-portal/admin`
2. **Welcome banner** — "Administration Mission Control" with greeting and "Open Full Admin" link
3. **Stats row 1** (4 cards) — Active Students, Staff Members, Avg Attendance %, Outstanding Fees
4. **Stats row 2** (4 cards) — Programs, Courses, Open Feedback, Library Active
5. **Module Quick Access** — 8 icon links: Students, Instructors, Fees, Attendance, Assessments, Library, Notices, Hostel (each opens Desk)
6. **Admissions Pipeline** — Active vs Inactive student counts
7. **System Health** — Total DocTypes, Active Users, Open Feedback (warning color if >0), Outstanding Fees (warning color if >0)

**B. Navigate to Desk** (click any module link or "Open Full Admin")
- Full Frappe Desk with all 10 workspaces available
- **What this demonstrates:** AdminCockpit provides institution-wide aggregate view across all modules; Desk gives unrestricted access.

---

## D. Scripted Walkthrough — Portal Side (Student & Guardian)

### Step 1: Student Portal — Rich Demo Account
**Login as:** `richdemo@demo.institution.local` (Shweta Joshi, STU-2026-00079, B.A. English)

1. **Dashboard** — welcome banner, stat cards (Attendance %, Fees count, Outstanding amount, Library books), recent notices, recent fees, attendance donut chart
2. **Attendance** — 50 records with status badges: Present (green), Absent (red), Late (amber), Excused (purple). Summary bar: 84% attendance rate
3. **Results** — THIS IS THE STANDOUT FEATURE:
   - 6 assessment results displayed as cards with marks, grade, and Pass/Fail badge
   - 4 results show marks (published by staff)
   - 2 results are from unpublished assessment groups → the page shows a **blue "Results Not Yet Published"** banner at the top
   - **Call out explicitly:** "Notice the banner — students cannot see their marks until staff publishes the results. This is the results_published gating feature."
4. **Fees** — 1 fee record (₹48,000, Paid status in green), payment history showing the payment record
5. **Library** — 3 currently checked-out books with due dates, 5 transaction history records, overdue fines visible on returned items
6. **Notices** — 6 published notices expandable on click
7. **Feedback** — submit form + history showing 1 feedback with status

### Step 2: Guardian Portal — Child Switcher
**Login as:** `guardian1@demo.institution.local` (Arun Nair)

1. **Dashboard** — shows data for the first linked child (STU-2026-00040, Vedant Verma or STU-2026-00078, Dhruv Reddy)
2. **Child Switcher** — in the sidebar, show the dropdown listing both children:
   - STU-2026-00040: Vedant Verma (B.Com)
   - STU-2026-00078: Dhruv Reddy (B.A. English)
3. **Switch child** — click the other child → all data on the page updates to show that child's records
4. Navigate through Attendance, Results, Fees for the second child → confirm all data is scoped correctly
5. **What this demonstrates:** Guardian can monitor multiple children from one account, with proper data isolation between children

---

## E. Anticipated Questions & Answers

### Q1: "Is this connected to a real payment gateway?"
**A:** No. Fee Payment is a manual-entry record — the Fee Manager types in the amount, payment mode, and reference number. A real gateway (Razorpay, Stripe) would require webhook integration for payment confirmation, refund handling, and receipt generation. This is documented as future scope in the architecture.

### Q2: "What happens if two students are assigned the same room at the same time?"
**A:** The `Hostel Room Allocation` DocType validates on save: it checks if the room is full (`occupied_count >= capacity`) and whether the student already has an active allocation. If either check fails, the save is rejected with a `ValidationError`. Same logic applies to transport allocations.

### Q3: "How do you prevent a student from seeing another student's grades?"
**A:** Two layers: (1) `permission_query_conditions` inject a SQL WHERE clause that filters Assessment Results to `student = '<their record>'`, so even a direct API call returns empty. (2) The portal's `portal_get_results` API additionally checks `results_published` on the parent Assessment Group — students see a "Not Yet Published" banner instead of marks. We tested cross-access in Stage 3 — Guardian1 accessing a non-child's attendance was blocked with a PermissionError.

### Q4: "Is this production-ready?"
**A:** The data model, validation logic, and permission system are solid. What's NOT production-ready: (1) no real payment gateway, (2) no real email/SMS dispatch (stubs only), (3) demo data has some idempotency quirks on re-runs, (4) the Report Card print format is empty. See DEPLOYMENT.md for what would be needed for a real deployment (SSL, backups, monitoring, real SMTP).

### Q5: "What about the library fine — does it go through approval?"
**A:** Currently no. When a library book is returned late, the system auto-calculates fine (₹5/day) and immediately creates a Fees record. In a real institution, this would typically go through a Fee Manager approval step. This is a known limitation — it works for the demo but needs a workflow for production.

### Q6: "Why Vue 3 for the portal instead of using Frappe's built-in web views?"
**A:** Frappe's standard web pages are server-rendered Jinja templates — they work but give a full page reload on every navigation. The Vue 3 SPA gives a single-page-app experience: smooth navigation, no page flicker, client-side routing. It also let us build the guardian child-switcher as a reactive component. The tradeoff is a separate build step (`vite build`), but it's lightweight.

### Q7: "Why does staff UI use both a custom portal AND Desk?"
**A:** This is the **hybrid approach (Option C from Phase 3)**. The reasoning: (1) Frappe Desk is powerful for CRUD but overwhelming as a landing page — 48 DocTypes, 10 workspaces, lots of sidebar items. Staff don't need all of that on login. (2) The Vue cockpit gives a focused, role-specific dashboard — an Instructor sees their classes and pending marks, not hostel allocations. (3) The cockpit handles 80% of daily use cases (viewing stats, quick actions). (4) For the 20% that needs full CRUD (creating new records, editing existing ones, running reports), the "Open Full Desk" button takes them to the rebranded Frappe Desk with Inter font and BIT blue theming. (5) Both are part of the same Vue build — the cockpit pages live in `/portal/src/pages/` alongside the student portal pages, sharing the same design system components. The result is a fast, focused entry point that scales down to full power when needed.

### Q8: "What does the Report Card print format show?"
**A:** It exists as a Jinja-type Print Format on Assessment Result, but the HTML is empty — this is a known gap. If asked to print, nothing would render. This was deprioritized because the portal Results page already shows marks, grades, and pass/fail status, which covers the core use case.

### Q9: "How does the system handle different academic years?"
**A:** Academic Year and Academic Term are separate DocTypes. Fee Schedules, Assessment Groups, and Student Groups are all linked to a specific Academic Year. When a new year starts, new schedules and groups are created — historical data remains queryable but is separated by year. Currently we have 2 Academic Years and 5 Terms configured.

### Q10: "Can a guardian submit feedback on behalf of their child?"
**A:** The portal Submit Feedback form uses the logged-in user's record. For guardians, the `portal_submit_feedback` API accepts a `student` parameter — so a guardian could theoretically submit for any of their linked children. The API validates that the student belongs to the guardian via `_validate_guardian_student()`. In practice, the current UI always submits for the logged-in user's own record.

### Q11: "What's the most impressive single feature to show?"
**A:** The results_published gating. Log in as the rich student, go to Results, and show the blue banner saying "Results Not Yet Published" alongside cards showing actual marks for published results. Then switch to an instructor account, publish those assessment groups, switch back to the student, and show that the banner disappears and marks are now visible. This demonstrates the real-time permission + publication gating system.

---

## F. Known Limitations

1. **Report Card print format is empty** — The Jinja template exists but has no HTML content. Marks/grades are visible in the portal Results page, but no printable report card is generated.

2. **Library fine auto-creates Fees without review** — Overdue returns immediately create a Fee record. No approval workflow for fine amounts.

3. **dispatch_notice is a stub** — Creates Communication Log entries but does not send real emails or SMS. Gateway integration is future scope.

4. **Student status field added late** — The `status` field (Active/Graduated/Expired) was backfilled in Stage 8. Historical records before Stage 8 had no explicit status.

5. **No real payment gateway** — Fee Payments are manual-entry records. No Razorpay/Stripe integration.

6. **Idempotency drift on demo data re-runs** — Running `generate_demo_data.py` multiple times may produce slightly different record counts or IDs. The system is designed for a clean initial load, not idempotent re-runs.

7. **Guardian naming format** — Uses `format:{guardian_name}-{###}` which can produce non-unique names if two guardians share the same name.

8. **Vehicle.driver_phone is Data, not Phone** — Uses Data fieldtype to avoid Frappe v16's country-code validation issues with Indian phone numbers.

9. **Dashboard created programmatically** — The Institution Overview Dashboard was created via `frappe.get_doc()` rather than app JSON, because Frappe v16 doesn't auto-sync non-standard Dashboard instances.

10. **Cockpit stats may lag behind Desk data** — Cockpit pages call whitelisted APIs that aggregate data. If a record is created in Desk and the cockpit tab isn't refreshed, the stats may be stale. This is expected SPA behavior, not a bug.

---

## G. Future Roadmap

- **LMS Module** — Course content, assignments, online submission, graded coursework
- **HR/Payroll** — Employee profiles, leave management, salary processing extending Staff Attendance
- **Payment Gateway** — Razorpay/Stripe integration for online fee collection with receipt generation
- **Real SMS/Email** — SMTP/Twilio integration replacing the dispatch_notice stub
- **Mobile App** — REST API exposure of existing whitelisted methods for native mobile consumption
- **Print Format Suite** — Report Card, Fee Receipt, ID Card print formats with institution branding
- **Batch/Section Management** — Academic batch and section concepts for multi-year cohort tracking
- **Hostel Mess** — Meal planning, mess attendance, dietary preferences
- **Cockpit customization** — Allow staff to rearrange/hide stat cards and quick actions per preference
