# -*- coding: utf-8 -*-
# Copyright (c) 2017, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DriverBackgroundUpdate(Document):
	def validate(self):
		doc = frappe.get_doc("Driver",self.driver)
		doc.lo = self.lo
		doc.lat = self.lat
		doc.batery = self.batery
		doc.signal=self.signal
		doc.last_update = self.last_update
		doc.save()
