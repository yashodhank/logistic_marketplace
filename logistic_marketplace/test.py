from __future__ import unicode_literals
import frappe
import json
@frappe.whitelist(allow_guest=True)
def get_job_order(principle=''):
	filters = frappe.local.form_dict
	data = frappe.get_list("Job Order",filters={
		'principle':principle
		},fields=["*"])
	for row in data:
		row['routes'] = frappe.db.sql("select * from `tabJob Order Route` where parent='{}'".format(row.name),as_dict=1)
	return data
