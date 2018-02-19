from __future__ import unicode_literals
import frappe


@frappe.whitelist(allow_guest=True)
def add_principle_contact_person():
    try:
        req = frappe.local.form_dict
        
        data = {
            "nama": req.nama,
            "telp": req.telp,
            principle: req.principle,
            "doctype": "Principle Contact Person",
            "docstatus":0,
            "reference_doctype":"Principle"
        }
        response = frappe.get_doc(data).insert().as_dict()
        frappe.db.commit()
        return response
    except ValueError as e:
	return 'error is occured'
