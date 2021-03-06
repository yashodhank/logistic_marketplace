from __future__ import unicode_literals
import frappe
import json

def patch():
	data = frappe.db.sql("select * from `tabJob Order` where pick_location is not null",as_dict=1)
	for row in data:
		frappe.db.sql("""insert into `tabJob Order Route` 
					(location 		,warehouse_name				,distributor_code 				,city 					, address			,contact 					,nama 					, phone		,type		,item_info ,remark ,order_index,parent,name,owner,creation,modified,modified_by,docstatus,parentfield,parenttype,idx) values
					("{}"			,"{}"						,"{}"							,"{}" 					,"{}"				,"{}"						,"{}" 					, "{}"		,"Pick Up"	,"{}"	,"",1,"{}","{}","{}","{}","{}","{}","{}","routes","Job Order",0)
		""".format(row.pick_location,row.nama_gudang_pengambilan,row.kode_distributor_pengambilan,row.kota_pengambilan,row.alamat_pengambilan,row.principle_contact_person,row.nama_principle_cp,row.telp_principle_cp,row.goods_information,row.name,row.name,row.owner,row.creation,row.modified,row.modified_by,row.docstatus),as_list=1)
		frappe.db.sql("""insert into `tabJob Order Route` 
					(location 		,warehouse_name				,distributor_code 				,city 					, address			,contact 					,nama 					, phone		,type		,item_info ,remark ,order_index,parent,name,owner,creation,modified,modified_by,docstatus,parentfield,parenttype,idx) values
					("{}"			,"{}"						,"{}"							,"{}" 					,"{}"				,"{}"						,"{}" 					, "{}"		,"Drop"	,"{}"	,"",2,"{}","{}","{}","{}","{}","{}","{}","routes","Job Order",0)
		""".format(row.delivery_location,row.nama_gudang_pengiriman,row.kode_distributor_pengiriman,row.kota_pengiriman,row.alamat_pengiriman,row.principle_contact_person,row.nama_principle_cp,row.telp_principle_cp,row.goods_information,row.name,row.name+"--",row.owner,row.creation,row.modified,row.modified_by,row.docstatus),as_list=1)

def delete():
	principle="PT Tiga Berlian Electric"
	frappe.db.sql("""delete from `tabJob Order Route` where parent IN (select name from `tabJob Order` where principle="{}") """.format(principle),as_list=1)
	frappe.db.sql("""delete from `tabJob Order` where principle="{}" """.format(principle),as_list=1)
 	frappe.db.sql("""delete from `tabJob Order Update` where parent IN (select name from `tabJob Order Update Image` where principle="{}") """.format(principle),as_list=1)
	frappe.db.sql("""delete from `tabJob Order Update` where principle="{}" """.format(principle),as_list=1)

def delete_principle():
	principle="PT Nestle Indonesia"
	jou = frappe.db.sql("""select name,docstatus from `tabJob Order Update` where principle="{}" """.format(principle),as_list=1)
	for row in jou:
		doc = frappe.get_doc("Job Order Update",row[0])
		if row[1]==1:
			doc.cancel()
			doc.delete()
		else:
			doc.delete()
		frappe.db.commit()
	list = frappe.db.sql("""select name,docstatus from `tabJob Order` where principle="{}" """.format(principle),as_list=1)
	for row in list:
		doc = frappe.get_doc("Job Order",row[0])
		if row[1]==1:
			doc.cancel()
			doc.delete()
		else:
			doc.delete()
		frappe.db.commit()
