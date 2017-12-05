# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.utils import get_request_session

class JobOrderUpdate(Document):
	def on_submit(self):
		if self.status=="6. Pekerjaan Selesai":
			jo = frappe.get_doc("Job Order",self.job_order)
			jo.status="Selesai"
			jo.save()
			s = get_request_session()
			url = "https://fcm.googleapis.com/fcm/send"
			header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}

			content = {"to":"/topics/{}".format(self.principle.replace(" ","_")) , "notification":{"title":self.job_order,"body":"Telah Selesai Oleh {}".format(self.vendor),"sound":"default"}, "data":{"job_order":self.job_order}}
			s.post(url=url,headers=header,data=json.dumps(content))
			header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}

			content = {"to":"/topics/{}".format(self.vendor.replace(" ","_")) , "notification":{"title":self.job_order,"body":"Telah Selesai","sound":"default"}, "data":{"job_order":self.job_order}}
			s.post(url=url,headers=header,data=json.dumps(content))
			

			
