"""
Stage 4 Task 0: Create rich demo student portal account and update DEMO_CREDENTIALS.md.
Also ensure guardian1's children have data.
"""
import frappe

RICH_STUDENT = 'STU-2026-00079'
RICH_EMAIL = 'richdemo@demo.institution.local'
DEMO_PASSWORD = 'Demo@2026'

def run():
    frappe.set_user('Administrator')
    
    # 1. Create rich demo student user
    existing = frappe.db.exists('User', RICH_EMAIL)
    if not existing:
        student = frappe.get_doc('Student', RICH_STUDENT)
        full_name = ' '.join(filter(None, [student.first_name, student.middle_name, student.last_name]))
        
        user = frappe.get_doc({
            'doctype': 'User',
            'email': RICH_EMAIL,
            'first_name': student.first_name,
            'last_name': student.last_name or '',
            'user_type': 'Website User',
            'send_welcome_email': 0,
        })
        user.append('roles', {'role': 'Student'})
        user.insert(ignore_permissions=True)
        user.new_password = DEMO_PASSWORD
        user.save(ignore_permissions=True)
        print(f'Created user: {RICH_EMAIL}')
    else:
        print(f'User {RICH_EMAIL} already exists')
    
    # 2. Set User Permission
    existing_perm = frappe.db.exists('User Permission', {
        'user': RICH_EMAIL, 'allow': 'Student', 'for_value': RICH_STUDENT
    })
    if not existing_perm:
        frappe.get_doc({
            'doctype': 'User Permission',
            'user': RICH_EMAIL,
            'allow': 'Student',
            'for_value': RICH_STUDENT,
        }).insert(ignore_permissions=True)
        print(f'Set User Permission: {RICH_EMAIL} -> Student {RICH_STUDENT}')
    else:
        print(f'Permission already exists')
    
    # 3. Verify data
    print(f'\nData for {RICH_STUDENT}:')
    for doctype, label in [
        ('Student Attendance', 'Attendance'),
        ('Assessment Result', 'Results'),
        ('Fees', 'Fees'),
        ('Fee Payment', 'Fee Payments'),
        ('Library Transaction', 'Library'),
        ('Feedback', 'Feedback'),
    ]:
        count = len(frappe.get_all(doctype, filters={'student': RICH_STUDENT}, limit=100))
        print(f'  {label}: {count} records')
    
    frappe.db.commit()
    print(f'\nRich demo student: {RICH_EMAIL} / {DEMO_PASSWORD}')
