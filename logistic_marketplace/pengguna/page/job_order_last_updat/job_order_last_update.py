from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_job_order_data(filters):
	where = ""
	if filters.get("principle"):
		where = """ and p.principle ="{}" """.format(principle)
	if filters.get("vendor"):
		where = """{} and p.vendor="{}" """.format(vendor)
	result = frappe.db.sql("""select d.job_order , d.waktu,d.status,d.lo,d.lat,p.principle ,p.vendor ,d.driver
			from `tabJob Order Update` d 
			join `tabJob Order` p on d.job_order = p.name 
			 where p.status = "Dalam Proses" {} and d.docstatus=1 order by d.waktu desc """.format(where),as_dict=1)
	last=[]
	jo=""
	for row in result:
		if jo != row.job_order:
			jo = row.job_order
			last.append(row)
	return last
	