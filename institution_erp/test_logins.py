"""
Comprehensive demo account login test for Frappe v16 site "institution.localhost".
Tests all 14 demo accounts via API, checks DB records, runs 3 iterations.
"""
import frappe
import requests
import json
import time


SITE_URL = "http://localhost:8000"
DEFAULT_PASSWORD = "Demo@2026"

ACCOUNTS = [
    # (email, role_description, user_type, expected_home_page)
    ("richdemo@demo.institution.local", "Student", "Website User", "/institution-portal"),
    ("student1@demo.institution.local", "Student", "Website User", "/institution-portal"),
    ("student2@demo.institution.local", "Student", "Website User", "/institution-portal"),
    ("student3@demo.institution.local", "Student", "Website User", "/institution-portal"),
    ("guardian1@demo.institution.local", "Guardian", "Website User", "/institution-portal"),
    ("guardian2@demo.institution.local", "Guardian", "Website User", "/institution-portal"),
    ("admin@demo.institution.local", "Administrator", "System User", "/app"),
    ("admissions@demo.institution.local", "Admissions Officer", "System User", "/app"),
    ("academichead@demo.institution.local", "Academic Head", "System User", "/app"),
    ("instructor1@demo.institution.local", "Instructor", "System User", "/app"),
    ("instructor2@demo.institution.local", "Instructor", "System User", "/app"),
    ("feemanager@demo.institution.local", "Fee Manager", "System User", "/app"),
    ("facilitymanager@demo.institution.local", "Facility Manager", "System User", "/app"),
    ("comms.officer@demo.institution.local", "Communication Officer", "System User", "/app"),
]


def check_db_records():
    """Check User records in the database for all demo accounts."""
    print("\n" + "=" * 80)
    print("DATABASE RECORD CHECKS")
    print("=" * 80)

    results = {}
    for email, role, user_type, expected_hp in ACCOUNTS:
        info = {
            "email": email,
            "role": role,
            "expected_type": user_type,
            "user_exists": False,
            "enabled": False,
            "user_type": None,
            "full_name": None,
            "password_hash_set": False,
            "has_roles": [],
            "duplicate_emails": 0,
        }

        # Check if user exists (multiple records = duplicate)
        users = frappe.get_all(
            "User",
            filters={"email": email},
            fields=["name", "enabled", "user_type", "full_name"],
        )
        info["duplicate_emails"] = len(users)

        if users:
            info["user_exists"] = True
            u = users[0]
            info["enabled"] = u.get("enabled") == 1
            info["user_type"] = u.get("user_type")
            info["full_name"] = u.get("full_name")
            info["status"] = "ENABLED" if info["enabled"] else "DISABLED"

            # Check password hash in __Auth table
            try:
                auth_row = frappe.db.sql(
                    "SELECT name, password FROM `__Auth` WHERE name=%s AND password IS NOT NULL AND password != ''",
                    (email,),
                    as_dict=True,
                )
                info["password_hash_set"] = len(auth_row) > 0
            except Exception as e:
                info["password_hash_set_error"] = str(e)

            # Get user roles
            try:
                info["has_roles"] = list(frappe.get_roles(email))
            except Exception:
                pass
        else:
            info["status"] = "USER_NOT_FOUND"

        results[email] = info

        status_icon = "OK" if info["user_exists"] and info["enabled"] else "FAIL"
        print(f"\n  [{status_icon}] {email}")
        print(f"       Exists: {info['user_exists']} | Enabled: {info['enabled']} | Type: {info['user_type']}")
        print(f"       Full Name: {info['full_name']}")
        print(f"       Password Hash Set: {info['password_hash_set']}")
        print(f"       Duplicate Records: {info['duplicate_emails']}")
        print(f"       Roles ({len(info['has_roles'])}): {', '.join(info['has_roles'][:10])}")

    return results


