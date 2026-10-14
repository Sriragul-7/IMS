#!/usr/bin/env python3
"""
Generate real diagrams for the report using Graphviz.
Outputs high-resolution PNG files to ../images/
"""
import os
import subprocess
from pathlib import Path

IMAGES_DIR = Path(__file__).parent.parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)

def run_dot(dot_content, filename):
    """Render a Graphviz DOT file to PNG."""
    dot_file = IMAGES_DIR / f"{filename}.dot"
    png_file = IMAGES_DIR / f"{filename}.png"
    dot_file.write_text(dot_content)
    try:
        subprocess.run(["dot", "-Tpng", "-Gdpi=300", str(dot_file), "-o", str(png_file)], 
                       check=True, capture_output=True)
        print(f"Generated: {png_file}")
        return png_file
    except subprocess.CalledProcessError as e:
        print(f"Error generating {filename}: {e.stderr.decode()}")
        return None
    except FileNotFoundError:
        print("Graphviz 'dot' not installed. Install with: apt-get install graphviz")
        return None

# ============================================================
# Figure 3.1: Technology Stack Diagram
# ============================================================
tech_stack = '''
digraph TechStack {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=11, style=filled, fillcolor="#f0f4f8", shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=10];
    
    subgraph cluster_presentation {
        label="Presentation Layer";
        style=dashed;
        color="#64748b";
        Portal [label="Vue 3 SPA\\n(Student/Guardian Portal)", fillcolor="#dbeafe"];
        Cockpit [label="Vue 3 Cockpits\\n(7 Staff Roles)", fillcolor="#dbeafe"];
        Desk [label="Frappe Desk\\n(Rebranded: Inter + BIT Blue)", fillcolor="#fef3c7"];
    }
    
    subgraph cluster_api {
        label="API Layer";
        style=dashed;
        color="#64748b";
        Whitelisted [label="11 Whitelisted Methods\\n(frappe.call / REST)", fillcolor="#dcfce7"];
        REST [label="Frappe REST API\\n(DocType CRUD)", fillcolor="#dcfce7"];
    }
    
    subgraph cluster_logic {
        label="Business Logic Layer";
        style=dashed;
        color="#64748b";
        Controllers [label="DocType Controllers\\n(22 files, validation)", fillcolor="#fce7f3"];
        Hooks [label="Hooks & Events\\n(on_update, on_submit)", fillcolor="#fce7f3"];
        Permissions [label="16 permission_query_conditions\\n(Row-level Security)", fillcolor="#fce7f3"];
        Workflows [label="Workflow Engine\\n(Student Applicant, Fee Discount)", fillcolor="#fce7f3"];
    }
    
    subgraph cluster_data {
        label="Data Layer";
        style=dashed;
        color="#64748b";
        MariaDB [label="MariaDB 10.6+\\n(48 DocTypes, 8 Child Tables)", fillcolor="#fef3c7"];
        Redis [label="Redis 7+\\n(Caching, Sessions, Queues)", fillcolor="#fef3c7"];
    }
    
    Portal -> Whitelisted;
    Cockpit -> Whitelisted;
    Desk -> REST;
    Whitelisted -> Controllers;
    Whitelisted -> Permissions;
    REST -> Controllers;
    Controllers -> Hooks;
    Controllers -> Workflows;
    Hooks -> MariaDB;
    Controllers -> MariaDB;
    Permissions -> MariaDB;
    Workflows -> MariaDB;
    Controllers -> Redis;
}
'''
run_dot(tech_stack, "fig3_1_tech_stack")

# ============================================================
# Figure 4.1: System Architecture Diagram (Layered)
# ============================================================
sys_arch = '''
digraph SysArch {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=11, style=filled, shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=10];
    
    subgraph cluster_user {
        label="Users";
        style=dashed;
        Student [label="Student", fillcolor="#dbeafe"];
        Guardian [label="Guardian", fillcolor="#dbeafe"];
        Instructor [label="Instructor", fillcolor="#fef3c7"];
        Admissions [label="Admissions Officer", fillcolor="#fef3c7"];
        FeeMgr [label="Fee Manager", fillcolor="#fef3c7"];
        FacilityMgr [label="Facility Manager", fillcolor="#fef3c7"];
        CommOfficer [label="Comm Officer", fillcolor="#fef3c7"];
        AcademicHead [label="Academic Head", fillcolor="#fef3c7"];
        SysMgr [label="System Manager", fillcolor="#fce7f3"];
    }
    
    subgraph cluster_frontend {
        label="Frontend";
        style=dashed;
        PortalUI [label="Vue 3 Portal SPA\\n/institution-portal", fillcolor="#dbeafe", shape=component];
        CockpitUI [label="Vue 3 Staff Cockpits\\n/institution-portal/<role>", fillcolor="#fef3c7", shape=component];
        DeskUI [label="Frappe Desk (Rebranded)\\n/app", fillcolor="#fce7f3", shape=component];
    }
    
    subgraph cluster_backend {
        label="Backend (Frappe v16.26.3)";
        style=dashed;
        Auth [label="Authentication\\nJWT + Session", fillcolor="#fce7f3"];
        API [label="Whitelisted API (11 methods)", fillcolor="#dcfce7"];
        Controllers [label="DocType Controllers\\n(Validation, Hooks)", fillcolor="#fce7f3"];
        PermQC [label="permission_query_conditions\\n(16 functions)", fillcolor="#fce7f3"];
    }
    
    subgraph cluster_db {
        label="Database";
        style=dashed;
        MariaDB [label="MariaDB\\n48 DocTypes", fillcolor="#fef3c7", shape=cylinder];
        Redis [label="Redis\\nCache/Queue/Session", fillcolor="#fef3c7", shape=cylinder];
    }
    
    Student -> PortalUI;
    Guardian -> PortalUI;
    Instructor -> CockpitUI;
    Admissions -> CockpitUI;
    FeeMgr -> CockpitUI;
    FacilityMgr -> CockpitUI;
    CommOfficer -> CockpitUI;
    AcademicHead -> CockpitUI;
    SysMgr -> CockpitUI;
    
    CockpitUI -> DeskUI [label="Open Full Desk", style=dashed, color="#64748b"];
    
    PortalUI -> Auth;
    CockpitUI -> Auth;
    DeskUI -> Auth;
    
    PortalUI -> API;
    CockpitUI -> API;
    DeskUI -> API [label="REST/Desk API"];
    
    API -> Controllers;
    Controllers -> PermQC;
    Controllers -> MariaDB;
    Controllers -> Redis;
    PermQC -> MariaDB;
}
'''
run_dot(sys_arch, "fig4_1_sys_arch")

