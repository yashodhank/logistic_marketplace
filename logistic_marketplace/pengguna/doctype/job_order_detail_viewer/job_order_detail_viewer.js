// Copyright (c) 2017, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order Detail Viewer', {
	refresh: function(frm) {

	},
	onload:function(frm) {
		frm.disable_save();
		frm.doc.job_order=""
		frm.doc.jo_status = ""
		frm.doc.principle =""
		frm.doc.reference =""
		frm.doc.principle_contact_person=""
		frm.doc.nama_principle_cp=""
		frm.doc.telp_principle_cp=""
		frm.doc.vendor=""
		frm.doc.vendor_contact_person=""
		frm.doc.nama_vendor_cp=""
		frm.doc.telp_vendor_cp=""
		frm.doc.pick_location=""
		frm.doc.kota_pengambilan=""
		frm.doc.alamat_pengambilan=""
		frm.doc.nama_gudang_pengambilan=""
		frm.doc.kode_distributor_pengambilan=""
		frm.doc.delivery_location=""
		frm.doc.kota_pengiriman=""
		frm.doc.alamat_pengiriman=""
		frm.doc.nama_gudang_pengiriman=""
		frm.doc.kode_distributor_pengiriman=""
		frm.doc.pick_date=""
		frm.doc.expected_delivery=""
		frm.doc.suggest_truck_type=""
		frm.doc.strict=""
		frm.doc.estimate_volume=""
		frm.doc.goods_information=""
		frm.doc.notes=""
		frm.doc.accept_date=""
		frm.doc.driver=""
		frm.doc.driver_nama=""
		frm.doc.driver_phone=""
		frm.doc.truck=""
		frm.doc.truck_volume=""
		frm.doc.truck_type=""
		frm.doc.truck_lambung=""
		frm.doc.job_order_history=""
	}
});
