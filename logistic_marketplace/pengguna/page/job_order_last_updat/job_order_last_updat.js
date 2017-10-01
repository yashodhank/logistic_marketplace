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

		var script = document.createElement('script');
		script.src = "//maps.googleapis.com/maps/api/js?sensor=false";
		document.body.appendChild(script);
		var themap;
	    var bounds = new google.maps.LatLngBounds();
	    var mapOptions = {
	    				    mapTypeId: 'roadmap',
							center: {lat:-7.3111249,lng:112.7279283},
							zoom: 10
		    			};
                    
    	// Display a map on the page
	    themap = new google.maps.Map($(wrapper).find(".layout-main"), mapOptions);
    	themap.setTilt(45);

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
				function() { me.get_data(); }, "fa fa-refresh"),
			map:themap
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
	render: function() {
		var me = this;
		data = me.options.data;
		markers = [];
		map=me.elements.map;
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
	}
});
