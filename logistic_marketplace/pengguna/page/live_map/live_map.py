from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_position(principle,vendor,driver):
	where = ""
	if principle!="All":
		where = """ and p.principle ="{}" """.format(principle)
	if vendor!="All":
		where = """{} and p.vendor="{}" """.format(where,vendor)
	if driver!="All":
		where = """{} and p.driver="{}" """.format(where,driver)
	result = frappe.db.sql("""select p.name as "job_order" , d.last_update,d.lo,d.lat,p.principle ,p.vendor ,p.driver 
		from `tabJob Order` p 
		join `tabDriver` d on d.name = p.driver 
		where p.status = "Dalam Proses" {}  order by d.last_update desc """.format(where),as_dict=1)
	last=[]
	jo=""
	for row in result:
		if jo != row.job_order:
			jo = row.job_order
			last.append(row)
	if last==[]:
		return "No Data"
	return last
	