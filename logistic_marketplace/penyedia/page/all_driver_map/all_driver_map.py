from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_position(driver,vendor):
	where = ""
	if driver!="All":
		where = """{} and d.name="{}" """.format(where,driver)
	result = frappe.db.sql("""select d.name as "driver",d.nama,d.phone,DATE_FORMAT(d.last_update,"%d-%m-%Y %H:%i") as waktu,d.lo,d.lat,d.status
		from `tabDriver` d 
		where vendor="{}" {} order by d.last_update desc """.format(vendor,where),as_dict=1)
	return result
	