from __future__ import unicode_literals
import frappe
import json
import time
import datetime
import os


#JOB ORDER
@frappe.whitelist(allow_guest=False)
def get_route(startjou='', endjou='',driver=''):
	data = frappe.db.sql("SELECT lo, lat, creation FROM `tabDriver Background Update` WHERE creation >= (SELECT creation FROM `tabJob Order Update` WHERE name='{}') AND creation <= (SELECT creation FROM `tabJob Order Update` WHERE name='{}') AND driver = '{}' AND lo != '0.0' AND lat != '0.0' AND lo != '' AND lat != '' GROUP BY lo * lat ORDER BY creation ASC;".format(startjou,endjou,driver),as_dict=1)

	return data

@frappe.whitelist(allow_guest=False)
def get_last_route(lastjou='',driver=''):
	data = frappe.db.sql("SELECT lo, lat, creation FROM `tabDriver Background Update` WHERE creation >= (SELECT creation FROM `tabJob Order Update` WHERE name='{}') AND driver = '{}' AND lo != '0.0' AND lat != '0.0' AND lo != '' AND lat != '' GROUP BY lo * lat ORDER BY creation ASC;".format(lastjou,driver),as_dict=1)

	return data

@frappe.whitelist(allow_guest=False)
def get_job_order(status='',principle='',vendor='',driver='',ref='%',start=0):
	filters = frappe.local.form_dict
	if principle != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND principle='{}' AND (LOWER(reference) LIKE LOWER('{}') OR LOWER(name) LIKE LOWER('{}')) AND docstatus = 1 ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,principle,ref,ref,start),as_dict=1)
	elif vendor != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND vendor='{}' AND (LOWER(reference) LIKE LOWER('{}') OR LOWER(name) LIKE LOWER('{}')) AND docstatus = 1 ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,vendor,ref,ref,start),as_dict=1)
	elif driver != '':
		data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE status='{}' AND driver='{}' AND (LOWER(reference) LIKE LOWER('{}') OR LOWER(name) LIKE LOWER('{}')) AND docstatus = 1 ORDER BY modified DESC LIMIT 20 OFFSET {}".format(status,driver,ref,ref,start),as_dict=1)
	# data = frappe.get_list("Job Order",filters={ 
	# 	'status':status,
	# 	'principle':principle
	# 	},fields=["*"],order_by='modified')
	

	for row in data:
		row['routes'] = frappe.db.sql("select * from `tabJob Order Route` where parent='{}'".format(row.name),as_dict=1)
		
		fetch_principle = frappe.db.sql("SELECT email FROM `tabPrinciple` WHERE nama ='{}'".format(row.principle), as_list=True)
		if (len(fetch_principle) > 0):
			user_principle = fetch_principle[0][0]
			fetch_principle_image = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(user_principle), as_list=True)
			if (len(fetch_principle_image) > 0):
				row['principle_image'] = fetch_principle_image[0]
			else:
				row['principle_image'] = list("")

		fetch_vendor = frappe.db.sql("SELECT email FROM `tabVendor` WHERE nama ='{}'".format(row.vendor), as_list=True)
		if (len(fetch_vendor) > 0):
			user_vendor = fetch_vendor[0][0]
		fetch_vendor_image = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(user_vendor), as_list=True)
		if (len(fetch_vendor_image) > 0):
			row['vendor_image'] = fetch_vendor_image[0]
		else:
			row['vendor_image'] = list("")
	return data

@frappe.whitelist(allow_guest=False)
def get_job_order_update(job_order=""):
	data = frappe.db.sql("SELECT * FROM `tabJob Order Update` WHERE job_order = '{}' AND docstatus = 1 ORDER BY creation DESC".format(job_order),as_dict=1)
	if (len(data) > 0):
		for row in data:
			row['image_count'] = frappe.db.sql("SELECT file_url FROM `tabFile` WHERE attached_to_doctype = 'Job Order Update' AND attached_to_name = '{}'".format(row['name']),as_dict=True)
		return data
	else:
		return []

@frappe.whitelist(allow_guest=False)
def get_image_jo_update(jod_name=''):
	request_attachments = frappe.db.sql("SELECT file_url FROM `tabFile` WHERE attached_to_doctype = 'Job Order Update' AND attached_to_name = '{}'".format(jod_name), as_dict=True)
	return request_attachments




