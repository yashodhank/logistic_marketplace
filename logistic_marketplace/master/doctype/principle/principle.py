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
			"apply_for_all_roles":0
			})
		perm.insert()
	def do_add(self):
		if self.vendor:
			user_list = frappe.db.sql("""select user from `tabUser Permission` where allow="Principle" and for_value="{}" """.format(self.name),as_dict=1)
			for row in user_list:
				add=1
				exist = frappe.db.sql("""select user from `tabUser Permission` where allow="Vendor" and for_value="{}" """.format(self.vendor),as_dict=1)
				for invalid in exist:
					add=0
				if add==1:
					perm = frappe.get_doc({
						"doctype": "User Permission",
						"user":row['user'],
						"allow":"Vendor",
						"for_value":self.vendor,
						"apply_for_all_roles":0
					})
					perm.insert()
			self.vendor_list="""{}<p>{}</p>""".format(self.vendor_list,self.vendor)
	def do_remove(self):
		user_list = frappe.db.sql("""select user from `tabUser Permission` where allow="Principle" and for_value="{}" """.format(self.name),as_dict=1)
			for row in user_list:
				frappe.db.sql("""delete from `tabUser Permission` where allow="Vendor" and for_value="{}" and user="{}" """.format(self.vendor,row['user']))
			new_list = frappe.db.sql("""select for_value from `tabUser Permission` where allow="Vendor" and user="{}" """.format(self.email),as_dict=1)
			vendor_list=""
			for row in new_list:
				vendor_list="""{}<p>{}</p>""".format(vendor_list,row['for_value'])
			self.vendor_list=vendor_list
@frappe.whitelist()
def get_allowed_vendor(user):
	return frappe.db.sql("""select for_value from `tabUser Permission` where allow="Vendor" and user="{}" """.format(user),as_dict=1)