const width = 1800;
const height = 1020;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

const projection = d3.geoMercator().center([-71.05, 42.3122]).scale(240000).translate([width / 2, height / 2]);

const geoPath = d3.geoPath().projection(projection);

svg.append('rect')
  .attr('class', 'background')
  .attr('width', width)
  .attr('height', height);

var g = svg.append('g');

var mapLayer = g.append('g')
  .classed('map-layer', true);

var hospitalLayer = g.append('g')
    .classed('hospital-layer', true);

var crimeLayer = g.append('g')
    .classed('crime-layer', true);

d3.json("data/boston.geojson", function(error, boston) {
  if (error) return console.error(error);

  mapLayer.selectAll('path')
      .data(boston.features)
      .enter().append('path')
      .attr('d', geoPath)
      .style('fill', "#fff")
      .style("opacity", "0.8");
});

d3.json("data/crimes.json", function (error, crimes) {
    if (error) return console.error(error);

    var data = [];

    for (var i = 0; i < crimes.length; i++) {
        data.push([crimes[i].long, crimes[i].lat])
    }

    crimeLayer.selectAll('circle')
        .data(data).enter()
        .append('circle')
        .attr('cx', function (d) {return projection(d)[0];})
        .attr('cy', function (d) {return projection(d)[1];})
        .attr('r', "1px")
        .attr('fill', 'blue')
        .attr('opacity', '0.5');



    /*
    hospitalLayer.selectAll('circle')
        .data(data).enter()
        .append('circle')
        .attr('cx', function (d) {return projection(d)[0];})
        .attr('cy', function (d) {return projection(d)[1];})
        .attr('name', function(d) {return d[3];})
        .attr('sqft', function(d) {return d[2];})
        .attr('bookings', 0)
        .attr('r', "5px")
        .attr('fill', 'red')
        .style("opacity", "1.0");
        */
});

document.getElementById('num2').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['2']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num3').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['3']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num4').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['4']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num5').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['5']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num6').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['6']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num7').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['7']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num8').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['8']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num9').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['9']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};

document.getElementById('num10').onclick = function () {
    d3.json("data/kmeans.json", function (error, means) {
        if (error) return console.error(error);

        hospitalLayer.selectAll('circle').remove();

        hospitalLayer.selectAll('circle')
            .data(means['10']).enter()
            .append('circle')
            .attr('cx', function (d) {return projection(d)[0];})
            .attr('cy', function (d) {return projection(d)[1];})
            .attr('r', "5px")
            .attr('fill', 'red')
            .style("opacity", "1.0");
    });
};
