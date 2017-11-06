from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_position(driver):
	where = ""
	if driver!="All":
		where = """{} and p.driver="{}" """.format(where,driver)
	result = frappe.db.sql("""select d.name as "driver",d.nama,d.phone,d.last_update,d.lo,d.lat,d.status
		from `tabDriver` d 
		order by d.last_update desc """.format(where),as_dict=1)
	return result
	