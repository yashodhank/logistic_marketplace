# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.utils import get_request_session

class JobOrder(Document):
	pass
	def on_update(self):
		if self.driver:
			data  = frappe.db.sql("""select driver from `tabJob Order` where docstatus=1 and driver="{}" and status != "{}"  """.format(self.driver,self.status),as_list=1)
			status = "Tersedia"
			for row in data:
				found="Tidak Tersedia"
			frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(found,self.driver),as_list=1)
	def validate(self):
		if self.truck and self.strict==1:
			if self.truck_type!=self.suggest_truck_type:
				frappe.throw("Selected Truck Type cant be {} but it should be {}".format(self.truck_type,self.suggest_truck_type))

def notify():
	list_to = frappe.db.sql("""select HOUR(TIMEDIFF(NOW(),j.modified)) as "lama" ,j.principle , j.name , j.reference , j.modified , j.vendor , j.owner ,v.email
		from `tabJob Order` j left join `tabVendor` v on j.vendor = v.name where HOUR(TIMEDIFF(NOW(),j.modified)) IN (4,9) order by j.modified """,as_dict=1)
	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	header = {"Authorization: key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type: application/json"}
	for row in list_to:
		email = row['email']
		if email == "Administrator":
			continue
		subject=""
		if row['lama']=="4":
			subject="Job Order belum di terima lebih dari 4 jam"
			msg = "{} <{}> belum di terima lebih dari 4 jam".format(row['name'],row['reference'])
		else:
			subject="Job Order belum di terima lebih dari 9 jam"
			msg = "{} <{}> belum di terima lebih dari 4 jam".format(row['name'],row['reference'])
		content = {"to":"/topics/{}".format(row['vendor']) , "data":{"message":msg,"job_order":row['name']}}
		s.post(url,content,header)
		text = "Dear, {} <br/><br/>Principle : {}<br/>Jor Order : {}<br/>Reference No : {}<br/>Vendor : {}".format(row['principle'],row['vendor'],row['name'],row['reference'],row['vendor'])
		frappe.sendmail(recipients=email, subject=subject,content = text)

def test_notify():
	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	header = {"Authorization": "key=AIzaSyB29-83tq1N84EA1jieerQsPt_pZcRq_3w","Content-Type": "application/json"}
	content = {"to":"/topics/PT_CocaCola_Amatil_Indonesia", "data":{"message":"test"}}
	print s.post(url,header,content)
		
