frappe.pages['live-map'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Live Map',
		single_column: true
	});
}