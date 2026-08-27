import frappe
from frappe.utils import today, add_days


def execute():
    print("=" * 60)
    print("STAGE 6 E2E TEST: Library, Hostel, Transport")
    print("=" * 60)

    results = {}

    try:
        cleanup()
        results.update(block_0_library())
        results.update(block_1_hostel())
        results.update(block_2_transport())
        results.update(block_3_reports())
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
        print("\n[Cleanup] Test data removed.")

    print("\n" + "=" * 60)
    print("STAGE 6 E2E TEST SUMMARY")
    print("=" * 60)
    all_pass = True
    for block, passed in results.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  {block}: {status}")

    print("\n" + "=" * 60)
    if all_pass:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("=" * 60)


def cleanup():
    for dt in [
        "Library Transaction", "Library Membership", "Library Item", "Book Category",
        "Hostel Room Allocation", "Hostel Room", "Hostel",
        "Student Transport Allocation", "Transport Route", "Vehicle",
        "Fees", "Fee Payment",
    ]:
        names = frappe.get_all(dt, pluck="name")
        for n in names:
            try:
                frappe.delete_doc(dt, n, force=True, ignore_permissions=True)
            except Exception:
                pass
    frappe.db.commit()


def ensure_students():
    existing = frappe.get_all("Student", pluck="name")
    if existing:
        return existing[:2]
    students = []
    for i, first in enumerate(["LibTest", "LibTest2"], 1):
        doc = frappe.get_doc({
            "doctype": "Student",
            "first_name": first,
            "last_name": "Student",
            "gender": "Male",
            "date_of_birth": "2000-01-01",
            "guardian": ensure_guardian(),
        })
        doc.insert(ignore_permissions=True)
        students.append(doc.name)
    frappe.db.commit()
    return students