# ============================================================
# Figure 4.2: Module Dependency Graph
# ============================================================
module_dep = '''
digraph ModuleDep {
    rankdir=LR;
    node [fontname="Helvetica", fontsize=10, style=filled, shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=9];
    
    Academics [label="Academics\\n(10 DocTypes)", fillcolor="#dbeafe"];
    SIS [label="SIS\\n(2 DocTypes)", fillcolor="#dcfce7"];
    Admissions [label="Admissions\\n(5 DocTypes)", fillcolor="#fef3c7"];
    Attendance [label="Attendance\\n(2 DocTypes)", fillcolor="#fce7f3"];
    Examination [label="Examination\\n(5 DocTypes)", fillcolor="#ede9fe"];
    Fees [label="Fees\\n(9 DocTypes)", fillcolor="#fee2e2"];
    Library [label="Library\\n(4 DocTypes)", fillcolor="#dcfce7"];
    Hostel [label="Hostel\\n(3 DocTypes)", fillcolor="#fef3c7"];
    Transport [label="Transport\\n(4 DocTypes)", fillcolor="#fce7f3"];
    Communication [label="Communication\\n(4 DocTypes)", fillcolor="#ede9fe"];
    
    // Core dependencies
    SIS -> Academics [label="Student Group Member"];
    Admissions -> Academics [label="Program, Academic Year"];
    Admissions -> SIS [label="Creates Student+Guardian"];
    Attendance -> Academics [label="Course Schedule, Student Group"];
    Attendance -> SIS [label="Student, Instructor"];
    Examination -> Academics [label="Course, Student Group, Grading Scale"];
    Fees -> SIS [label="Student"];
    Fees -> Academics [label="Academic Year, Student Group"];
    Library -> SIS [label="Student"];
    Hostel -> SIS [label="Student"];
    Transport -> SIS [label="Student"];
    Communication -> SIS [label="Student, Guardian"];
    Communication -> Academics [label="Student Group, Program"];
}
'''
run_dot(module_dep, "fig4_2_module_dep")

# ============================================================
# Figure 4.3: Role-Permission Matrix (Heatmap style)
# ============================================================
role_matrix = '''
digraph RoleMatrix {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, shape=plaintext];
    
    // Title
    Title [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
        <TR><TD COLSPAN="11" ALIGN="CENTER"><FONT POINT-SIZE="14"><B>Role-Permission Matrix (Write Access)</B></FONT></TD></TR>
    </TABLE>>];
    
    // Header row
    Header [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Role</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Student</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Guardian</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Admissions</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Academic</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Instructor</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Fee Mgr</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Facility</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Comm</B></FONT></TD>
            <TD BGCOLOR="#1e40af"><FONT COLOR="white"><B>Sys Mgr</B></FONT></TD>
        </TR>
    </TABLE>>];
    
    // Data rows
    StudentRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Student</B></TD>
            <TD BGCOLOR="#dcfce7">Own</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD>
        </TR>
    </TABLE>>];
    
    GuardianRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Guardian</B></TD>
            <TD BGCOLOR="#dcfce7">Linked</TD><TD BGCOLOR="#dcfce7">Own</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD>
        </TR>
    </TABLE>>];
    
    AdmissionsRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Admissions</B></TD>
            <TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#fef3c7">Read</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    AcademicRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Academic Head</B></TD>
            <TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Read</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    InstructorRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Instructor</B></TD>
            <TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fef3c7">Read</TD><TD BGCOLOR="#dcfce7">Own Groups</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    FeeRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Fee Manager</B></TD>
            <TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    FacilityRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Facility Mgr</B></TD>
            <TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    CommRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>Comm Officer</B></TD>
            <TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#fee2e2">—</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    SysRec [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#f0f4f8"><B>System Mgr</B></TD>
            <TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD><TD BGCOLOR="#dcfce7">Full</TD>
        </TR>
    </TABLE>>];
    
    Legend [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#dcfce7">Full / Own / Linked</TD><TD BGCOLOR="#fef3c7">Read Only</TD><TD BGCOLOR="#fee2e2">No Access</TD></TR>
    </TABLE>>];
    
    Title -> Header -> StudentRec -> GuardianRec -> AdmissionsRec -> AcademicRec -> InstructorRec -> FeeRec -> FacilityRec -> CommRec -> SysRec -> Legend;
}
'''
run_dot(role_matrix, "fig4_3_role_matrix")