@frappe.whitelist(allow_guest=False)
def get_job_order_by(name=''):
	data = frappe.db.sql("SELECT * FROM `tabJob Order` WHERE name='{}' ORDER BY modified DESC LIMIT 1".format(name),as_dict=1)
	for row in data:
		row['routes'] = frappe.db.sql("select * from `tabJob Order Route` where parent='{}'".format(row.name),as_dict=1)
		
		fetch_principle = frappe.db.sql("SELECT email FROM `tabPrinciple` WHERE nama ='{}'".format(row.principle), as_list=True)
		if (len(fetch_principle) > 0):
			user_principle = fetch_principle[0][0]
			fetch_principle_image = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(user_principle), as_list=True)
			if (len(fetch_principle_image) > 0):
				row['principle_image'] = fetch_principle_image[0]
			else:
				row['principle_image'] = list("")

		fetch_vendor = frappe.db.sql("SELECT email FROM `tabVendor` WHERE nama ='{}'".format(row.vendor), as_list=True)
		if (len(fetch_vendor) > 0):
			user_vendor = fetch_vendor[0][0]
			fetch_vendor_image = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(user_vendor), as_list=True)
			if (len(fetch_vendor_image) > 0):
				row['vendor_image'] = fetch_vendor_image[0]
			else:
				row['vendor_image'] = list("")
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
		data[stat] = frappe.db.sql("SELECT COUNT(name) as count FROM `tabJob Order` WHERE {}='{}' AND docstatus = 1 AND status='{}' ORDER BY modified".format(role,id,stat),as_dict=1)[0]
	return data

#DRIVER
# @frappe.whitelist(allow_guest=False)
# def validate_driver():
# 	driver = frappe.db.sql("SELECT * FROM `tabDriver`", as_dict=True)
# 	for row in driver:
# 		job_order = frappe.db.sql("""select driver from `tabJob Order` where docstatus=1 and driver="{}" and status = "Dalam Proses"  """.format(row.driver),as_list=1)
# 		if (len(job_order) > 0 && row)

@frappe.whitelist(allow_guest=False)
def get_driver(vendor='',ref='%',status='',start=0):
	if (status == ''):
		data = frappe.db.sql("SELECT * FROM `tabDriver` WHERE vendor ='{}' AND (nama LIKE '{}%' OR email LIKE '{}%') LIMIT 20 OFFSET {}".format(vendor,ref,ref,start), as_dict=True)
	else:
		data = frappe.db.sql("SELECT * FROM `tabDriver` WHERE vendor ='{}' AND status = '{}' AND (nama LIKE '{}%' OR email LIKE '{}%') LIMIT 20 OFFSET {}".format(vendor,status,ref,ref,start), as_dict=True)
	if len(data) > 0:
		dataUser = data[0]
		fetchProfileImage = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(dataUser['email']), as_list=True)
		if len(fetchProfileImage) > 0:
			dataUser['profile_image'] = fetchProfileImage[0]
		else:
			dataUser['profile_image'] = list("")

	return data

#USER

@frappe.whitelist(allow_guest=False)
def get_user(principle='',vendor='',driver=''):
	if principle != '':
		data = frappe.db.sql("SELECT * FROM `tabPrinciple` WHERE name = '{}'".format(principle), as_dict=True)
	elif vendor != '':
		data = frappe.db.sql("SELECT * FROM `tabVendor` WHERE name = '{}'".format(vendor), as_dict=True)
	elif driver != '':
		data = frappe.db.sql("SELECT * FROM `tabDriver` WHERE name = '{}'".format(driver), as_dict=True)

	if len(data) > 0:
		dataUser = data[0]
		fetchProfileImage = frappe.db.sql("SELECT user_image FROM `tabUser` WHERE email = '{}'".format(dataUser['email']), as_list=True)
		if len(fetchProfileImage) > 0:
			dataUser['profile_image'] = fetchProfileImage[0]
		else:
			dataUser['profile_image'] = list("")
	return data

@frappe.whitelist(allow_guest=True)
def validate_email(email=''):
	data = frappe.db.sql("SELECT full_name FROM `tabUser` WHERE email = '{}'".format(email), as_dict=True)
	return data

@frappe.whitelist(allow_guest=True)
def write_log(errorCode='',log=''):
	if not os.path.exists("~/api_log.txt"):
		new_file = open("~/api_log.txt","w")
		new_file.close()
	file = open("api_log.txt","a")
	ts = time.time() 
 	now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
 	file.write("Error Log with code {} at {}".format(errorCode, now))
 	file.write('{}'.format(log))
	file.write('\n')
	file.close()


