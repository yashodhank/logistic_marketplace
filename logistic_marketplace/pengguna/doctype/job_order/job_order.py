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
	def on_update_after_submit(self):
		#frappe.msgprint(self.driver)
		if self.driver:
			data  = frappe.db.sql("""select driver from `tabJob Order` where docstatus=1 and driver="{}" and status = "Dalam Proses"  """.format(self.driver),as_list=1)
			found = "Tersedia"
			for row in data:
				found="Tidak Tersedia"
			if self.status=="Dalam Proses":
				s = get_request_session()
				url = "https://fcm.googleapis.com/fcm/send"
				header = {"Authorization": "key=AAAAnuCvOxY:APA91bGdCn20mHlHrWEpGiNsiSmb36HEG0QmZ-L7U_iG8eOjm9btCFUgYn8klNStKetvEA1eFdiEmaopdScVk-jv_HNvnLwq4m1VI8LdrIueh9NFI6p5hVjdxs73THqvcRFQ8tZjtv61","Content-Type": "application/json"}
				content = {
					"to":"/topics/{}".format(self.driver.replace(" ","_").replace("@","_")),
					"data": 
						{
							#notification
							"title":self.name,
							"body":"Job Order {} di tugaskan".format(self.vendor),

							#data
							"job_order":self.name,
							"action":"NEW ASSIGNED JO"
						}
				}
				s.post(url=url,headers=header,data=json.dumps(content))

			frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(found,self.driver),as_list=1)
		if self.status=="Di Tolak":			
			s = get_request_session()
			url = "https://fcm.googleapis.com/fcm/send"
			header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}
			content ={
				"to":"/topics/{}".format(self.principle.replace(" ","_").replace("@","")),
				"data":
					{
						#notification
						"title":self.name,
						"body":"Job Order {} di tolak oleh {}".format(self.name,self.vendor),

						#data
						"job_order":self.name,
						"action":"REJECTED"
					}
			}
			s.post(url=url,headers=header,data=json.dumps(content))

			#frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(found,self.driver),as_list=1)
			#frappe.msgprint("updated")
	def validate(self):
		if self.truck and self.strict==1:
			if self.truck_type!=self.suggest_truck_type:
				frappe.throw("Selected Truck Type cant be {} but it should be {}".format(self.truck_type,self.suggest_truck_type))

	def on_submit(self):
		list_to = frappe.db.sql("""select email from `tabVendor` where name="{}" """.format(self.vendor),as_dict=1)
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"
		header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}
		for row in list_to:
			email = row['email']
			if email == "Administrator":
				continue
			subject=""
			subject="Job Order baru dari {}".format(self.principle)
			msg = "{} <{}> telah di berikan oleh {}".format(self.name,self.reference,self.principle)
			content = {
				"to":"/topics/{}".format(self.vendor.replace(" ","_")),
				"data":
					{
						#notification
						"title":self.name,
						"body":msg,

						#data
						"job_order":self.name,
						"action":"NEW JO"
					}
			}
			s.post(url=url,headers=header,data=json.dumps(content))
			#text = "Dear, {} <br/><br/>Principle : {}<br/>Jor Order : {}<br/>Reference No : {}<br/>Vendor : {}".format(row['principle'],row['vendor'],row['name'],row['reference'],row['vendor'])
			#frappe.sendmail(recipients=email, subject=subject,content = text)
def notify():
	list_to = frappe.db.sql("""select HOUR(TIMEDIFF(NOW(),j.modified)) as "lama" ,j.principle , j.name , j.reference , j.modified , j.vendor , j.owner ,v.email	from `tabJob Order` j left join `tabVendor` v on j.vendor = v.name where HOUR(TIMEDIFF(NOW(),j.modified)) IN (4,9) and j.status="Menunggu Persetujuan Vendor" order by j.modified """,as_dict=1)
	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
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
			msg = "{} <{}> belum di terima lebih dari 9 jam".format(row['name'],row['reference'])
		content = {
			"to":"/topics/{}".format(row['vendor'].replace(" ","_")),
			"data":
			{
				#notification
				"title":row["name"],
				"body":msg,

				#data
				"job_order":row["name"],
				"value":row["lama"],
				"ACTION":"RTO JO"
			}
		}
		s.post(url=url,headers=header,data=json.dumps(content))
		#text = "Dear, {} <br/><br/>Principle : {}<br/>Jor Order : {}<br/>Reference No : {}<br/>Vendor : {}".format(row['principle'],row['vendor'],row['name'],row['reference'],row['vendor'])
		#frappe.sendmail(recipients=email, subject=subject,content = text)

def test_notify():
	s = get_request_session()
	url = "https://fcm.googleapis.com/fcm/send"
	header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
	content = {"to":"/topics/PT_CocaCola_Amatil_Indonesia","notification":{"title":"title","body":"body"}, "data":{"job_order":"JO-20171000037"}}
	gg =  s.post(url=url,headers=header,data=json.dumps(content))
	print gg.content
		