# ============================================================
# Figure 4.4: ER Diagram (Simplified key entities)
# ============================================================
er_diagram = '''
digraph ERDiagram {
    rankdir=LR;
    node [fontname="Helvetica", fontsize=10, shape=box, style=filled];
    edge [fontname="Helvetica", fontsize=9, arrowhead=crow, arrowtail=crow, dir=both];
    
    // Core entities
    Student [label=<<B>Student</B><BR/>STU-.YYYY.-.#####<BR/>first_name, last_name<BR/>program, guardian<BR/>email_address, status>, fillcolor="#dbeafe"];
    Guardian [label=<<B>Guardian</B><BR/>{name}-{###}<BR/>guardian_name<BR/>guardian_email<BR/>relation_to_student<BR/>phone_number>, fillcolor="#dbeafe"];
    Program [label=<<B>Program</B><BR/>field:program_name<BR/>program_code, department>, fillcolor="#dcfce7"];
    Course [label=<<B>Course</B><BR/>field:course_name<BR/>course_code, credits<BR/>course_type>, fillcolor="#dcfce7"];
    AcademicYear [label=<<B>Academic Year</B><BR/>field:academic_year_name<BR/>year_start_date, year_end_date>, fillcolor="#dcfce7"];
    AcademicTerm [label=<<B>Academic Term</B><BR/>field:term_name<BR/>academic_year, dates>, fillcolor="#dcfce7"];
    StudentGroup [label=<<B>Student Group</B><BR/>field:group_name<BR/>program, academic_year<BR/>course, max_strength>, fillcolor="#dcfce7"];
    CourseSchedule [label=<<B>Course Schedule</B><BR/>hash<BR/>course, student_group<BR/>instructor, room<BR/>day, from_time, to_time>, fillcolor="#fef3c7"];
    Instructor [label=<<B>Instructor</B><BR/>INST-.####<BR/>instructor_name<BR/>employee_id, department<BR/>email, status>, fillcolor="#fef3c7"];
    Room [label=<<B>Room</B><BR/>field:room_name<BR/>building, floor<BR/>capacity, room_type>, fillcolor="#fef3c7"];
    
    // Admissions
    AdmInquiry [label=<<B>Admission Inquiry</B><BR/>ADM-INQ-.YYYY.-.####<BR/>applicant_name, program<BR/>source, status>, fillcolor="#fce7f3"];
    StuApplicant [label=<<B>Student Applicant</B><BR/>STU-APP-.YYYY.-.####<BR/>applicant_name, program<BR/>workflow_state<BR/>created_student>, fillcolor="#fce7f3"];
    EntranceTest [label=<<B>Entrance Test</B><BR/>field:test_name<BR/>test_date, max_marks<BR/>passing_marks>, fillcolor="#fce7f3"];
    TestResult [label=<<B>Entrance Test Result</B><BR/>hash<BR/>entrance_test, applicant<BR/>marks_obtained, result>, fillcolor="#fce7f3"];
    
    // Examination
    GradingScale [label=<<B>Grading Scale</B><BR/>field:scale_name>, fillcolor="#ede9fe"];
    AssessmentGroup [label=<<B>Assessment Group</B><BR/>field:group_name<BR/>academic_term<BR/>results_published<BR/>weightage_percent>, fillcolor="#ede9fe"];
    AssessmentPlan [label=<<B>Assessment Plan</B><BR/>hash<BR/>assessment_group, course<BR/>student_group, max_marks<BR/>grading_scale>, fillcolor="#ede9fe"];
    AssessmentResult [label=<<B>Assessment Result</B><BR/>hash<BR/>assessment_plan, student<BR/>marks_obtained, grade<BR/>percentage, status>, fillcolor="#ede9fe"];
    
    // Fees
    FeeCategory [label=<<B>Fee Category</B><BR/>field:category_name>, fillcolor="#fee2e2"];
    FeeStructure [label=<<B>Fee Structure</B><BR/>field:structure_name<BR/>program, academic_year<BR/>total_amount>, fillcolor="#fee2e2"];
    FeeSchedule [label=<<B>Fee Schedule</B><BR/>hash<BR/>fee_structure, student_group<BR/>due_date>, fillcolor="#fee2e2"];
    Fees [label=<<B>Fees</B><BR/>FEE-.YYYY.-.####<BR/>student, fee_schedule<BR/>total_amount, discount<BR/>paid, outstanding, status>, fillcolor="#fee2e2"];
    FeePayment [label=<<B>Fee Payment</B><BR/>PMT-.YYYY.-.#####<BR/>fees, student<BR/>amount, mode, ref>, fillcolor="#fee2e2"];
    FeeDiscount [label=<<B>Fee Discount</B><BR/>hash<BR/>student, fees<BR/>type, value, status>, fillcolor="#fee2e2"];
    
    // Facilities
    BookCategory [label=<<B>Book Category</B><BR/>field:category_name>, fillcolor="#dcfce7"];
    LibraryItem [label=<<B>Library Item</B><BR/>LIB-BOOK-.#####<BR/>title, author, isbn<BR/>total_copies, available>, fillcolor="#dcfce7"];
    LibraryMembership [label=<<B>Library Membership</B><BR/>LIB-MEM-.YYYY.-.####<BR/>student, valid_upto<BR/>max_books, status>, fillcolor="#dcfce7"];
    LibraryTransaction [label=<<B>Library Transaction</B><BR/>hash<BR/>student, library_item<BR/>type, dates, fine<BR/>status>, fillcolor="#dcfce7"];
    
    Hostel [label=<<B>Hostel</B><BR/>field:hostel_name<BR/>hostel_type, warden<BR/>total_capacity>, fillcolor="#fef3c7"];
    HostelRoom [label=<<B>Hostel Room</B><BR/>field:room_number<BR/>hostel, room_type<BR/>capacity, occupied_count>, fillcolor="#fef3c7"];
    RoomAllocation [label=<<B>Room Allocation</B><BR/>hash<BR/>student, hostel_room<BR/>allocation_date, status>, fillcolor="#fef3c7"];
    
    Vehicle [label=<<B>Vehicle</B><BR/>field:vehicle_number<BR/>capacity, driver<BR/>status>, fillcolor="#fce7f3"];
    TransportRoute [label=<<B>Transport Route</B><BR/>field:route_name<BR/>vehicle, fee_amount>, fillcolor="#fce7f3"];
    TransportAlloc [label=<<B>Student Transport Alloc</B><BR/>hash<BR/>student, route<BR/>pickup_stop, status>, fillcolor="#fce7f3"];
    
    // Communication
    Notice [label=<<B>Notice</B><BR/>NOTICE-.YYYY.-.#####<BR/>title, body, audience<BR/>publish_date, status>, fillcolor="#ede9fe"];
    NoticeRecipient [label=<<B>Notice Recipient</B><BR/>hash<BR/>notice, student<BR/>recipient_type, read>, fillcolor="#ede9fe"];
    Feedback [label=<<B>Feedback</B><BR/>FDBK-.YYYY.-.#####<BR/>student, guardian<BR/>category, status<BR/>resolution_notes>, fillcolor="#ede9fe"];
    
    // Relationships (key ones)
    Student -> Guardian [label="guardian", style=bold];
    Student -> Program [label="program"];
    Guardian -> Student [label="linked students", style=dashed];
    Program -> Course [label="courses"];
    AcademicYear -> AcademicTerm [label="terms"];
    AcademicYear -> StudentGroup [label="groups"];
    Program -> StudentGroup [label="program"];
    Course -> StudentGroup [label="course"];
    CourseSchedule -> Course [label="course"];
    CourseSchedule -> StudentGroup [label="student_group"];
    CourseSchedule -> Instructor [label="instructor"];
    CourseSchedule -> Room [label="room"];
    StudentGroup -> Student [label="members", style=dashed];
    
    AdmInquiry -> StuApplicant [label="converts to"];
    StuApplicant -> Student [label="creates on approve", style=bold, color="#1e40af"];
    StuApplicant -> Guardian [label="creates on approve", style=bold, color="#1e40af"];
    StuApplicant -> EntranceTest [label="takes"];
    EntranceTest -> TestResult [label="results"];
    StuApplicant -> TestResult [label="applicant"];
    
    GradingScale -> AssessmentGroup [label="used by"];
    AssessmentGroup -> AssessmentPlan [label="plans"];
    Course -> AssessmentPlan [label="course"];
    StudentGroup -> AssessmentPlan [label="student_group"];
    AssessmentPlan -> AssessmentResult [label="results"];
    Student -> AssessmentResult [label="student"];
    
    FeeCategory -> FeeStructure [label="components"];
    FeeStructure -> FeeSchedule [label="schedules"];
    StudentGroup -> FeeSchedule [label="student_group"];
    FeeSchedule -> Fees [label="generates"];
    Student -> Fees [label="student"];
    Fees -> FeePayment [label="payments"];
    Fees -> FeeDiscount [label="discounts"];
    
    BookCategory -> LibraryItem [label="category"];
    Student -> LibraryMembership [label="membership"];
    Student -> LibraryTransaction [label="transactions"];
    LibraryItem -> LibraryTransaction [label="item"];
    
    Hostel -> HostelRoom [label="rooms"];
    HostelRoom -> RoomAllocation [label="allocations"];
    Student -> RoomAllocation [label="student"];
    
    Vehicle -> TransportRoute [label="vehicle"];
    TransportRoute -> TransportAlloc [label="allocations"];
    Student -> TransportAlloc [label="student"];
    
    Notice -> NoticeRecipient [label="recipients"];
    Student -> NoticeRecipient [label="student"];
    Student -> Feedback [label="student"];
    Guardian -> Feedback [label="guardian"];
}
'''
run_dot(er_diagram, "fig4_4_er_diagram")

