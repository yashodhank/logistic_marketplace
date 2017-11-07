# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.password import update_password as _update_password
class Driver(Document):	
	def on_update(self):
		user = frappe.get_doc("User",self.email)
		user.new_password=self.password
		user.save()
	def before_insert(self):
		result = frappe.db.sql("""select name from `tabUser` where name="{}" """.format(self.email),as_list=1)
		for row in result:
			if row[0]==self.email:
				frappe.throw("Email Already Used {}".format(row[0]))
	def after_insert(self):
		password = "asd123"
		if self.password:
			password = self.password
		roles_to_apply=[{"role":"Driver"}]
		gg = frappe.get_doc({
			"doctype": "User",
			"email":self.email,
			"first_name":self.nama,
			"send_welcome_email":0,
			"new_password":password,
			"send_password_update_notification":0,
			"roles":roles_to_apply
			})

		gg.insert()
		_update_password(self.email,password)
		perm = frappe.get_doc({
			"doctype": "User Permission",
			"user":self.email,
			"allow":"Vendor",
			"for_value":self.vendor,
			"apply_for_all_roles":1
			})
		perm.insert()
		perm = frappe.get_doc({
			"doctype": "User Permission",
			"user":self.email,
			"allow":"Driver",
			"for_value":self.name,
			"apply_for_all_roles":1
			})
		perm.insert()

