queue()
	.defer(d3.json, "/nbjson")
	.await(makeGraphs);

function makeGraphs(error, nbjson) {

	var minimum = 0, maximum = 100;
	var minimumColor = "#BFD3E6", maximumColor = "#88419D";
	var color = d3.scale.linear().domain([minimum, maximum]).range([minimumColor, maximumColor]);

	var width = 1000, height = 600;
	var albersProjection = d3.geo.albers()
	  .scale( 190000 )
	  .rotate( [71.057,0] )
	  .center( [0, 42.313] );

	var path = d3.geo.path().projection(albersProjection);
	var svg = d3.select("body").append("svg").attr("width", width).attr("height", height);

	var counties = nbjson['features'];

	//counties
    svg.append("g")
    .attr("class", "Neighborhood")
    .selectAll("path")
    .data(nbjson['features'])
	.enter()
    .append("path")
    .attr("d", path)
    .style("fill", function(d) {
        return color(d['properties']['score']);
    });


    var w = 140, h = 300;

	var key = d3.select("body").append("svg").attr("id", "key").attr("width", w).attr("height", h);

	var legend = key.append("defs").append("svg:linearGradient").attr("id", "gradient").attr("x1", "100%").attr("y1", "0%").attr("x2", "100%").attr("y2", "100%").attr("spreadMethod", "pad");

	legend.append("stop").attr("offset", "0%").attr("stop-color", maximumColor).attr("stop-opacity", 1);

	legend.append("stop").attr("offset", "100%").attr("stop-color", minimumColor).attr("stop-opacity", 1);

	key.append("rect").attr("width", w - 100).attr("height", h - 100).style("fill", "url(#gradient)").attr("transform", "translate(0,10)");

	var y = d3.scale.linear().range([200, 0]).domain([minimum, maximum]);

	var yAxis = d3.svg.axis().scale(y).orient("right");

	key.append("g").attr("class", "y axis").attr("transform", "translate(42,10)").call(yAxis).append("text").attr("transform", "rotate(-90)").attr("y", 30).attr("dy", ".71em").style("text-anchor", "end").text("Score");

};