# ============================================================
# Figure 4.5: DFD Level 0 (Context Diagram)
# ============================================================
dfd_l0 = '''
digraph DFD_L0 {
    rankdir=LR;
    node [fontname="Helvetica", fontsize=11, style=filled, shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=10];
    
    // External entities
    StudentExt [label="Student", shape=oval, fillcolor="#dbeafe"];
    GuardianExt [label="Guardian", shape=oval, fillcolor="#dbeafe"];
    InstructorExt [label="Instructor", shape=oval, fillcolor="#fef3c7"];
    AdmissionsExt [label="Admissions Officer", shape=oval, fillcolor="#fef3c7"];
    FeeMgrExt [label="Fee Manager", shape=oval, fillcolor="#fef3c7"];
    FacilityExt [label="Facility Manager", shape=oval, fillcolor="#fef3c7"];
    CommExt [label="Comm Officer", shape=oval, fillcolor="#fef3c7"];
    AcademicExt [label="Academic Head", shape=oval, fillcolor="#fef3c7"];
    SysMgrExt [label="System Manager", shape=oval, fillcolor="#fce7f3"];
    
    // Central process
    System [label="Institution ERP\n(Process 0)", shape=circle, fillcolor="#1e40af", fontcolor="white", fontsize=14, width=2.5, height=1.5];
    
    // Data stores
    DB [label="MariaDB\n(48 DocTypes)", shape=cylinder, fillcolor="#fef3c7", width=1.5];
    
    // Flows
    StudentExt -> System [label="Portal Access\n(Attendance, Results, Fees, Library, Notices, Feedback)"];
    GuardianExt -> System [label="Portal Access\n(Child Switcher, Multi-student view)"];
    InstructorExt -> System [label="Cockpit + Desk\n(Attendance, Marks, Schedule)"];
    AdmissionsExt -> System [label="Cockpit + Desk\n(Inquiry→Applicant→Approval)"];
    FeeMgrExt -> System [label="Cockpit + Desk\n(Fees, Payments, Discounts, Reports)"];
    FacilityExt -> System [label="Cockpit + Desk\n(Library, Hostel, Transport)"];
    CommExt -> System [label="Cockpit + Desk\n(Notices, Feedback, Dashboard)"];
    AcademicExt -> System [label="Cockpit + Desk\n(Academics Overview, Attendance, Exams)"];
    SysMgrExt -> System [label="Admin Cockpit + Desk\n(Institution-wide, All Modules)"];
    
    System -> DB [label="Read/Write\nAll DocTypes", dir=both];
}
'''
run_dot(dfd_l0, "fig4_5_dfd_l0")

