// Copyright (c) 2017, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver', {
	refresh: function(frm) {
		frm.set_df_property("email", "read_only", frm.doc.__islocal ? 0 : 1);
	}
});
