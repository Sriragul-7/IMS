# Demo Readiness Checklist — Institution ERP

**Run through this 30 minutes before presenting.** Each item is a literal action.

---

## Pre-Demo Setup (30 min before)

- [ ] **Start bench** — `bench start` in the frappe-bench directory. Confirm it says "Running on http://0.0.0.0:8000"
- [ ] **Clear browser cache** — In Chrome: Ctrl+Shift+Delete → "Cached images and files" → Clear. Or use Ctrl+Shift+R for hard reload
- [ ] **Open incognito/private window** — This ensures no leftover sessions or cached CSS. Use this for the actual demo
- [ ] **Open DEMO_CREDENTIALS.md** in a second tab — Keep it handy for quick copy-paste of email addresses
- [ ] **Verify site is reachable** — Open `http://localhost:8000` in the incognito window. Should show Frappe login page or portal

## Smoke Test (5 min)

- [ ] **Test rich student account** — Login as `richdemo@demo.institution.local` / `Demo@2026`
  - Should land on Student Dashboard with stat cards (Attendance %, Fees, Library)
  - Click "Attendance" in sidebar → should show 50 records with colored status badges
  - Click "Results" → should show 6 result cards + blue "Results Not Yet Published" banner
  - Click "Library" → should show 3 active book issues
  - Logout
- [ ] **Test rich guardian account** — Login as `guardian1@demo.institution.local` / `Demo@2026`
  - Should land on Guardian Dashboard
  - Verify child switcher in sidebar shows 2 children
  - Switch to second child → data should update
  - Logout
- [ ] **Test one staff cockpit** — Login as `instructor1@demo.institution.local` / `Demo@2026`
  - Should land on Instructor Cockpit (not Desk directly)
  - Should show attendance summary stats and pending assessments
  - Click "Open Full Desk" → should open Desk in new tab
  - Logout

## During Demo

- [ ] **Start with the 60-second pitch** (Section A of DEMO_WALKTHROUGH.md)
- [ ] **Show student portal first** — Use `richdemo@demo.institution.local`
  - Dashboard → Attendance → Results (call out the "Not Published" banner) → Fees → Library
- [ ] **Show guardian portal** — Use `guardian1@demo.institution.local`
  - Dashboard → Child Switcher → switch child → verify data changes
- [ ] **Show staff cockpit** — Use `instructor1@demo.institution.local`
  - Cockpit → stats → "Open Full Desk" → show filtered Course Schedule
- [ ] **Show admissions pipeline** — Use `admissions@demo.institution.local`
  - Admissions Cockpit → pipeline stages → Desk → Student Applicant workflow
- [ ] **Show fee management** — Use `feemanager@demo.institution.local`
  - Fee Manager Cockpit → collection overview → Desk → Fee records with status badges
- [ ] **Show Admin Cockpit** — Use `admin@demo.institution.local`
  - Admin Cockpit → institution-wide stats → module quick access

## Post-Demo Cleanup

- [ ] **Close all browser tabs** — Ensure no sessions remain
- [ ] **Stop bench** — `Ctrl+C` in the bench terminal (if needed)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Portal shows unstyled page | Run rebuild: `cd apps/institution_erp && npm run build && rm -rf institution_erp/public/portal && cp -r public/portal institution_erp/public/portal && bench --site institution.localhost clear-cache` |
| Login fails | Check `bench start` is running. Verify password is `Demo@2026` |
| Cockpit shows "Not authorized" | User may not have the right role. Check DEMO_CREDENTIALS.md for correct email |
| Desk looks unstyled (no Inter font) | Run `bench --site institution.localhost clear-cache` |
| "Results Not Yet Published" banner missing | This is expected — it only shows for unpublished assessment groups |
| Child switcher not showing | Guardian must have 2+ linked children. Use `guardian1@demo.institution.local` |
| Slow initial load | First visit after cache clear is slower. Subsequent loads are fast |

## Key Demo Accounts (Quick Reference)

| Account | Email | What to Show |
|---------|-------|-------------|
| Rich Student | `richdemo@demo.institution.local` | Full portal with data across all modules |
| Rich Guardian | `guardian1@demo.institution.local` | Child switcher, multi-student monitoring |
| Instructor | `instructor1@demo.institution.local` | Cockpit → attendance, assessments |
| Fee Manager | `feemanager@demo.institution.local` | Cockpit → fees, payments |
| System Manager | `admin@demo.institution.local` | Admin Cockpit → institution-wide overview |

**Password for all: `Demo@2026`**
