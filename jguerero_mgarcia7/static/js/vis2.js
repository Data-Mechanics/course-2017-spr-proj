queue()
	.defer(d3.json, "/other")
	.await(correlation);


function correlation(other) {
	var chart = new CanvasJS.Chart("chartContainer",
        {
          title:{
            text: "Import Cost Impact on Business",      
            fontFamily: "arial black",
            fontColor: "DarkSlateGrey"
          },
                            animationEnabled: true,
          axisX: {
            title:"Ease of Doing Business(1 = most friendly)",
            titleFontFamily: "arial"

          },
          axisY:{
            title: "Import cost per container",
            titleFontFamily: "arial",
            valueFormatString:"0 USD",
            titleFontSize: 12
          },

          data: [
          {        
            type: "scatter",  
            toolTipContent: "<span style='\"'color: {color};'\"'><strong>{name}</strong></span> <br/> <strong>Cost/ container</strong> {y} $<br/> <strong>Ease of Business</strong> {x} ",
            dataPoints: other
          }
          ]
		}
	)};

chart.render();