# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobOrder(Document):
	pass
	def validate(self):
		if self.truck and self.strict==1:
			if self.truck_type!=self.suggest_truck_type:
				frappe.throw("Selected Truck Type cant be {} but it should be {}".format(self.truck_type,self.suggest_truck_type))

def notify():
	list_to = frappe.db.sql("""select HOUR(TIMEDIFF(NOW(),modified)) as "lama" ,principle , name , reference , modified , vendor , owner from `tabJob Order` where HOUR(TIMEDIFF(NOW(),modified)) IN (4,9) order by modified """,as_dict=1)
	for row in list_to:
		email = row['owner']
		if email == "Administrator":
			continue
		subject=""
		if row['lama']=="4":
			subject="Job Order belum di terima lebih dari 4 jam"
		else:
			subject="Job Order belum di terima lebih dari 9 jam"
		text = "Dear, {} <br/><br/>Jor Order : {}<br/>Reference No : {}<br/>Vendor : {}".format(row['principle'],row['name'],row['reference'],row['vendor'])
		frappe.sendmail(recipients=email, subject=subject,
				content = text)