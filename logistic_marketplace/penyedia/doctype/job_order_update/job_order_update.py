# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class JobOrderUpdate(Document):
	def on_submit(self):
		if self.status=="5. Proses Bongkar Selesai":
			jo = frappe.get_doc("Job Order",self.job_order)
			jo.status="Selesai"
			jo.save()
	
