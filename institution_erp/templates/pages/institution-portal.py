"""Portal page - serves the Vue SPA at /institution-portal"""
import frappe

no_cache = True

def get_context(context):
    context.title = "Bannari Amman Institute of Technology - Student Portal"
    context.no_breadcrumbs = True
    context.no_header = True
