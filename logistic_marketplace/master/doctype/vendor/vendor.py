# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Vendor(Document):
	def validate(self):
		result = frappe.db.sql("""select name from `tabUser` where name="{}" """.format(self.email),as_list=1)
		for row in result:
			if row[0]==self.email:
				frappe.throw("Email Already Used {}".format(row[0]))
	def after_insert(self):
		password = "asd123"
		if self.password:
			password = self.password
		roles_to_apply=[{"role":"Vendor"}]
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
			"for_value":self.name,
			"apply_for_all_roles":1
			})
		perm.insert()
