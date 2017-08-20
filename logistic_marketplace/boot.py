# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt"


from __future__ import unicode_literals
import frappe
from frappe.utils.nestedset import get_root_of

def boot_session(bootinfo):
	principle = frappe.db.sql("""select name from `tabPrinciple` where user="{}" """.format(frappe.session['user']),as_dict=1)
	for row in principle:
		frappe.session['principle']=row['name']
		bootinfo.sysdefaults.principle=row['name']
	vendor = frappe.db.sql("""select name from `tabVendor` where user="{}" """.format(frappe.session['user']),as_dict=1)
	for row in vendor:
		frappe.session['vendor']=row['name']
		bootinfo.sysdefaults.vendor=row['name']