# ============================================================
# Figure 4.6: DFD Level 1
# ============================================================
dfd_l1 = '''
digraph DFD_L1 {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, style=filled, shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=9];
    
    // External entities (simplified)
    Student [label="Student", shape=oval, fillcolor="#dbeafe"];
    Guardian [label="Guardian", shape=oval, fillcolor="#dbeafe"];
    Staff [label="Staff Roles", shape=oval, fillcolor="#fef3c7"];
    
    // Processes
    P1 [label="1. Admissions\nInquiry → Applicant → Test → Approval\nAuto Student/Guardian Creation", fillcolor="#fce7f3", width=2.2];
    P2 [label="2. Academics\nProgram/Course/Schedule/Group\nInstructor/Room Management", fillcolor="#dbeafe", width=2.2];
    P3 [label="3. Fees\nStructure → Schedule → Invoice\nPayment → Discount → Dues Report", fillcolor="#fee2e2", width=2.2];
    P4 [label="4. Facilities\nLibrary (Issue/Return/Fine)\nHostel (Room/Allocation)\nTransport (Route/Allocation)", fillcolor="#dcfce7", width=2.2];
    P5 [label="5. Communication\nNotice (Targeted Dispatch)\nFeedback (Track/Resolve)\nDashboard (Cards/Charts)", fillcolor="#ede9fe", width=2.2];
    P6 [label="6. Examination\nGrading Scale → Group → Plan\nBulk Marks → Auto Grade\nResults Published Gate", fillcolor="#fef3c7", width=2.2];
    P7 [label="7. Attendance\nStudent (per Course Schedule)\nStaff (per Instructor)\nBulk Mark APIs", fillcolor="#fef3c7", width=2.2];
    P8 [label="8. Portal Access\nStudent/Guardian SPA\nRow-level Security\nResults Gating", fillcolor="#dbeafe", width=2.2];
    
    // Data stores
    DS1 [label="D1: Student &\nGuardian Master", shape=cylinder, fillcolor="#fef3c7"];
    DS2 [label="D2: Academic\nStructure", shape=cylinder, fillcolor="#fef3c7"];
    DS3 [label="D3: Fees &\nPayments", shape=cylinder, fillcolor="#fef3c7"];
    DS4 [label="D4: Assessment\n& Results", shape=cylinder, fillcolor="#fef3c7"];
    DS5 [label="D5: Attendance\nRecords", shape=cylinder, fillcolor="#fef3c7"];
    DS6 [label="D6: Facilities\n(Lib/Hostel/Trans)", shape=cylinder, fillcolor="#fef3c7"];
    DS7 [label="D7: Communication\n(Notices/Feedback)", shape=cylinder, fillcolor="#fef3c7"];
    DS8 [label="D8: Admissions\nPipeline", shape=cylinder, fillcolor="#fef3c7"];
    
    // Flows
    Student -> P1 [label="Inquiry/Application"];
    Staff -> P1 [label="Review/Approve"];
    P1 -> DS8 [label="Admission Records", dir=both];
    P1 -> DS1 [label="Creates Student+Guardian", dir=both];
    
    Staff -> P2 [label="Manage Programs/Courses"];
    P2 -> DS2 [label="Academic Data", dir=both];
    
    Staff -> P3 [label="Manage Fees"];
    Student -> P3 [label="View/Pay Fees"];
    P3 -> DS3 [label="Fee Records", dir=both];
    P3 -> DS1 [label="Student Link", dir=both];
    
    Staff -> P4 [label="Manage Facilities"];
    Student -> P4 [label="Library/Hostel/Transport"];
    P4 -> DS6 [label="Facility Records", dir=both];
    P4 -> DS1 [label="Student Link", dir=both];
    
    Staff -> P5 [label="Dispatch Notices"];
    Student -> P5 [label="View Notices/Feedback"];
    Guardian -> P5 [label="View Notices/Feedback"];
    P5 -> DS7 [label="Comm Records", dir=both];
    P5 -> DS1 [label="Recipient Link", dir=both];
    
    Staff -> P6 [label="Create Assessments/Enter Marks"];
    Student -> P6 [label="View Results (if published)"];
    P6 -> DS4 [label="Assessment Data", dir=both];
    P6 -> DS2 [label="Course/Group Link", dir=both];
    P6 -> DS1 [label="Student Link", dir=both];
    
    Staff -> P7 [label="Mark Attendance"];
    Student -> P7 [label="View Attendance"];
    P7 -> DS5 [label="Attendance Records", dir=both];
    P7 -> DS2 [label="Schedule/Group Link", dir=both];
    P7 -> DS1 [label="Student/Instructor Link", dir=both];
    
    Student -> P8 [label="Portal Login"];
    Guardian -> P8 [label="Portal Login"];
    P8 -> DS1 [label="Own/Linked Records", dir=both];
    P8 -> DS3 [label="Own Fees", dir=both];
    P8 -> DS4 [label="Own Results (published)", dir=both];
    P8 -> DS5 [label="Own Attendance", dir=both];
    P8 -> DS6 [label="Own Facility Records", dir=both];
    P8 -> DS7 [label="Own Notices/Feedback", dir=both];
}
'''
run_dot(dfd_l1, "fig4_6_dfd_l1")

