<!DOCTYPE html>

<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=1024, user-scalable=no">
    <style>
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0;}
      #map{ height: 100% }
    
    </style>
  
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5.1/leaflet.css" />

<div id="map"></div>
<script src="http://d3js.org/d3.v3.js"></script>

<script src="http://cdn.leafletjs.com/leaflet-0.5.1/leaflet.js"></script>
<script src="https://raw.github.com/mbostock/d3/5348d911938a0d1fdf43d7c86befbd908e431204/lib/colorbrewer/colorbrewer.js"></script>
<script src="https://raw.github.com/Caligatio/jsSHA/release-1.42/src/sha1.js"></script>
<script src="https://raw.github.com/imbcmdth/RTree/master/src/rtree.js"></script>
<script>

var m = L.map("map").setView([42.3504, -71.104],9);

//make the map


L.tileLayer("http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg",{minZoom:4,maxZoom:12,attribution:'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'}).addTo(m);
	
//add a tileset	

var pts = L.layerGroup().addTo(m);

function Quadtree(points){
    points = points || [];
    var p=points;
    var rTree = new RTree();
     p.forEach(function(v,i){
         rTree.insert(
             {x:v[0],y:v[1],w:0,h:0},v
         );
         });
    this.add = function(pts){
        p = p.concat(pts);

       pts.forEach(function(v,i){
         rTree.insert(
             {x:v[0],y:v[1],w:0,h:0},v
         );
         });
    };
    this.bbox=function(blat1,blng1,blat2,blng2){
        if(!blat1){
            return p;
        }
        return rTree.search({x:blat1,y:blng1,w:(blat2-blat1),h:(blng2-blng1)});
    };
}

var qt, bbox;

function morePoints(lat,lng){
    //compute random points
    var randomLat = d3.random.normal(lat, .15),
    randomLng = d3.random.normal(lng, .5);
    var points = d3.range(600).map(function() { return [randomLat(), randomLng()]; });
    if(!qt){//if we don't have a quad tree make one
        qt = new Quadtree(points);
    }else{
        //else add it to the current
        qt.add(points);
    }
    redoBox(bbox);// update the map
}
function getHash(text){
    //this is very much overkill but to make sure the same random style goes in everytime
    var shaObj = new jsSHA(text, "TEXT");
    return parseInt(shaObj.getHash("SHA-1", "HEX").slice(0,10),16)%11;
}


function redoBox(p){
    p=p||[];//make sure p is defined
    pts.clearLayers();//clear the map
    bbox=p;//update the bbox
    qt.bbox.apply(qt,p).forEach(function(v){//do the query
         pts.addLayer(L.circleMarker(v,{stroke:false,fillOpacity:0.8,color:colorbrewer.Spectral[11][getHash(JSON.stringify(v))],clickable:false}));//turn it into a marker wiht a popup
    });
}

m.on("contextmenu",function(){redoBox()});//so you can right click to add to map

var AddButton= L.Control.extend({//creating the buttons
    options: {
        position: 'bottomleft'
    },
    onAdd: function (map) {
        // create the control container with a particular class name
        var div = L.DomUtil.create('div','bgroup');
        var addButton = L.DomUtil.create('button', 'addStuff',div);
        addButton.type="button";
        addButton.innerHTML="Add More Points";
        L.DomEvent.addListener(addButton,"click",function(){
            morePoints(map.getCenter().lat,map.getCenter().lng);//make sure it's where you currently are.
            });
        var allButton = L.DomUtil.create('button', 'allStuff',div);
        allButton.type="button";
        allButton.innerHTML="ShowAll";
        L.DomEvent.addListener(allButton,"click",function(){
            redoBox();
            });
        return div;
    }
});
//add them to the map
m.addControl(new AddButton());

//this is the box selection thingy
var BoxSelect = L.Map.BoxZoom.extend({
	
	_onMouseUp: function (e) {
		this._pane.removeChild(this._box);
		this._container.style.cursor = '';

		L.DomUtil.enableTextSelection();

		L.DomEvent
		    .off(document, 'mousemove', this._onMouseMove)
		    .off(document, 'mouseup', this._onMouseUp);

		var map = this._map,
		    layerPoint = map.mouseEventToLayerPoint(e);

		if (this._startLayerPoint.equals(layerPoint)) { return; }

		var bounds = new L.LatLngBounds(
		        map.layerPointToLatLng(this._startLayerPoint),
		        map.layerPointToLatLng(layerPoint));

		map.fire("boxselectend", {
			boxSelectBounds: [bounds.getSouthWest().lat,bounds.getSouthWest().lng,bounds.getNorthEast().lat,bounds.getNorthEast().lng]
		});
	}
});
m.boxZoom.disable();//turn off  the defult behavior
var boxSelect = new BoxSelect(m);//new box select
boxSelect.enable();//add it
m.on("boxselectend",function(e){redoBox(e.boxSelectBounds);});//put the behavior in.
</script>
