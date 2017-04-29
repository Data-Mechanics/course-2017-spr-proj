queue()
	.defer(d3.json, "/nbjson")
	.await(makeGraphs);

layerInfo = {
        "score": {"title": "Food Accessibility Score", "range": [20,40,60,80,100], "colors": ["#54278f", "#756bb1", "#9e9ac8", "#bcbddc", "#cbc9e2"]}, // food score
        "obesity": {"title": "% Obesity", "range": [10,20,30,40,50], "colors": ["#005a32", "#238b45", "#41ab5d", "#74c476", "#a1d99b"]}, //obesity
        "quality_food": {"title": "Quality of Food Sources", "range": [0.2,0.4,0.6,0.8,1.0], "colors": ["#99000d", "#cb181d", "#ef3b2c", "#fb6a4a", "#fc9272"]}, // avg quality of food sources within walking distance
        "dist_closest": {"title": "Distance to Closest Food Source (km)", "range": [0.2,0.4,0.6,0.8,1.0], "colors": ["#084594", "#2171b5", "#4292c6", "#6baed6", "#6baed6"]}, // avg walking distance to closest
        "avg_num_food": {"title": "Average # of Food Sources within walking distance (<1km)", "range": [2.0,4.0,6.0,8.0,10.0], "colors": ["#7a0177", "#ae017e", "#dd3497", "#f768a1", "#fa9fb5"]} // avg # within walking distance
        };

function makeGraphs(error, nbjson) {

  // initialize the map
  var map = L.map('map').setView([42.35, -71.08], 13);

  // load a tile layer
	L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', 
	{
		attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
		maxZoom: 16,
		minZoom: 9
	}).addTo(map);

	// Default layer is the score visualization
	var handles = addInfoLayer("quality_food", nbjson, map);
	var currentLayer = handles[0];
	var currentLegend = handles[1];
	var currentInfoBox = handles[2];


	var id;
	$('.button').click( function () {
    	id = $(this).attr('id')

 		map.remove()

 		// initialize the map
  		map = L.map('map').setView([42.35, -71.08], 13);

  		// load a tile layer
		L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', 
		{
			attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
			maxZoom: 16,
			minZoom: 9
		}).addTo(map);


 		switch (id) {
 			case "score": handles = addInfoLayer("score", nbjson, map); break;
 			case "obesity": handles = addInfoLayer("obesity", nbjson, map); break;
 			case "quality_food": handles = addInfoLayer("quality_food", nbjson, map); break;
 			case "dist_closest": handles = addInfoLayer("dist_closest", nbjson, map); break;
 			case "avg_num_food": handles = addInfoLayer("avg_num_food", nbjson, map); break;
 			default: handles = addInfoLayer("avg_num_food", nbjson, map);
 		}

	});


};


function addInfoLayer(type,nbjson, map) {

	function getColor(d) {
	return d > layerInfo[type]["range"][3] ? layerInfo[type]["colors"][0] :
		   d > layerInfo[type]["range"][2]  ? layerInfo[type]["colors"][1] :
		   d > layerInfo[type]["range"][1]  ? layerInfo[type]["colors"][2] :
		   d > layerInfo[type]["range"][0]  ? layerInfo[type]["colors"][3] :
					  							layerInfo[type]["colors"][4];
	}

	function style(feature) {
		return {
			fillColor: getColor(feature.properties[type]),
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '1',
			fillOpacity: 0.4
		};
	}


	var infoLayer = L.geoJson(nbjson, {style:style});
	map.addLayer(infoLayer);

	var legend = L.control({position: 'bottomright'});

	legend.onAdd = function (map) {

		var div = L.DomUtil.create('div', 'info legend'),
			scores = layerInfo[type]["range"],
			labels = [];


		for (var i = 0; i < scores.length-1; i++) {
			div.innerHTML +=
				'<i style="background:' + getColor(scores[i+1]) + '"></i> ' +
				scores[i] + (scores[i + 1] ? '&ndash;' + scores[i + 1] + '<br>' : '&ndash;' + scores[scores.length-1]);
		}


		return div;
	};

	legend.addTo(map);

	function highlightFeature(e) {
	    var layer = e.target;

	    layer.setStyle({
	        weight: 5,
	        color: 'black',
	        dashArray: '',
	        fillOpacity: 0.7
	    });

	    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
	        layer.bringToFront();
	    }

	    info.update(layer.feature.properties);
	}

	function resetHighlight(e) {
    	geojson.resetStyle(e.target);
    	info.update();
	}

	var geojson;
	geojson = L.geoJson(nbjson);

	function zoomToFeature(e) {
    	map.fitBounds(e.target.getBounds());
	}


	function onEachFeature(feature, layer) {
	    layer.on({
	        mouseover: highlightFeature,
	        mouseout: resetHighlight,
	        click: zoomToFeature
	    });
	}

	geojson = L.geoJson(nbjson, {
	    style: style,
	    onEachFeature: onEachFeature
	}).addTo(map);



	var info = L.control();

	info.onAdd = function (map) {
	    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
	    this.update();
	    return this._div;
	};

	// method that we will use to update the control based on feature properties passed
	info.update = function (props) {
	    this._div.innerHTML = '<h4>' + layerInfo[type]["title"] + '</h4>' +  (props ?
	        '<b>' + props.name + '</b><br />' + props[type].toFixed(2) 
	        : 'Hover over a neighborhood');
	};

	info.addTo(map);

	return [infoLayer, legend, info];
}