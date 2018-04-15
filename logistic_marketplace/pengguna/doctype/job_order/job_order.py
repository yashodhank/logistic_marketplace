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
	def onload(self):
		job_order_update = frappe.db.sql("""select name,DATE_FORMAT(waktu,"%d-%m-%Y %H:%i") as "waktu",note,status,lo,lat,owner,vendor,principle from `tabJob Order Update` where job_order="{}" order by waktu asc """.format(self.name),as_dict=1)
		upd = ""
		for row in job_order_update:
			image_list = frappe.db.sql("""select file_url from `tabFile` where attached_to_doctype="Job Order Update" and attached_to_name="{}" """.format(row['name']),as_dict=1)
			img = "<div>"
			for gg in image_list:
				img="""{}<img src="{}" style="padding-right:20px;"/> """.format(img,gg['file_url'])
			img = "{}</div>".format(img)

			upd="{}<div><strong>{}</strong><br/>At {}<br/>Note :<br/>{}<br/>Done by : {}{}<div>".format(upd,row['status'],row['waktu'],row['note'],row['owner'],img)
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
		#self.save()
		frappe.db.sql("""update `tabJob Order` set job_order_history='{}' where name="{}" """.format(upd,self.name),as_list=1)
		frappe.db.commit()
	def on_update_after_submit(self):
		#frappe.msgprint(self.driver)
		if self.driver:
			data  = frappe.db.sql("""select driver from `tabJob Order` where docstatus=1 and driver="{}" and status = "Dalam Proses"  """.format(self.driver),as_list=1)
			found = "Tersedia"
			for row in data:
				found="Tidak Tersedia"
			frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(found,self.driver),as_list=1)		
			if self.status=="Dalam Proses":
				s = get_request_session()
				url = "https://fcm.googleapis.com/fcm/send"
				header = {"Authorization": "key=AAAAnuCvOxY:APA91bGdCn20mHlHrWEpGiNsiSmb36HEG0QmZ-L7U_iG8eOjm9btCFUgYn8klNStKetvEA1eFdiEmaopdScVk-jv_HNvnLwq4m1VI8LdrIueh9NFI6p5hVjdxs73THqvcRFQ8tZjtv61","Content-Type": "application/json"}
				content = {
					"to":"/topics/{}".format(self.driver.replace(" ","_").replace("@","_")),
					"data": 
						{
							"subject":"{}".format(self.driver.replace(" ","_").replace("@","_")),

							#notification
							"title":"{} <{}>".format(self.name,self.reference),
							"body":"Job Order {} di tugaskan".format(self.vendor),

							#data
							"job_order":self.name,
							"action":"NEW_ASSIGNED_JO"
						}
				}
				s.post(url=url,headers=header,data=json.dumps(content))
			
		if self.status=="Di Tolak":			
			s = get_request_session()
			url = "https://fcm.googleapis.com/fcm/send"
			header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}
			content ={
				"to":"/topics/{}".format(self.principle.replace(" ","_").replace("@","")),
				"data":
					{
						"subject":"{}".format(self.principle.replace(" ","_").replace("@","")),

						#notification
						"title":"{} <{}>".format(self.name,self.reference),
						"body":"Job Order {} di tolak oleh {}".format(self.name,self.vendor),

						#data
						"job_order":self.name,
						"action":"REJECTED"
					}
			}
			s.post(url=url,headers=header,data=json.dumps(content))

			#frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(found,self.driver),as_list=1)
			#frappe.msgprint("updated")

	def on_cancel(self):
		data  = frappe.db.sql("""select driver from `tabJob Order` where driver="{}" and status = "Dalam Proses" and name != "{}" """.format(self.driver,self.name),as_list=1)
		status = "Tersedia"
		if (len(data) > 0):
			status = "Tidak Tersedia"
		frappe.db.sql("""update `tabDriver` set status="{}" where name="{}" """.format(status, self.driver),as_list=1)

	def validate(self):
		if self.truck and self.strict==1:
			if self.truck_type!=self.suggest_truck_type:
				frappe.throw("Selected Truck Type cant be {} but it should be {}".format(self.truck_type,self.suggest_truck_type))

	def on_submit(self):
		list_to = frappe.db.sql("""select email from `tabVendor` where name="{}" """.format(self.vendor),as_dict=1)
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"
		header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
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
						"subject":"{}".format(self.vendor.replace(" ","_")),

						#notification
						"title":"{} <{}>".format(self.name,self.reference),
						"body":msg,

						#data
						"job_order":self.name,
						"action":"NEW_JO"
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
				"subject":"{}".format(row['vendor'].replace(" ","_")),

				#notification
				"title":row["name"],
				"body":msg,

				#data
				"job_order":row["name"],
				"value":row["lama"],
				"ACTION":"RTO_JO"
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

