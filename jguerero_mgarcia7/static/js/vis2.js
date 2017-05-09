queue()
	.defer(d3.json, "/correlationjson")
	.await(correlation);

function correlation(correlationjson) {

	var id;
	$('.button').click( function () {
    	id = $(this).attr('id')

 		switch (id) {
 			case "io": handles = makegraph("io", correlationjson); break;
 			case "if": handles = makegraph("if", correlationjson); break;
 			case "fi": handles = makegraph("fi", correlationjson); break;
 			default: handles = makegraph("io", correlationjson);
 		}
	});
};

function makegraph(graph, correlationjson) {

	if (graph == 'io') {
		var chart = new CanvasJS.Chart("chartContainer",
	        {
	          title:{
	            text: "Income vs. Obesity 	(R2=-0.543)",
	            fontFamily: "Impact",
	            fontColor: "DarkSlateGrey"
	          },
	                            animationEnabled: true,
	          axisX: {
	            title:"Income",
	            titleFontFamily: "impact"

	          },
	          axisY:{
	            title: "Obesity",
	            titleFontFamily: "impact",
	            valueFormatString:"0",
	            titleFontSize: 12
	          },

	          data: [
	          {        
	            type: "scatter",  
	            toolTipContent: "<span style='\"'color: blue;'\"'><strong>{name}</strong></span> <br/> <strong>Cost/ container</strong> {y} $<br/> <strong>Ease of Business</strong> {x} ",
	            dataPoints: [

	            	{'x': 54314.80952380953, 'y': 36.54886978669214, 'name': 'East Boston'}, 
	            	{'x': 85375.09090909091, 'y': 30.81967213114754, 'name': 'Charlestown'}, 
	            	{'x': 47823.555555555555, 'y': 25.964934018957937, 'name': 'Fenway/Kenmore'}, 
	            	{'x': 32592.5625, 'y': 44.16196132354232, 'name': 'Roxbury'}, 
	            	{'x': 58933.03571428572, 'y': 37.69115933585785, 'name': 'Dorchester'}, 
	            	{'x': 82530.93103448275, 'y': 30.88863173855792, 'name': 'South Boston'}, 
	            	{'x': 84250.42857142857, 'y': 32.216808769792934, 'name': 'South End'}, 
	            	{'x': 52957.73333333333, 'y': 27.277934618059817, 'name': 'Allston/Brighton'}, 
	            	{'x': 86159.25, 'y': 33.72645660975181, 'name': 'Jamaica Plain'}, 
	            	{'x': 41743.42105263158, 'y': 46.81886421286949, 'name': 'Mattapan'}, 
	            	{'x': 71824.0, 'y': 36.75593036445233, 'name': 'Roslindale'}, 
	            	{'x': 88363.30769230769, 'y': 34.52132107023411, 'name': 'West Roxbury'}, 
	            	{'x': 108189.875, 'y': 28.853972090979013, 'name': 'Back Bay'}, 
	            	{'x': 66741.0, 'y': 40.302998310810814, 'name': 'Hyde Park'}, 
	            	{'x': 82163.6, 'y': 27.874859075535515, 'name': 'North End'}, 
	            	{'x': 98898.66666666667, 'y': 25.178784266984504, 'name': 'West End'}, 
	            	{'x': 115616.66666666667, 'y': 28.5689077113111, 'name': 'Beacon Hill'}, 
	            	{'x': 45199.5, 'y': 31.728166405470866, 'name': 'Mission Hill'}]
	          }
	          ]
			}
		)
	}

	else if (graph == 'if') {

		var chart = new CanvasJS.Chart("chartContainer",
	        {
	          title:{
	            text: "Income vs. Food Score 	(R2=-0.0243)",
	            fontFamily: "Impact",
	            fontColor: "DarkSlateGrey"
	          },
	                            animationEnabled: true,
	          axisX: {
	            title:"Income",
	            titleFontFamily: "impact"

	          },
	          axisY:{
	            title: "Food Score",
	            titleFontFamily: "impact",
	            valueFormatString:"0",
	            titleFontSize: 12
	          },

	          data: [
	          {        
	            type: "scatter",  
	            toolTipContent: "<span style='\"'color: blue;'\"'><strong>{name}</strong></span> <br/> <strong>Cost/ container</strong> {y} $<br/> <strong>Ease of Business</strong> {x} ",
	            dataPoints: [

	            	{'x': 54314.80952380953, 'y': 76.14259946010529, 'name': 'East Boston'}, 
	            	{'x': 85375.09090909091, 'y': 83.442020082782, 'name': 'Charlestown'}, 
	            	{'x': 47823.555555555555, 'y': 95.94161605191823, 'name': 'Fenway/Kenmore'}, 
	            	{'x': 32592.5625, 'y': 48.52487513935597, 'name': 'Roxbury'},
	            	{'x': 58933.03571428572, 'y': 61.93419515814582, 'name': 'Dorchester'}, 
	            	{'x': 82530.93103448275, 'y': 56.927358025919645, 'name': 'South Boston'}, 
	            	{'x': 84250.42857142857, 'y': 94.98193445639015, 'name': 'South End'}, 
	            	{'x': 52957.73333333333, 'y': 46.77972559500286, 'name': 'Allston/Brighton'}, 
	            	{'x': 86159.25, 'y': 58.96651128784938, 'name': 'Jamaica Plain'},
	            	{'x': 41743.42105263158, 'y': 49.58758406463348, 'name': 'Mattapan'}, 
	            	{'x': 71824.0, 'y': 43.50011864146607, 'name': 'Roslindale'}, 
	            	{'x': 88363.30769230769, 'y': 0.0, 'name': 'West Roxbury'}, 
	            	{'x': 108189.875, 'y': 90.33737601854506, 'name': 'Back Bay'}, 
	            	{'x': 66741.0, 'y': 28.203840209352876, 'name': 'Hyde Park'}, 
	            	{'x': 82163.6, 'y': 90.72500370036316, 'name': 'North End'}, 
	            	{'x': 98898.66666666667, 'y': 74.65258472422494, 'name': 'West End'}, 
	            	{'x': 115616.66666666667, 'y': 50.88780285305418, 'name': 'Beacon Hill'}, 
	            	{'x': 45199.5, 'y': 87.9067969700475, 'name': 'Mission Hill'}]
	          }
	          ]
			}
		)

	}

	else if (graph == 'fi') {

		var chart = new CanvasJS.Chart("chartContainer",
	        {
	          title:{
	            text: "Food Score vs. Obesity	(R2=-0.466)",
	            fontFamily: "Impact",
	            fontColor: "DarkSlateGrey"
	          },
	                            animationEnabled: true,
	          axisX: {
	            title:"Income",
	            titleFontFamily: "impact"

	          },
	          axisY:{
	            title: "Obesity",
	            titleFontFamily: "impact",
	            valueFormatString:"0",
	            titleFontSize: 12
	          },

	          data: [
	          {        
	            type: "scatter",  
	            toolTipContent: "<span style='\"'color: blue;'\"'><strong>{name}</strong></span> <br/> <strong>Cost/ container</strong> {y} $<br/> <strong>Ease of Business</strong> {x} ",
	            dataPoints: [

	            	{'x': 76.14259946010529, 'y': 36.54886978669214, 'name': 'East Boston'},
	            	{'x': 83.442020082782, 'y': 30.81967213114754, 'name': 'Charlestown'}, 
	            	{'x': 95.94161605191823, 'y': 25.964934018957937, 'name': 'Fenway/Kenmore'},
	            	{'x': 48.52487513935597, 'y': 44.16196132354232, 'name': 'Roxbury'},
	            	{'x': 61.93419515814582, 'y': 37.69115933585785, 'name': 'Dorchester'},
	            	{'x': 56.927358025919645, 'y': 30.88863173855792, 'name': 'South Boston'},
	            	{'x': 94.98193445639015, 'y': 32.216808769792934, 'name': 'South End'},
	            	{'x': 46.77972559500286, 'y': 27.277934618059817, 'name': 'Allston/Brighton'},
	            	{'x': 58.96651128784938, 'y': 33.72645660975181, 'name': 'Jamaica Plain'},
	            	{'x': 49.58758406463348, 'y': 46.81886421286949, 'name': 'Mattapan'},
	            	{'x': 43.50011864146607, 'y': 36.75593036445233, 'name': 'Roslindale'},
	            	{'x': 0.0, 'y': 34.52132107023411, 'name': 'West Roxbury'},
	            	{'x': 90.33737601854506, 'y': 28.853972090979013, 'name': 'Back Bay'},
	            	{'x': 28.203840209352876, 'y': 40.302998310810814, 'name': 'Hyde Park'},
	            	{'x': 90.72500370036316, 'y': 27.874859075535515, 'name': 'North End'},
	            	{'x': 74.65258472422494, 'y': 25.178784266984504, 'name': 'West End'},
	            	{'x': 50.88780285305418, 'y': 28.5689077113111, 'name': 'Beacon Hill'},
	            	{'x': 87.9067969700475, 'y': 31.728166405470866, 'name': 'Mission Hill'}]
	          }
	          ]
			}
		)

	}

	
chart.render();

};

