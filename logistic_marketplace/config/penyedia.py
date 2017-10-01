from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Job Order"
				},{
					"type": "doctype",
					"name": "Job Order Update"
				}
			]
		},
		{
			"label": _("Master"),
			"items": [
				{
					"type": "doctype",
					"name": "Driver"
				},
				{
					"type": "doctype",
					"name": "Vendor Contact Person"
				}
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "page",
					"name": "job-order-last-updat",
					"label": "Job Order Last Update Position",
				}
			]
		}
	]