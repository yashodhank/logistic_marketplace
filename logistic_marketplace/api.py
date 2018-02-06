from __future__ import unicode_literals
import frappe
import json
@frappe.whitelist(allow_guest=False)
def get_job_order(status='',principle='',vendor='',driver='',ref='%%',start=0):
	filters = frappe.local.form_dict
	if principle != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND principle='{}' AND reference LIKE '{}' ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,principle,ref,start),as_dict=1)
	elif vendor != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND vendor='{}' AND reference LIKE '{}' ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,vendor,ref,start),as_dict=1)
	elif driver != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND driver='{}' AND reference LIKE '{}' ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,driver,ref,start),as_dict=1)
	# data = frappe.get_list("Job Order",filters={ 
	# 	'status':status,
	# 	'principle':principle
	# 	},fields=["*"],order_by='modified')
	for row in data:
		row['routes'] = frappe.db.sql("select * from `tabJob Order Route` where parent='{}'".format(row.name),as_dict=1)
	return data



@frappe.whitelist(allow_guest=False)
def get_job_order_by(name=''):
	data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE name='{}' ORDER BY modified DESC LIMIT 1".format(name),as_dict=1)
	for row in data:
		row['routes'] = frappe.db.sql("select * from `tabJob Order Route` where parent='{}'".format(row.name),as_dict=1)
	return data

@frappe.whitelist(allow_guest=False)
def get_job_order_count(role='',id=''):
	status = []
	if role == 'principle':
		status = ['Menunggu Persetujuan Vendor', 'Dalam Proses', 'Selesai', 'Di Tolak']
	elif role == 'vendor':
		status = ['Menunggu Persetujuan Vendor', 'Dalam Proses', 'Selesai']
	elif role == 'driver':
		status = ['Dalam Proses', 'Selesai']

	data = dict()
	for stat in status:
		data[stat] = frappe.db.sql("SELECT COUNT(name) as count FROM `tabJob Order` WHERE {}='{}' AND status='{}' ORDER BY modified".format(role,id,stat),as_dict=1)[0]
	return data

