The Problem:

The main goal of our project is to use our datasets to provide a visualization on the living conditions of Boston based on the city’s 
crime reports and density of police stations.  
The plan we want to execute to achieve the visualization we want will involve the usage of the Google Maps API which will allow us to pin-point the 
specific locations of crime reports and the specific locations of police stations in city. 

Datasets we chose:

Crime Reports in Boston Between August 2015-Present
https://data.cityofboston.gov/resource/29yf-ye7n.json

Police Stations in Boston
https://data.cityofboston.gov/resource/pyxn-r3i2.json

We came up with an algorithm that is able to find the closet police station for every crime report in Boston, so we can determine which districts in Boston has
the highest crime rate. We calculated each distance between the crime incident and the location of the police station, and determined which police station had 
the closest distance to that crime report. We used this algorithm to come up with our bar graph chart to show the police stations that received the most crime
reports in their surrounding area. In order to run this algorithm, we ran nearestStation.py, which is located in our GitHub project directory.

How to view the visualizations:

	- First, retrieve all the data to visualize by running the following python files:

	crimerate.py
	policestation.py

	- Then, download the crimeMap.html and policeMap.html files onto your computer.

	- Next, obtain the Javascript API Key from Google Maps and place them in the html files on the following line at the section that says "YOUR_API_KEY"

	src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">

	- Finally, click on the html files to see the map with the markers indicated.