# ============================================================
# Figure 4.7: Use Case Diagram
# ============================================================
use_case = '''
digraph UseCase {
    rankdir=LR;
    node [fontname="Helvetica", fontsize=10];
    edge [fontname="Helvetica", fontsize=9];
    
    // Actors
    Student [label="Student", shape=actor, fillcolor="#dbeafe", style=filled];
    Guardian [label="Guardian", shape=actor, fillcolor="#dbeafe", style=filled];
    Instructor [label="Instructor", shape=actor, fillcolor="#fef3c7", style=filled];
    Admissions [label="Admissions Officer", shape=actor, fillcolor="#fef3c7", style=filled];
    FeeMgr [label="Fee Manager", shape=actor, fillcolor="#fef3c7", style=filled];
    Facility [label="Facility Manager", shape=actor, fillcolor="#fef3c7", style=filled];
    Comm [label="Comm Officer", shape=actor, fillcolor="#fef3c7", style=filled];
    Academic [label="Academic Head", shape=actor, fillcolor="#fef3c7", style=filled];
    SysMgr [label="System Manager", shape=actor, fillcolor="#fce7f3", style=filled];
    
    // Use cases - Portal
    subgraph cluster_portal {
        label="Student/Guardian Portal";
        style=dashed; color="#64748b";
        UC1 [label="View Dashboard", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC2 [label="View Attendance", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC3 [label="View Results", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC4 [label="View Fees & Payments", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC5 [label="View Library Transactions", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC6 [label="View Notices", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC7 [label="Submit Feedback", shape=ellipse, fillcolor="#dbeafe", style=filled];
        UC8 [label="Switch Child (Guardian)", shape=ellipse, fillcolor="#dbeafe", style=filled];
    }
    
    // Use cases - Staff Cockpit
    subgraph cluster_cockpit {
        label="Staff Cockpits";
        style=dashed; color="#64748b";
        UC9 [label="View Role Dashboard", shape=ellipse, fillcolor="#fef3c7", style=filled];
        UC10 [label="Quick Actions", shape=ellipse, fillcolor="#fef3c7", style=filled];
    }
    
    // Use cases - Desk (Full CRUD)
    subgraph cluster_desk {
        label="Frappe Desk (Full CRUD)";
        style=dashed; color="#64748b";
        UC11 [label="Manage Admissions Pipeline", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC12 [label="Manage Academics", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC13 [label="Mark Attendance", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC14 [label="Enter Assessment Marks", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC15 [label="Manage Fees & Payments", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC16 [label="Manage Library/Hostel/Transport", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC17 [label="Dispatch Notices", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC18 [label="Manage Feedback", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC19 [label="View Reports & Dashboard", shape=ellipse, fillcolor="#fce7f3", style=filled];
        UC20 [label="Administer System", shape=ellipse, fillcolor="#fce7f3", style=filled];
    }
    
    // Relationships
    Student -> {UC1 UC2 UC3 UC4 UC5 UC6 UC7}
    Guardian -> {UC1 UC2 UC3 UC4 UC5 UC6 UC7 UC8}
    Instructor -> {UC9 UC10 UC13 UC14}
    Admissions -> {UC9 UC10 UC11}
    FeeMgr -> {UC9 UC10 UC15}
    Facility -> {UC9 UC10 UC16}
    Comm -> {UC9 UC10 UC17 UC18 UC19}
    Academic -> {UC9 UC10 UC12 UC13 UC14 UC19}
    SysMgr -> {UC9 UC10 UC11 UC12 UC13 UC14 UC15 UC16 UC17 UC18 UC19 UC20}
    
    // Include/extend
    UC3 -> UC2 [label="<<extend>>\n(results gating)", style=dashed, dir=back];
    UC10 -> UC11 [label="<<include>>\n(Open Full Desk)", style=dashed];
    UC10 -> UC12 [label="<<include>>"];
    UC10 -> UC13 [label="<<include>>"];
    UC10 -> UC14 [label="<<include>>"];
    UC10 -> UC15 [label="<<include>>"];
    UC10 -> UC16 [label="<<include>>"];
    UC10 -> UC17 [label="<<include>>"];
    UC10 -> UC18 [label="<<include>>"];
    UC10 -> UC19 [label="<<include>>"];
    UC10 -> UC20 [label="<<include>>"];
}
'''
run_dot(use_case, "fig4_7_use_case")