def chat(self, method):
	if self.reference_doctype!="Job Order":
		return
	if self.comment_type!="Comment":
		return
	data  = frappe.db.sql("""select principle, vendor, driver from `tabJob Order` where name='{}' """.format(self.reference_name),as_list=1)
	

	if (len(data) > 0):
		users = data[0]

		#principle
		# s = get_request_session()
		# url = "https://fcm.googleapis.com/fcm/send"
		# header = {"Authorization": "key=AAAA66ppyJE:APA91bFDQd8klnCXe-PTgLUkUD7x4p9UAxW91NbqeTN9nbX7-GmJMlsnQ2adDd84-rl6LqKnD7KLSeM9xBmADnPuRh0YadoQKux7IrZ27tsjVzvzlFDoXuOnZRP7eXrf0k51QGGifLGw","Content-Type": "application/json"}
		# content = {
		# 	"to":"/topics/{}".format(users[0].replace(" ","_")),
		# 	"data":
		# 		{
		# 			#notification
					# "title":"{} - Pesan dari {}".format(self.reference_name,self.sender_full_name),
		# 			"body":"{}".format(self.content),

		# 			#data
		# 			"job_order":"{}".format(self.reference_name),
		# 			"sender":"{}".format(self.sender_full_name),
		# 			"action":"CHAT JOB ORDER"
		# 		}
		# }
		# s.post(url=url,headers=header,data=json.dumps(content))

		#vendor
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"
		header = {"Authorization": "key=AAAA7ndto_Q:APA91bHVikGANVsFaK2UEKLVXQEA1cleaeM7DlLLuaA87jEVhBGNTe4t8fi0h5Ttc7jRkoiEkZYlrw7Idsn9S9ZfDFtl1S3H3j21Xs8VXtANCDjycLLkMAyLLdHKaBfi3NYc3Z8VIxo8","Content-Type": "application/json"}
		content = {
			"to":"/topics/{}".format(users[1].replace(" ","_")),
			"data":
				{
					"subject":"{}".format(users[1].replace(" ","_")),

					#notification
					"title":"{} - Pesan dari {}".format(self.reference_name,self.sender_full_name),
					"body":"{}".format(self.content),

					#data
					"job_order":"{}".format(self.reference_name),
					"sender":"{}".format(self.sender_full_name),
					"action":"CHAT JOB ORDER"
				}
		}
		s.post(url=url,headers=header,data=json.dumps(content))

		#driver
		fetchDriver = frappe.db.sql("""SELECT nama FROM `tabDriver` WHERE name='{}'""".format(users[2]),as_list=1)
		dataDriver = fetchDriver[0]
		driverName = dataDriver[0]
		s = get_request_session()
		url = "https://fcm.googleapis.com/fcm/send"
		header = {"Authorization": "key=AAAAnuCvOxY:APA91bGdCn20mHlHrWEpGiNsiSmb36HEG0QmZ-L7U_iG8eOjm9btCFUgYn8klNStKetvEA1eFdiEmaopdScVk-jv_HNvnLwq4m1VI8LdrIueh9NFI6p5hVjdxs73THqvcRFQ8tZjtv61","Content-Type": "application/json"}
		content = {
			"to":"/topics/{}".format(users[2].replace(" ","_").replace("@","_")),
			"data": 
				{
					"subject":"{}".format(users[2].replace(" ","_").replace("@","_")),

					#notification
					"title":"{} - Pesan dari {}".format(self.reference_name,driverName),
					"body":"{}".format(self.content),

					#data
					"job_order":"{}".format(self.reference_name),
					"sender":"{}".format(self.sender_full_name), 
					"action":"CHAT JOB ORDER"
				}
		}
		s.post(url=url,headers=header,data=json.dumps(content))

		

		
