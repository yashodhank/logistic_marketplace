# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt"


from __future__ import unicode_literals
import frappe
from frappe.utils.nestedset import get_root_of

def boot_session(bootinfo):
	has_role = frappe.db.sql("""select allow,for_value from `tabUser Permission` where user="{}" """.format(frappe.session['user']),as_dict=1)
	for row in has_role:
		if row.['allow'] == "Principle":
			frappe.session['principle']=row['for_value']
			bootinfo.sysdefaults.principle=row['for_value']
		elif row.['allow'] == "Vendor":
			frappe.session['vendor']=row['for_value']
			bootinfo.sysdefaults.vendor=row['for_value']
		elif row.['allow'] == "Driver":
			frappe.session['driver']=row['for_value']
			bootinfo.sysdefaults.driver=row['for_value']