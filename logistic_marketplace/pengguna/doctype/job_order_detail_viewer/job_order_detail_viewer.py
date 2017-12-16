# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobOrderDetailViewer(Document):
	pass
	def view_job_order(self):
		job_order =frappe.get_doc("Job Order", self.job_order)
		self.jo_status = job_order.status
		self.principle =job_order.principle
		self.reference =job_order.reference
		self.principle_contact_person=job_order.principle_contact_person
		self.nama_principle_cp=job_order.nama_principle_cp
		self.telp_principle_cp=job_order.telp_principle_cp
		self.vendor=job_order.vendor
		self.vendor_contact_person=job_order.vendor_contact_person
		self.nama_vendor_cp=job_order.nama_vendor_cp
		self.telp_vendor_cp=job_order.telp_vendor_cp
		self.pick_location=job_order.pick_location
		self.kota_pengambilan=job_order.kota_pengambilan
		self.alamat_pengambilan=job_order.alamat_pengambilan
		self.nama_gudang_pengambilan=job_order.nama_gudang_pengambilan
		self.kode_distributor_pengambilan=job_order.kode_distributor_pengambilan
		self.delivery_location=job_order.delivery_location
		self.kota_pengiriman=job_order.kota_pengiriman
		self.alamat_pengiriman=job_order.alamat_pengiriman
		self.nama_gudang_pengiriman=job_order.nama_gudang_pengiriman
		self.kode_distributor_pengiriman=job_order.kode_distributor_pengiriman
		self.pick_date=job_order.pick_date
		self.expected_delivery=job_order.expected_delivery
		self.suggest_truck_type=job_order.suggest_truck_type
		self.strict=job_order.strict
		self.estimate_volume=job_order.estimate_volume
		self.goods_information=job_order.goods_information
		self.notes=job_order.notes
		self.accept_date=job_order.accept_date
		self.driver=job_order.driver
		self.driver_nama=job_order.driver_nama
		self.driver_phone=job_order.driver_phone
		self.truck=job_order.truck
		self.truck_volume=job_order.truck_volume
		self.truck_type=job_order.truck_type
		self.truck_lambung=job_order.truck_lambung

		job_order_update = frappe.db.sql("""select name,waktu,note,status,lo,lat,vendor,principle from `tabJob Order Update` where job_order="{}" order by waktu asc """.format(self.job_order),as_dict=1)
		upd = ""
		for row in job_order_update:
			image_list = frappe.db.sql("""select file_url from `tabFile` where attached_to_doctype="Job Order Update" and attached_to_name="{}" """.format(row['name']),as_dict=1)
			img = "<div>"
			for gg in image_list:
				img="""{}<img src="{}" style="padding-right:20px;"/> """.format(img,gg['file_url'])
			img = "{}</div>".format(img)

			upd="{}<div><strong>{}</strong><br/>At {}<br/>Note :<br/>{}{}<div>".format(upd,row['status'],row['waktu'],row['note'],img)
			if row['lat']=="0.0" and row['lo']=="0.0":
				upd+="<div>GPS Tidak Tersedia Saat Melakukan Update ini</div>"
			else:
				upd+="""
			<div>
<iframe 
  width="300" 
  height="170" 
  frameborder="0" 
  scrolling="no" 
  marginheight="0" 
  marginwidth="0" 
  src="https://maps.google.com/maps?q="""+row['lat']+","+row['lo']+"""&hl=es;z=14&amp;output=embed"
 >
 </iframe>
			</div>"""

		self.job_order_history=upd
