# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DriverBackgroundUpdate(Document):
	def validate(self):
		doc = frappe.get_doc("Driver",self.driver)
		doc.lo = self.lo
		doc.lat = self.lat
		doc.batery = self.batery
		doc.signal=self.signal
		doc.last_update = self.last_update
		doc.save()


	def gps_update(self, method):
		data  = frappe.db.sql("""select vendor from `tabDriver` where name='{}' """.format(self.driver),as_list=1)
		if (len(data) > 0):
			users = data[0]
			#vendor
			s = get_request_session()
			url = "https://fcm.googleapis.com/fcm/send"
			header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
			content = {
				"to":"/topics/{}".format(users[0].replace(" ","_")),
				"data":
					{
						#notification
						"title":"Perubahan GPS dari {}".format(self.driver),

						#data
						"driver":"{}".format(self.driver),
						"action":"GPS UPDATE"
					}
			}
			s.post(url=url,headers=header,data=json.dumps(content))
