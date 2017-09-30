frappe.pages['job-order-last-updat'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Order Last Update Position',
		single_column: true
	});
	wrapper.map = new MapLastUpdate(wrapper);
}

MapLastUpdate = Class.extend({
	init: function(wrapper) {
		var me = this;
		// 0 setTimeout hack - this gives time for canvas to get width and height
		setTimeout(function() {
			me.setup(wrapper);
			me.get_data();
		}, 0);
	},
	setup: function(wrapper) {
		var me = this;

		this.elements = {
			layout: $(wrapper).find(".layout-main"),
			principle: wrapper.page.add_field({
			"fieldname":"principle",
			"label": __("Principle"),
			"fieldtype": "Link",
			"options": "Principle",
			"default": frappe.defaults.get_user_default("principle"),
			"read_ony":1,
			"reqd": 1
			}),
			vendor: wrapper.page.add_field({
			"fieldname":"vendor",
			"label": __("Vendor"),
			"fieldtype": "Link",
			"options": "Vendor",
			"default": frappe.defaults.get_user_default("vendor"),
			"reqd": 1
			}),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh"),
				function() { me.get_data(); }, "fa fa-refresh"),
		};
		
	},
	get_data: function(btn) {
		var me = this;
		frappe.call({
			method: "logistic_marketplace.pengguna.page.job_order_last_updat.job_order_last_update.get_job_order_data",
			args: {
				principle: this.options.principle,
				vendor: this.options.vendor
			},
			btn: btn,
			callback: function(r) {
				if(!r.exc) {
					me.options.data = r.message;
					me.render();
				}
			}
		});
	},
});
