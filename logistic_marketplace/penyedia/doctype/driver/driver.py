# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Driver(Document):	
	def on_update(self):
		result = frappe.db.sql("""select name from `tabUser` where name="{}" """.format(self.email),as_list=1)
		for row in result:
			frappe.throw("Email Already Used")
	def after_insert(self):
		password = "asd123"
		if self.password:
			password = self.password
		roles_to_apply=[{"role":"Driver"}]
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

