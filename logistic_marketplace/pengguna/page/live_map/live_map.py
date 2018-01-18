from __future__ import unicode_literals
import frappe

from frappe import _

@frappe.whitelist()
def get_position(principle,vendor,driver,driver_status):
	where = ""
	if principle!="All":
		where = """ and p.principle ="{}" """.format(principle)
	if vendor!="All":
		where = """{} and d.vendor="{}" """.format(where,vendor)
	if driver!="All":
		where = """{} and d.name="{}" """.format(where,driver)
	result=[]
	if driver_status=="Idle":
		if principle!="All":
			return "No Data"
		result = frappe.db.sql("""select "Idle" as "job_order", DATE_FORMAT(d.last_update,"%d-%m-%Y %H:%i") as waktu,d.lo,d.lat ,"None" as "principle",d.vendor ,d.name as "driver" 
			from `tabDriver` d
			where d.status = "Tersedia" {}  order by d.last_update desc """.format(where),as_dict=1)
		if result==[]:
			return "No Data"
		return result
	elif driver_status=="On Duty":
		result = frappe.db.sql("""select p.name as "job_order" , DATE_FORMAT(d.last_update,"%d-%m-%Y %H:%i") as waktu,d.lo,d.lat,p.principle ,p.vendor ,p.driver 
			from `tabJob Order` p 
			join `tabDriver` d on d.name = p.driver 
			where p.status = "Dalam Proses" and d.status="Tidak Tersedia" {}  order by d.name,d.last_update desc """.format(where),as_dict=1)
		last=[]
		jo=""
		for row in result:
			if jo != row.driver:
				jo = row.driver
				last.append(row)
		if last==[]:
			return "No Data"
		return last
	else:
		result = frappe.db.sql("""select ifnull(p.name,"Idle") as "job_order" , DATE_FORMAT(d.last_update,"%d-%m-%Y %H:%i") as waktu,d.lo,d.lat,ifnull(p.principle,"None") as "principle" ,d.vendor ,d.name as "driver"
			from `tabDriver` d 
			left join `tabJob Order` p on d.name = p.driver and p.status = "Dalam Proses"
			where 1=1 {}  order by d.name, d.last_update desc,p.modified desc """.format(where),as_dict=1)
		last=[]
		jo=""
		for row in result:
			if jo != row.driver:
				jo = row.driver
				last.append(row)
		if last==[]:
			return "No Data"
		return last
	