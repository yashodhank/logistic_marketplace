# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Driver(Document):	
	def on_update(self):
		self.user_setup()
	def user_setup(self):
		gg = frappe.db.sql("""select name from tabUser where name="{}" """.format(self.email))
		found=0
		for row in gg:
			found =1
		if found==1 :
			if self.password:
				#update the password
				pass
		else:
			password = "asd123"
			if self.password:
				password = self.password
			roles_to_apply=[{"role":"System Manager"}]

			doc = frappe.get_doc({
				"doctype": "User",
				"email":self.email,
				"first_name":self.nama,
				"send_welcome_email":0,
				"new_password":password,
				"send_password_update_notification":0,
				"roles":roles_to_apply
				})
			doc.insert()

