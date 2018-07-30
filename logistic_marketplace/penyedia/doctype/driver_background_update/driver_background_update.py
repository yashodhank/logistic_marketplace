# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json
from frappe.utils import get_request_session

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

	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	if (len(data) > 0):
		users = data[0]
		#vendor
		header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
		content = {
			"to":"/topics/{}".format(users[0].replace(" ","_").replace("-","_").replace("(","").replace(")","").replace(".", "_").replace("@", "_").replace("-","_").replace("(","").replace(")","").replace(".", "_").replace("@", "_")),
			"data":
				{
					"subject":"{}".format(users[0].replace(" ","_").replace("-","_").replace("(","").replace(")","").replace(".", "_").replace("@", "_")),
					
					#notification
					"title":"Perubahan GPS dari {}".format(self.driver),

					#data
					"driver":"{}".format(self.driver),
					"action":"GPS_UPDATE"
				}
		}
		s.post(url=url,headers=header,data=json.dumps(content))

	# data  = frappe.db.sql("""SELECT principle FROM `tabJob Order` WHERE status='Dalam Proses' AND driver='{}'""".format(self.driver),as_list=1)

	# if (len(data) > 0):
	# 	users = data[0]
	# 	#principle
	# 	header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}
	# 	content = {
	# 		"to":"/topics/{}".format(users[0].replace(" ","_").replace("-","_").replace("(","").replace(")","").replace(".", "_").replace("@", "_")),
	# 		"data":
	# 			{
	# 				"subject":"{}".format(users[0].replace(" ","_").replace("-","_").replace("(","").replace(")","").replace(".", "_").replace("@", "_")),
					
	# 				#notification
	# 				"title":"Perubahan GPS dari {}".format(self.driver),

	# 				#data
	# 				"driver":"{}".format(self.driver),
	# 				"action":"GPS_UPDATE"
	# 			}
	# 	}
	# 	s.post(url=url,headers=header,data=json.dumps(content))


