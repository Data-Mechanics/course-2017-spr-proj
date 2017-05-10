// js code to draw map by Leaflet framework

// settings of map
var mymap = L.map('mapid').setView([42.3201, -71.067], 11); // boston coordinates as center, default zoom level 11
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	maxZoom: 18,
	id: 'mapbox.streets-satellite', 
	accessToken: 'pk.eyJ1IjoiYnVjczU5MSIsImEiOiJjajF6ZDF4YjcwMDk4MzNvNTI5YmE0c2J3In0.XdH1j3yxDVvJhwRUuDD_KA'
}).addTo(mymap);

// orange circle marker setting
var geojsonMarkerOptionsOrange = {
	radius: 5,
	fillColor: "#ff7800",
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.6
};

// blue circle marker setting
var geojsonMarkerOptionsBlue = {
	radius: 5,
	fillColor: "#3366FF",
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.6
};

// yellow circle marker setting
var geojsonMarkerOptionsYellow = {
	radius: 5,
	fillColor: "#FFFF33",
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.6
};

// draw circle markers from geoJSON file
L.geoJSON(finalscore_json, {
	pointToLayer: function (feature, latlng) {
		// console.log(feature['properties']['overall score']);
		var circle;
		if (feature['properties']['overall score'] > 0.8) { //score > 0.8, use orange circle
			var circle = L.circleMarker(latlng, geojsonMarkerOptionsOrange);
			console.log('1');
		} else if (feature['properties']['overall score'] > 0.5 && feature['properties']['overall score'] < 0.8){	// score > 0.5 and < 0.8, use blue circle
			var circle = L.circleMarker(latlng, geojsonMarkerOptionsBlue);
			console.log('2');
		} else{ // score < 0.5, use yellow circle
			var circle = L.circleMarker(latlng, geojsonMarkerOptionsYellow);
		}

		// circle marker popup information
		circle.bindPopup("Name: " + feature['properties']['name'] + "<hr>" + "Overall Score: " + feature['properties']['overall score'] + "<hr>" + "URL: " + "<a target=\"_blank\" href=\"" + feature['properties']['url'] +"\">Explore It!</a>").openPopup();
		return circle;
	}
}).addTo(mymap);