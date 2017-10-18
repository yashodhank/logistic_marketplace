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
	def validate(self):
		if self.truck and self.strict==1:
			if self.truck_type!=self.suggest_truck_type:
				frappe.throw("Selected Truck Type cant be {} but it should be {}".format(self.truck_type,self.suggest_truck_type))

def notify():
	list_to = frappe.db.sql("""select HOUR(TIMEDIFF(NOW(),modified)) as "lama" ,principle , name , reference , modified , vendor , owner from `tabJob Order` where HOUR(TIMEDIFF(NOW(),modified)) IN (4,9) order by modified """,as_dict=1)
	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	header = {"Authorization: key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type: application/json"}
	for row in list_to:
		email = row['owner']
		if email == "Administrator":
			continue
		subject=""
		if row['lama']=="4":
			subject="Job Order belum di terima lebih dari 4 jam"
			msg = "{} <{}> belum di terima lebih dari 4 jam".format(row['name'],row['reference'])
		else:
			subject="Job Order belum di terima lebih dari 9 jam"
			msg = "{} <{}> belum di terima lebih dari 4 jam".format(row['name'],row['reference'])
		content = {"to":"/topics/{}".format(row['principle']) , "data":{"message":msg,"job_order":row['name']}
		s.post(url,data=content,header=header)
		text = "Dear, {} <br/><br/>Jor Order : {}<br/>Reference No : {}<br/>Vendor : {}".format(row['principle'],row['name'],row['reference'],row['vendor'])
		#frappe.sendmail(recipients=email, subject=subject,content = text)