# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Master",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Master")
		},
		{
			"module_name": "Penyedia",
			"color": "grey",
			"icon": "octicon octicon-organization",
			"type": "module",
			"label": _("Penyedia")
		},
		{
			"module_name": "Pengguna",
			"color": "grey",
			"icon": "octicon octicon-gist-secret",
			"type": "module",
			"label": _("Pengguna")
		}
	]
