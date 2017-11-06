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
				}
			]
		},
		{
			"label": _("Master"),
			"items": [
				{
					"type": "doctype",
					"name": "Principle Contact Person"
				},
				{
					"type":"doctype",
					"name":"Location"
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
				},
				{
					"type":"page",
					"name":"live-map",
					"label":"Live Map"
				},
				{
                                        "type":"page",
                                        "name":"all-driver-map",
                                        "label":"All Driver Map"
                                }
			]
		}
	]
