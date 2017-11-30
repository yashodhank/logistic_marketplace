// Copyright (c) 2017, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Principle', {
	refresh: function(frm) {
		frm.set_df_property("email", "read_only", frm.doc.__islocal ? 0 : 1);
		//frm.set_df_property("password", "read_only", frm.doc.__islocal ? 0 : 1);
		frm.doc.password="";
		cur_frm.set_value("password","");
		if (frm.doc.__islocal==0){
		frappe.call({
				method: "logistic_marketplace.master.doctype.principle.principle.get_allowed_vendor",
				args: {
					user: frm.doc.email
				},
				callback: function(r, rt) {
					if(r.message) {
						vendor_list=""
						$.each(r.message, function(key, value) {
							if (vendor_list==""){
								vendor_list="<p>"+value["for_value"]+"</p>";
							}else{
								vendor_list+="<p>"+value["for_value"]+"</p>";
							}
						})
						frm.doc.vendor_list=vendor_list;
						frm.refresh();
					}
				}
			})
		}
	}
});
