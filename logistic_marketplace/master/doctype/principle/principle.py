# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.password import update_password as _update_password , get_decrypted_password
class Principle(Document):
	def on_update(self):
		_update_password(self.email,get_decrypted_password("Principle",self.name))
	def validate(self):
		result = frappe.db.sql("""select name from `tabUser` where name="{}" """.format(self.email),as_list=1)
		for row in result:
			if row[0]==self.email:
				frappe.throw("Email Already Used {}".format(row[0]))
	def after_insert(self):
		password = get_decrypted_password("Principle",self.name)
		roles_to_apply=[{"role":"Principle"}]
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
			"allow":"Principle",
			"for_value":self.name,
			"apply_for_all_roles":1
			})
		perm.insert()
	