def test_api_login():
    """Test login via the Frappe API for all accounts. Run 3 iterations."""
    all_results = {}

    for iteration in range(1, 4):
        print("\n" + "=" * 80)
        print(f"LOGIN TEST - RUN {iteration} of 3")
        print("=" * 80)

        run_results = []
        for email, role, user_type, expected_hp in ACCOUNTS:
            result = {
                "email": email,
                "role": role,
                "user_type": user_type,
                "expected_home_page": expected_hp,
                "login_success": False,
                "full_name": None,
                "home_page": None,
                "message": None,
                "app_access": None,
                "home_page_match": None,
            }

            # Step 1: Attempt login via POST
            try:
                resp = requests.post(
                    f"{SITE_URL}/api/method/login",
                    data={"usr": email, "pwd": DEFAULT_PASSWORD},
                    timeout=15,
                    allow_redirects=False,
                )
                result["status_code"] = resp.status_code

                try:
                    body = resp.json()
                except Exception:
                    body = {"text": resp.text[:500]}

                # Frappe v16 returns: {"message": "Logged In", "full_name": "...", "home_page": "..."}
                # on success with HTTP 200
                if resp.status_code == 200:
                    msg = body.get("message", "")
                    result["login_success"] = True
                    result["full_name"] = body.get("full_name")
                    result["home_page"] = body.get("home_page")
                    result["message"] = msg if isinstance(msg, str) else str(msg)

                    # Check home_page for website users
                    if user_type == "Website User":
                        hp = result["home_page"]
                        if hp:
                            result["home_page_match"] = hp.startswith("/institution-portal") or hp == expected_hp
                        else:
                            result["home_page_match"] = False
                            result["message"] = f"No home_page in response"
                    else:
                        result["home_page_match"] = True

                    # Step 2: For system users, check /app access
                    if user_type == "System User":
                        cookies = resp.cookies
                        try:
                            app_resp = requests.get(
                                f"{SITE_URL}/app",
                                cookies=cookies,
                                timeout=15,
                                allow_redirects=False,
                            )
                            result["app_access"] = app_resp.status_code
                        except Exception as e:
                            result["app_access"] = f"ERROR: {e}"

                elif resp.status_code in (303, 302):
                    location = resp.headers.get("Location", "")
                    if "login" not in location.lower():
                        result["login_success"] = True
                        result["message"] = f"Redirect to {location} (indicates success)"
                    else:
                        result["message"] = f"Redirected back to login: {location}"
                else:
                    result["message"] = str(body.get("message", body.get("_server_messages", str(body)[:300])))

            except requests.exceptions.ConnectionError:
                result["message"] = "CONNECTION ERROR - site not reachable"
            except requests.exceptions.Timeout:
                result["message"] = "TIMEOUT"
            except Exception as e:
                result["message"] = f"EXCEPTION: {str(e)[:200]}"

            run_results.append(result)

            # Print per-user result
            status_icon = "PASS" if result["login_success"] else "FAIL"
            hp_info = ""
            if user_type == "Website User":
                match_str = "OK" if result["home_page_match"] else "MISMATCH"
                hp_info = f" | home_page={result['home_page']} [{match_str}]"
            elif user_type == "System User":
                hp_info = f" | home_page={result['home_page']}"

            app_info = ""
            if user_type == "System User" and result["app_access"] is not None:
                app_ok = result["app_access"] == 200
                app_info = f" | /app={result['app_access']} [{'OK' if app_ok else 'FAIL'}]"

            print(f"\n  [{status_icon}] {email}")
            print(f"       Role: {role} | Type: {user_type}")
            print(f"       Full Name: {result['full_name']}{hp_info}{app_info}")
            if result["message"]:
                print(f"       Details: {result['message']}")

        all_results[f"run_{iteration}"] = run_results

    return all_results


def run():
    """Main entry point - run via bench execute."""
    print("=" * 80)
    print("DEMO ACCOUNT COMPREHENSIVE LOGIN TEST")
    print(f"Site: institution.localhost | URL: {SITE_URL}")
    print(f"Password: {DEFAULT_PASSWORD}")
    print(f"Total Accounts: {len(ACCOUNTS)}")
    print(f"Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Phase 1: Database checks
    db_results = check_db_records()

    # Phase 2: API login tests (3 runs)
    api_results = test_api_login()

    # Phase 3: Summary
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)

    for iteration in range(1, 4):
        run_key = f"run_{iteration}"
        results = api_results[run_key]
        pass_count = sum(1 for r in results if r["login_success"])
        fail_count = len(results) - pass_count

        print(f"\n--- Run {iteration}: {pass_count} PASS / {fail_count} FAIL out of {len(results)} ---")
        for r in results:
            status = "PASS" if r["login_success"] else "FAIL"
            parts = []
            if r["user_type"] == "Website User":
                match = "OK" if r.get("home_page_match") else "MISMATCH"
                parts.append(f"home_page={r.get('home_page', 'N/A')} [{match}]")
            elif r["user_type"] == "System User":
                parts.append(f"home_page={r.get('home_page', 'N/A')}")
                parts.append(f"/app={r.get('app_access', 'N/A')}")

            extra = " | ".join(parts)
            print(f"  [{status}] {r['email']} | {extra}")
            if r["message"]:
                print(f"         -> {r['message']}")

    # DB summary
    print("\n--- Database Record Summary ---")
    disabled_count = 0
    not_found_count = 0
    duplicate_count = 0
    no_hash_count = 0

    for email, info in db_results.items():
        if not info["user_exists"]:
            not_found_count += 1
        if info["user_exists"] and not info["enabled"]:
            disabled_count += 1
        if info["duplicate_emails"] > 1:
            duplicate_count += 1
        if info["user_exists"] and not info["password_hash_set"]:
            no_hash_count += 1

    print(f"  Users Found: {len(ACCOUNTS) - not_found_count}/{len(ACCOUNTS)}")
    print(f"  Users Enabled: {len(ACCOUNTS) - disabled_count}/{len(ACCOUNTS)}")
    print(f"  Duplicate Emails: {duplicate_count}")
    print(f"  Missing Password Hash: {no_hash_count}")

    if disabled_count > 0:
        print("\n  DISABLED USERS:")
        for email, info in db_results.items():
            if info["user_exists"] and not info["enabled"]:
                print(f"    - {email}")

    if not_found_count > 0:
        print("\n  USERS NOT IN DATABASE:")
        for email, info in db_results.items():
            if not info["user_exists"]:
                print(f"    - {email}")

    if no_hash_count > 0:
        print("\n  USERS WITHOUT PASSWORD HASH:")
        for email, info in db_results.items():
            if info["user_exists"] and not info["password_hash_set"]:
                print(f"    - {email}")

    # Check consistency across runs
    print("\n--- Cross-Run Consistency ---")
    for i, acct in enumerate(ACCOUNTS):
        email = acct[0]
        statuses = [api_results[f"run_{j}"][i]["login_success"] for j in range(1, 4)]
        if all(statuses):
            print(f"  [OK] {email}: PASS/PASS/PASS")
        elif not any(statuses):
            print(f"  [FAIL] {email}: FAIL/FAIL/FAIL")
        else:
            print(f"  [FLAKY] {email}: {'/'.join('PASS' if s else 'FAIL' for s in statuses)}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    return {"db_results": db_results, "api_results": api_results}