def ensure_guardian():
    existing = frappe.get_all("Guardian", pluck="name")
    if existing:
        return existing[0]
    doc = frappe.get_doc({
        "doctype": "Guardian",
        "guardian_name": "Lib Test Guardian",
        "relation_to_student": "Father",
        "email_address": "lib.guardian@test.com",
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


# ---------------------------------------------------------------------------
# BLOCK 0: LIBRARY
# ---------------------------------------------------------------------------

def block_0_library():
    print("\n[0] LIBRARY TESTS")
    results = {}
    students = ensure_students()
    student1, student2 = students[0], students[1]

    print("  [0a] Creating Book Category...")
    cat_name = "Fiction"
    if not frappe.db.exists("Book Category", {"category_name": cat_name}):
        cat = frappe.get_doc({"doctype": "Book Category", "category_name": cat_name})
        cat.insert(ignore_permissions=True)
        frappe.db.commit()
    print(f"    Book Category '{cat_name}' ready.")

    print("  [0b] Creating Book (2 copies)...")
    book = frappe.get_doc({
        "doctype": "Library Item",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "978-0743273565",
        "book_category": cat_name,
        "publisher": "Scribner",
        "total_copies": 2,
    })
    book.insert(ignore_permissions=True)
    frappe.db.commit()
    item_name = book.name
    print(f"    Book created: {item_name}, available_copies={book.available_copies}")
    results["book_creation"] = book.available_copies == 2

    print("  [0c] Creating Library Membership for student1...")
    mem1 = frappe.get_doc({
        "doctype": "Library Membership",
        "student": student1,
        "valid_upto": add_days(today(), 365),
        "max_books_allowed": 3,
    })
    mem1.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"    Membership created: {mem1.name}, status={mem1.status}")
    results["membership_creation"] = mem1.status == "Active"

    print("  [0d] Issuing book to student1...")
    txn1 = frappe.get_doc({
        "doctype": "Library Transaction",
        "student": student1,
        "library_item": item_name,
        "transaction_type": "Issue",
        "transaction_date": today(),
    })
    txn1.insert(ignore_permissions=True)
    txn1.submit()
    frappe.db.commit()
    item = frappe.get_doc("Library Item", item_name)
    print(f"    Issue to student1: status={txn1.status}, available_copies={item.available_copies}")
    results["issue_student1"] = txn1.status == "Issued" and item.available_copies == 1

    print("  [0e] Creating Membership for student2 and issuing...")
    mem2 = frappe.get_doc({
        "doctype": "Library Membership",
        "student": student2,
        "valid_upto": add_days(today(), 365),
        "max_books_allowed": 3,
    })
    mem2.insert(ignore_permissions=True)
    frappe.db.commit()

    txn2 = frappe.get_doc({
        "doctype": "Library Transaction",
        "student": student2,
        "library_item": item_name,
        "transaction_type": "Issue",
        "transaction_date": today(),
    })
    txn2.insert(ignore_permissions=True)
    txn2.submit()
    frappe.db.commit()
    item = frappe.get_doc("Library Item", item_name)
    print(f"    Issue to student2: status={txn2.status}, available_copies={item.available_copies}")
    results["issue_student2"] = txn2.status == "Issued" and item.available_copies == 0

    print("  [0f] Attempting 3rd issue (should fail — no copies)...")
    student3 = ensure_students_extra()[0]
    mem3 = frappe.get_doc({
        "doctype": "Library Membership",
        "student": student3,
        "valid_upto": add_days(today(), 365),
        "max_books_allowed": 3,
    })
    try:
        mem3.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()

    txn3 = frappe.get_doc({
        "doctype": "Library Transaction",
        "student": student3,
        "library_item": item_name,
        "transaction_type": "Issue",
        "transaction_date": today(),
    })
    try:
        txn3.insert(ignore_permissions=True)
        frappe.db.commit()
        print("    ERROR: 3rd issue should have been rejected!")
        results["issue_3rd_rejected"] = False
    except Exception as e:
        frappe.db.rollback()
        print(f"    Correctly rejected: {str(e)[:80]}")
        results["issue_3rd_rejected"] = True

    print("  [0g] Returning book from student1 (late — fine calculation)...")
    txn_ret = frappe.get_doc({
        "doctype": "Library Transaction",
        "student": student1,
        "library_item": item_name,
        "transaction_type": "Return",
        "transaction_date": today(),
        "return_date": add_days(today(), 16),
    })
    txn_ret.insert(ignore_permissions=True)
    txn_ret.submit()
    frappe.db.commit()
    item = frappe.get_doc("Library Item", item_name)
    print(f"    Return: fine_amount={txn_ret.fine_amount}, status={txn_ret.status}, available_copies={item.available_copies}")
    results["return_late_fine"] = txn_ret.fine_amount == 10 and item.available_copies == 1

    return results


def ensure_students_extra():
    students = frappe.get_all("Student", pluck="name")
    if len(students) >= 3:
        return [students[2]]
    doc = frappe.get_doc({
        "doctype": "Student",
        "first_name": "LibTest3",
        "last_name": "Student",
        "gender": "Male",
        "date_of_birth": "2000-01-01",
        "guardian": ensure_guardian(),
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return [doc.name]


# ---------------------------------------------------------------------------
# BLOCK 1: HOSTEL
# ---------------------------------------------------------------------------

def block_1_hostel():
    print("\n[1] HOSTEL TESTS")
    results = {}
    students = frappe.get_all("Student", fields=["name"], limit_page_length=3)
    student_names = [s.name for s in students]
    while len(student_names) < 2:
        extra = ensure_students_extra()
        student_names.append(extra[0])

    print("  [1a] Creating Hostel and Room (capacity 2)...")
    hostel = frappe.get_doc({
        "doctype": "Hostel",
        "hostel_name": "Test Block A",
        "hostel_type": "Boys",
        "address": "123 Test Street",
    })
    hostel.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"    Hostel created: {hostel.name}")

    room = frappe.get_doc({
        "doctype": "Hostel Room",
        "hostel": hostel.name,
        "room_number": "A-101",
        "room_type": "Double",
        "capacity": 2,
    })
    room.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"    Room created: {room.name}, capacity={room.capacity}, occupied={room.occupied_count}")
    results["room_creation"] = room.occupied_count == 0

    print("  [1b] Allocating student1 to room...")
    alloc1 = frappe.get_doc({
        "doctype": "Hostel Room Allocation",
        "student": student_names[0],
        "hostel_room": room.name,
        "allocation_date": today(),
    })
    alloc1.insert(ignore_permissions=True)
    frappe.db.commit()
    room = frappe.get_doc("Hostel Room", room.name)
    print(f"    Allocated student1: occupied_count={room.occupied_count}")
    results["alloc_student1"] = room.occupied_count == 1

    print("  [1c] Allocating student2 to room...")
    alloc2 = frappe.get_doc({
        "doctype": "Hostel Room Allocation",
        "student": student_names[1],
        "hostel_room": room.name,
        "allocation_date": today(),
    })
    alloc2.insert(ignore_permissions=True)
    frappe.db.commit()
    room = frappe.get_doc("Hostel Room", room.name)
    print(f"    Allocated student2: occupied_count={room.occupied_count}")
    results["alloc_student2"] = room.occupied_count == 2

    print("  [1d] Attempting 3rd allocation (should fail — room full)...")
    student3_names = ensure_students_extra()
    alloc3 = frappe.get_doc({
        "doctype": "Hostel Room Allocation",
        "student": student3_names[0],
        "hostel_room": room.name,
        "allocation_date": today(),
    })
    try:
        alloc3.insert(ignore_permissions=True)
        frappe.db.commit()
        print("    ERROR: 3rd allocation should have been rejected!")
        results["alloc_3rd_rejected"] = False
    except Exception as e:
        frappe.db.rollback()
        print(f"    Correctly rejected: {str(e)[:80]}")
        results["alloc_3rd_rejected"] = True

    print("  [1e] Vacating student1...")
    alloc1 = frappe.get_doc("Hostel Room Allocation", alloc1.name)
    alloc1.status = "Vacated"
    alloc1.vacate_date = today()
    alloc1.save(ignore_permissions=True)
    frappe.db.commit()
    room = frappe.get_doc("Hostel Room", room.name)
    print(f"    Vacated student1: occupied_count={room.occupied_count}")
    results["vacate_student1"] = room.occupied_count == 1

    return results


# ---------------------------------------------------------------------------
# BLOCK 2: TRANSPORT
# ---------------------------------------------------------------------------

def block_2_transport():
    print("\n[2] TRANSPORT TESTS")
    results = {}
    student_names = [s.name for s in frappe.get_all("Student", fields=["name"], limit_page_length=3)]

    print("  [2a] Creating Vehicle and Route (capacity 2)...")
    vehicle = frappe.get_doc({
        "doctype": "Vehicle",
        "vehicle_number": "TN-01-TEST-6666",
        "capacity": 2,
        "driver_name": "Test Driver",
        "driver_phone": "9876543210",
    })
    vehicle.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"    Vehicle created: {vehicle.name}")

    route = frappe.get_doc({
        "doctype": "Transport Route",
        "route_name": "Campus Route 1",
        "vehicle": vehicle.name,
        "fee_amount": 5000,
        "stops": [
            {"stop_name": "Main Gate", "stop_order": 1, "pickup_time": "07:00:00"},
            {"stop_name": "Library Junction", "stop_order": 2, "pickup_time": "07:15:00"},
            {"stop_name": "Hostel Block", "stop_order": 3, "pickup_time": "07:30:00"},
        ],
    })
    route.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"    Route created: {route.name}, stops={len(route.stops)}")
    results["route_creation"] = len(route.stops) == 3

    print("  [2b] Allocating student1 to route...")
    alloc1 = frappe.get_doc({
        "doctype": "Student Transport Allocation",
        "student": student_names[0],
        "transport_route": route.name,
        "pickup_stop": "Main Gate",
        "allocation_date": today(),
    })
    alloc1.insert(ignore_permissions=True)
    frappe.db.commit()
    count = frappe.db.count("Student Transport Allocation", {"transport_route": route.name, "status": "Active"})
    print(f"    Allocated student1: active_allocations={count}")
    results["transport_alloc_student1"] = count == 1

    print("  [2c] Allocating student2 to route...")
    alloc2 = frappe.get_doc({
        "doctype": "Student Transport Allocation",
        "student": student_names[1],
        "transport_route": route.name,
        "pickup_stop": "Library Junction",
        "allocation_date": today(),
    })
    alloc2.insert(ignore_permissions=True)
    frappe.db.commit()
    count = frappe.db.count("Student Transport Allocation", {"transport_route": route.name, "status": "Active"})
    print(f"    Allocated student2: active_allocations={count}")
    results["transport_alloc_student2"] = count == 2

    print("  [2d] Attempting 3rd allocation (should fail — vehicle full)...")
    student3 = ensure_students_extra()[0]
    alloc3 = frappe.get_doc({
        "doctype": "Student Transport Allocation",
        "student": student3,
        "transport_route": route.name,
        "pickup_stop": "Hostel Block",
        "allocation_date": today(),
    })
    try:
        alloc3.insert(ignore_permissions=True)
        frappe.db.commit()
        print("    ERROR: 3rd allocation should have been rejected!")
        results["transport_alloc_3rd_rejected"] = False
    except Exception as e:
        frappe.db.rollback()
        print(f"    Correctly rejected: {str(e)[:80]}")
        results["transport_alloc_3rd_rejected"] = True

    return results


# ---------------------------------------------------------------------------
# BLOCK 3: REPORTS
# ---------------------------------------------------------------------------

def block_3_reports():
    print("\n[3] REPORTS")
    results = {}

    print("  [3a] Library Circulation Report...")
    from institution_erp.library.report.library_circulation import library_circulation
    cols, data, _, _ = library_circulation.execute()
    print(f"    Returned {len(data)} rows, {len(cols)} columns")
    results["library_circulation_report"] = len(cols) > 0

    print("  [3b] Hostel Occupancy Report...")
    from institution_erp.hostel.report.hostel_occupancy import hostel_occupancy
    cols, data, _, _ = hostel_occupancy.execute()
    print(f"    Returned {len(data)} rows, {len(cols)} columns")
    results["hostel_occupancy_report"] = len(cols) > 0

    print("  [3c] Transport Route Utilization Report...")
    from institution_erp.transport.report.transport_route_utilization import transport_route_utilization
    cols, data, _, _ = transport_route_utilization.execute()
    print(f"    Returned {len(data)} rows, {len(cols)} columns")
    results["transport_utilization_report"] = len(cols) > 0

    return results