# ============================================================
# Figure 4.8: Sequence — Admission Approval
# ============================================================
seq_admission = '''
digraph SeqAdmission {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, shape=box, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    // Lifelines
    AdmOfficer [label="Admissions\nOfficer", fillcolor="#fef3c7"];
    System [label="Institution ERP", fillcolor="#dbeafe"];
    DB [label="MariaDB", shape=cylinder, fillcolor="#fef3c7"];
    
    // Sequence
    AdmOfficer -> System [label="1. Review Applicant\n(Workflow: Under Review)"];
    System -> DB [label="2. READ Student Applicant", dir=both];
    AdmOfficer -> System [label="3. Approve Applicant\n(Workflow: Approved)"];
    System -> System [label="4. on_update Trigger\n(Student Applicant)"];
    System -> DB [label="5. CREATE Guardian\nDocType", dir=both];
    System -> DB [label="6. CREATE Student\nDocType (STU-.YYYY.-.#####)", dir=both];
    System -> DB [label="7. LINK Guardian→Student\n(guardian field)", dir=both];
    System -> DB [label="8. SET created_student\n= Student Name", dir=both];
    System -> AdmOfficer [label="9. Return Success\n(Student + Guardian created)"];
    
    // Notes
    Note1 [label="Auto-creation happens\nin on_update hook\nwhen workflow_state=\n'Approved'", shape=note, fillcolor="#fef3c7"];
    System -> Note1 [style=dashed];
}
'''
run_dot(seq_admission, "fig4_8_seq_admission")

# ============================================================
# Figure 4.9: Sequence — Fee Payment
# ============================================================
seq_fee = '''
digraph SeqFee {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, shape=box, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    FeeMgr [label="Fee Manager", fillcolor="#fef3c7"];
    System [label="Institution ERP", fillcolor="#dbeafe"];
    DB [label="MariaDB", shape=cylinder, fillcolor="#fef3c7"];
    
    FeeMgr -> System [label="1. Create Fee Payment\n(amount, mode, ref)"];
    System -> DB [label="2. VALIDATE\npayment ≤ outstanding", dir=both];
    System -> DB [label="3. INSERT Fee Payment\n(docstatus=1 on submit)", dir=both];
    System -> System [label="4. on_submit Hook\n(recompute_paid_and_status)"];
    System -> DB [label="5. READ all Fee Payments\nfor this Fees", dir=both];
    System -> System [label="6. CALCULATE\npaid = Σ payments\ndiscount = discount_amount\noutstanding = total - paid - discount"];
    System -> DB [label="7. UPDATE Fees\npaid_amount, outstanding_amount\nstatus (Unpaid/Partial/Paid/Overdue)", dir=both];
    System -> FeeMgr [label="8. Return Updated\nFees + Payment"];
}
'''
run_dot(seq_fee, "fig4_9_seq_fee")

# ============================================================
# Figure 4.10: Sequence — Assessment Result
# ============================================================
seq_assessment = '''
digraph SeqAssessment {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, shape=box, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    Instructor [label="Instructor", fillcolor="#fef3c7"];
    System [label="Institution ERP", fillcolor="#dbeafe"];
    DB [label="MariaDB", shape=cylinder, fillcolor="#fef3c7"];
    StudentPortal [label="Student Portal", fillcolor="#dbeafe"];
    
    Instructor -> System [label="1. mark_bulk_assessment_results\n(assessment_plan, results_data)"];
    System -> DB [label="2. VALIDATE\nmarks ≤ max_marks", dir=both];
    System -> DB [label="3. READ Grading Scale\nintervals", dir=both];
    System -> System [label="4. FOR each result:\n   percentage = marks/max*100\n   grade = matching interval\n   status = Pass/Fail"];
    System -> DB [label="5. UPSERT Assessment Result\n(prevents duplicate)", dir=both];
    System -> Instructor [label="6. Return Created\nResults"];
    
    // Results published gate
    Instructor -> System [label="7. Set Assessment Group\nresults_published = 1"];
    System -> DB [label="8. UPDATE Assessment Group", dir=both];
    StudentPortal -> System [label="9. portal_get_results\n(student, assessment_plan)"];
    System -> System [label="10. CHECK\nresults_published = 1?"];
    System -> DB [label="11. IF yes: READ Results\nELSE: Return 'Not Published'", dir=both];
    System -> StudentPortal [label="12. Return Results\nOR 'Not Published' banner"];
}
'''
run_dot(seq_assessment, "fig4_10_seq_assessment")

# ============================================================
# Figure 4.11: Sequence — Library Fine
# ============================================================
seq_library = '''
digraph SeqLibrary {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, shape=box, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    FacilityMgr [label="Facility Manager", fillcolor="#fef3c7"];
    System [label="Institution ERP", fillcolor="#dbeafe"];
    DB [label="MariaDB", shape=cylinder, fillcolor="#fef3c7"];
    
    FacilityMgr -> System [label="1. Submit Library Transaction\n(type=Return, return_date)"];
    System -> DB [label="2. VALIDATE\nopen Issue exists", dir=both];
    System -> System [label="3. CALCULATE\nfine = days_overdue × ₹5"];
    System -> DB [label="4. UPDATE Library Transaction\nfine_amount, status=Returned\navailable_copies++", dir=both];
    
    // Fine > 0 creates Fee
    System -> System [label="5. IF fine > 0:\n   CREATE Fees Record\n   (category=Library Fine)"];
    System -> DB [label="6. INSERT Fees\n(outstanding = fine)", dir=both];
    System -> FacilityMgr [label="7. Return Transaction\n+ Fine Fee Created"];
    
    Note1 [label="LIMITATION: Fine\ncreates Fee immediately\nwithout Fee Manager\napproval workflow", shape=note, fillcolor="#fee2e2"];
    System -> Note1 [style=dashed];
}
'''
run_dot(seq_library, "fig4_11_seq_library")

