from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_job_order_data(principle):
	if principle:
		result = frappe.db.sql("""select job_order , waktu,status,lo,lat,principle ,vendor from `tabJob Order Update` where principle="{}" and docstatus=1 order by waktu desc """.format(principle),as_dict=1)
	else:
		result = frappe.db.sql("""select job_order , waktu,status,lo,lat,principle ,vendor from `tabJob Order Update` where principle="{}" and docstatus=1 order by waktu desc """.format(principle),as_dict=1)
