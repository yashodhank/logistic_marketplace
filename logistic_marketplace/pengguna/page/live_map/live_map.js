var map;
var bounds;
var appgg;
var loaded_data=[];
var loaded=0;
var global_wrapper;
var current_markers=[];
var timer = setInterval(function(){me.get_data();},10000)

function initMap(){
	
	bounds = new google.maps.LatLngBounds();
	var mapOptions = {
						mapTypeId: 'roadmap',
						center: {lat:-7.3111249,lng:112.7279283},
						zoom: 5
					};
				
	// Display a map on the page
	map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
	map.setTilt(45);
	loaded=1;
	appgg.setup(global_wrapper);
	appgg.get_data();
}
frappe.pages['live-map'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Live Map',
		single_column: true
	});
	global_wrapper=wrapper;
	appgg = new LiveMap(wrapper);
}

LiveMap = Class.extend({
	init: function(wrapper) {
		var me = this;
		$('<style>#map_wrapper {height: 500px;}#map_canvas {width: 100%;height:75%;}</style><script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCUG1BaoBIpZIap-nr9jSpJOsEjDOQIPXo&callback=initMap"></script><div id="map_wrapper"><div class="mapping" id="map_canvas"></div></div>').appendTo($(wrapper).find(".layout-main"))
		// 0 setTimeout hack - this gives time for canvas to get width and height
		// setTimeout(function() {
		// 	me.setup(wrapper);
		// 	me.get_data();
		// }, 0);
	},
	setup: function(wrapper) {
		var me = this;
		

		principle_ro=0
		if (frappe.session.principle){
			principle_ro=1
		}
		vendor_ro=0
		if (frappe.session.vendor){
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
			}).$wrapper.find("input"),
			vendor: wrapper.page.add_field({
			"fieldname":"vendor",
			"label": __("Vendor"),
			"fieldtype": "Link",
			"options": "Vendor",
			"default": frappe.defaults.get_user_default("vendor"),
			"read_only":vendor_ro
			}).$wrapper.find("input"),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh"),
				function() { 
					me.get_data();
			}, "fa fa-refresh")
		};
		if (vendor_ro==1){
			this.elements.driver=wrapper.page.add_field({
			"fieldname":"driver",
			"label": __("Driver"),
			"fieldtype": "Link",
			"options": "Driver",
			}).$wrapper.find("input")
		}
		// this.elements.refresh_btn.on("click", function() {
		// 	me.get_data(this);
		// });
	},
	get_data: function(btn) {
		if (loaded==1){
		var me = this;
		var dd="All";
		var pp=this.elements.principle.val();
		var vv=this.elements.vendor.val();
		if ("driver" in this.elements){
			dd=this.elements.driver.val();
		}
		if (pp==null || pp==""){pp="All"}
		if (vv==null || vv==""){vv="All"}
		if (dd==null || dd==""){dd="All"}
		frappe.call({
			method: "logistic_marketplace.pengguna.page.live_map.live_map.get_position",
			args: {
					principle: pp,
					vendor: vv,
					driver:dd
			},
			btn: btn,
			callback: function(r) {
				if(!r.exc) {
					if (r.message=="No Data"){
						loaded_data=[];
					}else{
						loaded_data = r.message;
					}
					
					
				}else{
					loaded_data=[];
				}
				me.render();
			}
		});
		}
	},
	render: function() {
		if (loaded==1){
		var me = this;
		var data = loaded_data;
		for( i = 0; i < current_markers.length; i++ ) {
			current_markers[i].setMap(null);
		}
		current_markers=[];
		if (loaded_data.length>0){
		var markers = [];
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
			current_markers.push(marker);
		}
			// Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
		var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
			this.setZoom(5);
			google.maps.event.removeListener(boundsListener);
		});
	}
	}}
});
