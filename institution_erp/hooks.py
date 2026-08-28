app_name = "institution_erp"
app_title = "Institution Erp"
app_publisher = "SriRagul"
app_description = "Institution Student ERP Extention"
app_email = "sriragul.aa@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "institution_erp",
# 		"logo": "/assets/institution_erp/logo.png",
# 		"title": "Institution Erp",
# 		"route": "/institution_erp",
# 		"has_permission": "institution_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = ["/assets/institution_erp/css/inter-font.css", "/assets/institution_erp/css/desk-theme.css"]

# include js, css files in header of web template
# web_include_css = "/assets/institution_erp/css/institution_erp.css"
# web_include_js = "/assets/institution_erp/js/institution_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "institution_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Portal
# ------
website_route_rules = [
	{"from_route": "/institution-portal/<path:app_path>", "to_route": "institution-portal"},
]

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "institution_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
	"Student": "institution-portal",
	"Guardian": "institution-portal",
	"Instructor": "institution-portal",
	"Academic Head": "institution-portal",
	"Fee Manager": "institution-portal",
	"Facility Manager": "institution-portal",
	"Communication Officer": "institution-portal",
	"System Manager": "institution-portal",
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "institution_erp.utils.jinja_methods",
# 	"filters": "institution_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "institution_erp.install.before_install"
# after_install = "institution_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "institution_erp.uninstall.before_uninstall"
# after_uninstall = "institution_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "institution_erp.utils.before_app_install"
# after_app_install = "institution_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "institution_erp.utils.before_app_uninstall"
# after_app_uninstall = "institution_erp.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "institution_erp.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "institution_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Student": "institution_erp.api.get_permission_query_conditions_student",
	"Student Attendance": "institution_erp.api.get_permission_query_conditions_student_attendance",
	"Staff Attendance": "institution_erp.api.get_permission_query_conditions_staff_attendance",
	"Assessment Result": "institution_erp.api.get_permission_query_conditions_assessment_result",
	"Assessment Plan": "institution_erp.api.get_permission_query_conditions_assessment_plan",
	"Fees": "institution_erp.api.get_permission_query_conditions_fees",
	"Fee Payment": "institution_erp.api.get_permission_query_conditions_fee_payment",
	"Library Item": "institution_erp.api.get_permission_query_conditions_library_item",
	"Library Membership": "institution_erp.api.get_permission_query_conditions_library_membership",
	"Library Transaction": "institution_erp.api.get_permission_query_conditions_library_transaction",
	"Hostel": "institution_erp.api.get_permission_query_conditions_hostel",
	"Hostel Room": "institution_erp.api.get_permission_query_conditions_hostel",
	"Hostel Room Allocation": "institution_erp.api.get_permission_query_conditions_hostel",
	"Vehicle": "institution_erp.api.get_permission_query_conditions_transport",
	"Transport Route": "institution_erp.api.get_permission_query_conditions_transport",
	"Student Transport Allocation": "institution_erp.api.get_permission_query_conditions_transport",
	"Notice": "institution_erp.api.get_permission_query_conditions_notice",
	"Notice Recipient": "institution_erp.api.get_permission_query_conditions_notice_recipient",
	"Communication Log": "institution_erp.api.get_permission_query_conditions_communication_log",
	"Feedback": "institution_erp.api.get_permission_query_conditions_feedback",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"institution_erp.tasks.all"
# 	],
# 	"daily": [
# 		"institution_erp.tasks.daily"
# 	],
# 	"hourly": [
# 		"institution_erp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"institution_erp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"institution_erp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "institution_erp.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "institution_erp.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "institution_erp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "institution_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["institution_erp.utils.before_request"]
# after_request = ["institution_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["institution_erp.utils.before_job"]
# after_job = ["institution_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"institution_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

