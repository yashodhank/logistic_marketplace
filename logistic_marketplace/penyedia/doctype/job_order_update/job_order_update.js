// Copyright (c) 2017, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order Update', {
	refresh: function(frm) {
		var html="";
		var attachment = cur_frm.attachments.get_attachments();
		//alert(JSON.stringify(attachment));
		for (var i=0;i<attachment.length;i++){
			html=html+'<img src="'+attachment[i].file_url+'" style="padding-right:20px;"/>';
		}
		frm.set_value("image_list",html);
		//frm.doc.image_list=html;
		//alert(html);
		//$.each(frm.doc.job_order_update_images, function(i,d){
		//	html=html+"<img src='"+d.file+"' />";
		//});
	}
});
cur_frm.add_fetch("job_order", "principle", "principle");
