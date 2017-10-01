var map;
var bounds;
var appgg;
var loaded_data=[];
var loaded=0;
function initMap(){
	appgg.render();
	bounds = new google.maps.LatLngBounds();
	var mapOptions = {
						mapTypeId: 'roadmap',
						center: {lat:-7.3111249,lng:112.7279283},
						zoom: 10
					};
				
	// Display a map on the page
	map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
	map.setTilt(45);
	loaded=1;
}
frappe.pages['job-order-last-updat'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Order Last Update Position',
		single_column: true
	});
	appgg = new MapLastUpdate(wrapper);
}

MapLastUpdate = Class.extend({
	init: function(wrapper) {
		var me = this;
		$('<style>#map_wrapper {height: 500px;}#map_canvas {width: 100%;height: 100%;}</style><script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCUG1BaoBIpZIap-nr9jSpJOsEjDOQIPXo&callback=initMap"></script><div id="map_wrapper"><div class="mapping" id="map_canvas"></div></div>').appendTo($(wrapper).find(".layout-main"))
		// 0 setTimeout hack - this gives time for canvas to get width and height
		setTimeout(function() {
			me.setup(wrapper);
			me.get_data();
		}, 0);
	},
	setup: function(wrapper) {
		var me = this;
		

		principle_ro=0
		if (frappe.session.principle){
			principle_ro=1
		}
		vendor_ro=0
		if (frappe.session.principle){
			vendor_ro=1
		}
		this.elements = {
			layout: $(wrapper).find(".layout-main"),
			principle: wrapper.page.add_field({
			"fieldname":"principle",
			"label": __("Principle"),
			"fieldtype": "Link",
			"options": "Principle",
			"default": frappe.defaults.get_user_default("principle"),
			"read_only":principle_ro
			}),
			vendor: wrapper.page.add_field({
			"fieldname":"vendor",
			"label": __("Vendor"),
			"fieldtype": "Link",
			"options": "Vendor",
			"default": frappe.defaults.get_user_default("vendor"),
			"read_only":vendor_ro
			}),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh"),
				function() { me.get_data(); }, "fa fa-refresh")
		};
				
	},
	get_data: function(btn) {
		if (loaded==1){
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
					loaded_data = r.message;
					me.render();
				}
			}
		});
		}
	},
	render: function() {
		if (loaded==1){
		var me = this;
		data = loaded_data;
		markers = [];
		infoWindowContent = [];
		for (var row in data){
			info = data[row];
			markers.push([info.job_order,info.lat,info.lo]);
			infoWindowContent.push(['<div class="info_content">' +
				'<h3>'+ info.job_order+'</h3>' +
				'<p>Principle : '+info.principle+'</p>'+
				'<p>Vendor : '+info.vendor+'</p></div>']);
		}
			
		// Display multiple markers on a map
		var infoWindow = new google.maps.InfoWindow(), marker, i;
   
		// Loop through our array of markers & place each one on the map  
		for( i = 0; i < markers.length; i++ ) {
			var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
			bounds.extend(position);
			marker = new google.maps.Marker({
				position: position,
				map: map,
				title: markers[i][0]
			});
	   
			// Allow each marker to have an info window	
			google.maps.event.addListener(marker, 'click', (function(marker, i) {
				return function() {
					infoWindow.setContent(infoWindowContent[i][0]);
					infoWindow.open(map, marker);
				}
			})(marker, i));
				// Automatically center the map fitting all markers on the screen
			map.fitBounds(bounds);
		}
			// Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
		var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
			this.setZoom(7);
			google.maps.event.removeListener(boundsListener);
		});
	}}
});
