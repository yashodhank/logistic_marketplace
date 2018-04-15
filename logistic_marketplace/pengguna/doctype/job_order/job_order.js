// Copyright (c) 2017, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

var mapScript = document.createElement("script")
mapScript.type = "text/javascript"
mapScript.text = "function initMap(){\n    var map = new google.maps.Map(document.getElementById('map'), {\n      zoom: 9,\n      center: {lat: -6.211712, lng: 106.844781},\n      mapTypeId: 'terrain'\n    });\n    console.log('map loaded')\n    console.log(map)\n}"
document.head.appendChild(mapScript)

var script = document.createElement("script");
script.type = "text/javascript";
script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAkkWJrWJbouVzo7WpHd_-mlPJogyKSffM&callback=initMap";
script.defer = true
script.async = true
script.onload = function(){
	console.log("Google maps Loaded");
};
document.head.appendChild(script);

var hasOwnProperty = Object.prototype.hasOwnProperty;

function isEmpty(obj) {

    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;

    // If it isn't an object at this point
    // it is empty, but it can't be anything *but* empty
    // Is it empty?  Depends on your application.
    if (typeof obj !== "object") return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}


function refreshMap(jou) {
	console.log('refreshMap')
	if (isEmpty(jou)) {
		cur_frm.set_value('track_history','Belum ada perubahan lokasi')
	} else {
		var jobOrderUpdate = jou.message
		var lastIndex = jobOrderUpdate.length - 1
		getRoute(jobOrderUpdate,jobOrderUpdate[lastIndex].name,jobOrderUpdate[0].name,cur_frm.doc.driver)
	}
	
}

function add_marker(map, point, note, icon_id) {
	var icon = {
	    url: "http://system.digitruk.com//files/loc_"+icon_id+".png",
	    scaledSize: new google.maps.Size(30, 27.6),
	    origin: new google.maps.Point(0,0),
	    anchor: new google.maps.Point(10, 10)
	}
	if (icon_id == '-') {
		icon = {
		    url: "http://system.digitruk.com//files/loc.png",
		    scaledSize: new google.maps.Size(30, 27.6),
		    origin: new google.maps.Point(0,0),
		    anchor: new google.maps.Point(10, 10)
		}
	}
	if (icon_id == '6') {
		icon = {
		    url: "http://system.digitruk.com//files/loc_6.png",
		    scaledSize: new google.maps.Size(24, 42.9),
		    origin: new google.maps.Point(0,0),
		    anchor: new google.maps.Point(10, 40)
		}
	}
	
    var marker = new google.maps.Marker({
    	map: map, 
    	icon : icon,
    	position: point, 
    	clickable: true,
    	draggable: false,
    	animation: google.maps.Animation.DROP
    })
    marker.note = note
    google.maps.event.addListener(marker, 'click', function() {
        var info_window = new google.maps.InfoWindow({content: marker.note})
        info_window.open(map, marker);
    })
    return marker;
}

function getRoute(jobOrderUpdate,startjou,endjou,driver) {
	console.log('get route')
	console.log(startjou + ' ' + endjou + ' ' + driver)
	frappe.call({
		    method:"logistic_marketplace.api.get_route",
		    args: {
		        startjou:startjou,
		        endjou:endjou,
		        driver:driver
		    }, 
		    callback: function(r) { 
		    	$('#loading-indicator').html('')
		    	console.log(jobOrderUpdate)
		    	var map = new google.maps.Map(document.getElementById('map'), {
			      zoom: 9,
			      center: {lat: parseFloat(jobOrderUpdate[0].lat), lng: parseFloat(jobOrderUpdate[0].lo)},
			      mapTypeId: 'terrain'
			    })
				console.log('refresh map')
				console.log(map)

				//plot marker
				for (var i = 0;i<jobOrderUpdate.length;i++) {
					var icon_id = jobOrderUpdate[i].status.charAt(0)
					add_marker(map, new google.maps.LatLng(parseFloat(jobOrderUpdate[i].lat), parseFloat(jobOrderUpdate[i].lo)), '<strong>' + jobOrderUpdate[i].status + '</strong><br>' + 'Perubahan dilakukan pada ' + jobOrderUpdate[i].creation, icon_id)
				}
				
				if (isEmpty(r)) {

				} else {
					//plot track route history
					var routeCoord = []
					route = r.message
					for (var i=0;i<route.length;i++) {
						routeCoord.push({
							lat: parseFloat(route[i].lat),
							lng: parseFloat(route[i].lo)
						})
					}

					console.log(routeCoord)

			        var routePath = new google.maps.Polyline({
			          path: routeCoord,
			          geodesic: true,
			          strokeColor: '#8FAE35',
			          strokeOpacity: 1.0,
			          strokeWeight: 3
			        });

			        routePath.setMap(map);
				}
				$('#map').css('height','500px')
		    }
		})
}

frappe.ui.form.on('Job Order', {
	refresh: function(frm) {
		cur_frm.set_value('track_history','<div id="loading-indicator">Loading...</div><div id="map"></div>')
		current_name = (frm.docname)
		driver = frm.doc.driver
		frappe.call({
		    method:"frappe.client.get_list",
		    args: {
		        doctype:"Job Order Update",
		        filters: {
		            job_order:current_name
		        },
		        fields:["name","creation","lat","lo","status"]
		    }, 
		    callback: function(r) { 
		    	refreshMap(r)
		    }
		})
	},
	onload:function(frm) {
		
	}
});
