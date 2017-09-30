from __future__ import unicode_literals
import frappe

#list
field = '*'
table = 'tabJob Order' 

@frappe.whitelist(allow_guest=True)
def list():
    query = 'SELECT ' + field + ' from `' + table + '`'
    result = frappe.db.sql(query,as_dict=1)
    return result