# ============================================================
# Figure 4.12: Activity — Student Portal
# ============================================================
act_student = '''
digraph ActStudent {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    Start [label="Start", shape=circle, fillcolor="#1e40af", fontcolor="white", width=0.5];
    Login [label="Login at\n/institution-portal", fillcolor="#dbeafe"];
    Auth [label="Authenticate\nJWT Token", fillcolor="#dbeafe"];
    RoleCheck [label="Role = Student?", shape=diamond, fillcolor="#fef3c7"];
    Dashboard [label="Student Dashboard\n(StatCards, Charts,\nRecent Notices/Fees)", fillcolor="#dbeafe"];
    NavMenu [label="Sidebar Navigation", fillcolor="#dbeafe"];
    
    // Pages
    Attendance [label="Attendance Page\n50 records, status badges\nSummary: 84%", fillcolor="#dbeafe"];
    Results [label="Results Page\n6 Assessment Results\nBlue banner if unpublished", fillcolor="#dbeafe"];
    Fees [label="Fees Page\n1 Fee (₹48,000, Paid)\nPayment History", fillcolor="#dbeafe"];
    Library [label="Library Page\n3 Active Issues\n5 Transaction History", fillcolor="#dbeafe"];
    Notices [label="Notices Page\n6 Published Notices\nExpandable", fillcolor="#dbeafe"];
    Feedback [label="Feedback Page\nSubmit Form + History", fillcolor="#dbeafe"];
    Profile [label="Profile Page\nView/Edit Details", fillcolor="#dbeafe"];
    Logout [label="Logout", fillcolor="#dbeafe"];
    End [label="End", shape=circle, fillcolor="#1e40af", fontcolor="white", width=0.5];
    
    Start -> Login -> Auth -> RoleCheck;
    RoleCheck -> Dashboard [label="Yes"];
    RoleCheck -> End [label="No (Guardian/Staff)"];
    Dashboard -> NavMenu;
    NavMenu -> {Attendance Results Fees Library Notices Feedback Profile};
    {Attendance Results Fees Library Notices Feedback Profile} -> NavMenu;
    NavMenu -> Logout -> End;
}
'''
run_dot(act_student, "fig4_12_act_student")

# ============================================================
# Figure 4.13: Activity — Staff Hybrid Flow
# ============================================================
act_staff = '''
digraph ActStaff {
    rankdir=TB;
    node [fontname="Helvetica", fontsize=10, style=filled];
    edge [fontname="Helvetica", fontsize=9];
    
    Start [label="Start", shape=circle, fillcolor="#1e40af", fontcolor="white", width=0.5];
    Login [label="Staff Login\n(Frappe Desk)", fillcolor="#fef3c7"];
    RoleDetect [label="Detect Role\n(Instructor/FeeMgr/etc.)", fillcolor="#fef3c7"];
    Redirect [label="Redirect to\n/institution-portal/<role>", fillcolor="#fef3c7"];
    Cockpit [label="Role-Specific Cockpit\n(Stats, Quick Actions,\nPending Items)", fillcolor="#fef3c7"];
    QuickAction [label="Click Quick Action\n(e.g., Mark Attendance)", fillcolor="#fef3c7"];
    OpenDesk [label="Opens Desk in\nNew Tab\n(Full CRUD)", fillcolor="#fce7f3"];
    DeskWork [label="Perform Full CRUD\nCreate/Edit/Delete/Submit\nRun Reports", fillcolor="#fce7f3"];
    ReturnCockpit [label="Return to Cockpit\n(Refresh for Updated Stats)", fillcolor="#fef3c7"];
    Logout [label="Logout", fillcolor="#fef3c7"];
    End [label="End", shape=circle, fillcolor="#1e40af", fontcolor="white", width=0.5];
    
    Start -> Login -> RoleDetect -> Redirect -> Cockpit;
    Cockpit -> QuickAction -> OpenDesk -> DeskWork;
    DeskWork -> ReturnCockpit -> Cockpit;
    Cockpit -> Logout -> End;
}
'''
run_dot(act_staff, "fig4_13_act_staff")

# ============================================================
# Figure 5.16: Workflow — Student Applicant
# ============================================================
wf_applicant = '''
digraph WFApplicant {
    rankdir=LR;
    node [fontname="Helvetica", fontsize=10, style=filled, shape=box, rounded=true];
    edge [fontname="Helvetica", fontsize=9];
    
    Draft [label="Draft", fillcolor="#fef3c7"];
    Applied [label="Applied", fillcolor="#dbeafe"];
    UnderReview [label="Under Review", fillcolor="#fef3c7"];
    Approved [label="Approved", fillcolor="#dcfce7", style="filled,bold"];
    Rejected [label="Rejected", fillcolor="#fee2e2"];
    
    Draft -> Applied [label="Submit Application"];
    Applied -> UnderReview [label="Officer Reviews"];
    UnderReview -> Approved [label="Approve\n→ Creates Student+Guardian"];
    UnderReview -> Rejected [label="Reject"];
    Approved -> Rejected [label="Reopen (if needed)"];
    Rejected -> Applied [label="Re-apply"];
    
    // Auto-creation note
    Note [label="on_update hook:\nworkflow_state='Approved'\n→ create Guardian\n→ create Student\n→ link both", shape=note, fillcolor="#fef3c7"];
    Approved -> Note [style=dashed];
}
'''
run_dot(wf_applicant, "fig5_16_wf_applicant")

print("\n=== Diagram generation complete ===")
print(f"Images saved to: {IMAGES_DIR}")
print("Check for any 'dot not found' errors above.")