from __future__ import unicode_literals
import frappe

import json
import file_manager
from file_manager import upload
from base import validate_method
from base import validate_param_value
from base import validate_param_exist
from base import validate_dict_exist
from base import validate_time_format
from datetime import datetime
import os, base64, re


#list
field = '*'
table = 'tabJob Order' 

@frappe.whitelist(allow_guest=True)
def image():
	response = {}

	validate = validate_method(frappe.local.request.method,["POST"])
	if validate != True:
		return validate

	req = frappe.local.form_dict
	req.filename = "checkpoint.jpg"

	validate = validate_param_exist([req.checkpoint_id, req.filedata],"checkpoint_id, image")
	if validate != True:
		return validate

	try:

		uploaded = upload("Job Order Update",req.checkpoint_id,1)

		data = {
			"doctype": "Job Order Update Image",
			"docstatus": 0,
			"parent": req.checkpoint_id,
			"parenttype": "Check Point",
			"parentfield": "checkpoint_image",
			"attach": uploaded["file_url"]
		}
			
		result = frappe.get_doc(data).insert().as_dict()

		response["code"] = 200
		response["message"] = "Success"
		response["data"] = result

	except Exception as e:
		response["code"] = 400
		response["message"] = e.message
		response["data"] = ""
	except UnboundLocalError as e:
		response["code"] = 400
		response["message"] = e.message
		response["data"] = ""

	return response
