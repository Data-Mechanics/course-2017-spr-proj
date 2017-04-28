queue()
	.defer(d3.json, "/nbjson")
	.await(makeGraphs);

function makeGraphs(error, nbjson) {

	var formatNumber = d3.format(",d");

	var minimum = 0, maximum = 100;
	var minimumColor = "#BFD3E6", maximumColor = "#88419D";
	var color = d3.scale.linear().domain([minimum, maximum]).range([minimumColor, maximumColor]);

	var width = 1000, height = 1000;
	var albersProjection = d3.geo.albers()
	  .scale( 190000 )
	  .rotate( [71.057,0] )
	  .center( [0, 42.313] );

	var path = d3.geo.path().projection(albersProjection);
	var svg = d3.select("body").append("svg").attr("width", width).attr("height", height);

	var counties = nbjson['features'];


	/*

				item['FoodScore'] = nb_tups[3]
				item['avg_num_food'] = nb_tups[0]
				item['dist_closest'] = nb_tups[1]
				item['quality_food'] = nb_tups[2] 
	*/


	tip = d3.tip()
		.attr('class', 'd3-tip')
		.offset([150, 100])
		.direction('n')
		.html(function(d) {
		return d['properties']['name'] + "<br/>Avg # of Food Sources: " + d['properties']['avg_num_food'].toFixed(2) +
    "<br/>Avg Distance of Closest Food Source: " + d['properties']['dist_closest'].toFixed(2) + "<br/>Avg Quality of Food Sources: " + d['properties']['quality_food'].toFixed(2) +
    	"<br/>Overall Score: " + d['properties']['score'].toFixed(2)
	});

	svg.call(tip);

	//counties
    svg.append("g")
    .attr("class", "Neighborhood")
    .selectAll("path")
    .data(nbjson['features'])
	.enter()
    .append("path")
    .attr("d", path)
    .on('mouseover',tip.show)
    .on('mouseout', tip.hide)
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


	var formatNumber = d3.format(",d");

};