
# The Boston Public Schools Transportation Challenge
### Contributors Megan Horan, Ryan Chen, Victoria Thomson

[Boston Public Schools Transportation Challenge](http://bostonpublicschools.org/transportationchallenge)

## Abstract:
The problem our group chose to tackle was set forth by the Boston Public Schools, in an attempt to optimize school busing systems. This problem was interesting because it provided us with datasets that were accurate and easy to obtain, affording us the opportunity to obtain beneficial results for the lives of students and bus drivers. We chose to focus on the location of bus yards in relation to schools, and to get some useful numbers about the different average distances between students. While these two analyses do not optimize a bus route as a whole, they serve to bolster further research by providing useful representations of data for an ideal bus route. 

## Goals:
1. Optimize bus yard locations based of the congregations of schools, minimizing the distance between each bus yard and all the schools it services
2. Find the average distance between students using different metrics to group the students

## Datasets used:
[buses dataset](http://datamechanics.io/data/_bps_transportation_challenge/buses.json)
[simulated students dataset json](http://datamechanics.io/data/_bps_transportation_challenge/students.json)
[schools dataset geojson](http://datamechanics.io/data/_bps_transportation_challenge/schools.json)
[Provided by Datamechanics.io repository](http://datamechanics.io/?prefix=_bps_transportation_challenge/)

## Optimization Algorithms

#### Bus yard optimization:
In order to analyze the bus yard locations, we used the **k-means algorithm** to find the hubs of where schools are located. We wanted to cluster the schools because if we could see where the schools were congregating, we would find out the locations for the bus yards that best served the largest amount of schools. If the bus yards were placed in their ideal areas, where they would be serving the most schools they possibly could, then the total travel time from start to finish for those buses would decrease drastically and shave off any unnecessary travel time. We then tried all the different means to find the **ideal number of k-values**, which would be a k-value after which adding more means would not decrease the cost significantly This graph below is the representation of data collected: on the x-axis is k values and on the y-axis is the average cost between all the schools and their respective means.

![alt-sytle](https://github.com/ryanscodebay/course-2017-spr-proj/blob/master/mrhoran_rnchen_vthomson/visualization/int_graph/kmeans_cost_image.png "kmeans cost")

Our k-means algorithm then returns a dataset that has the location of the bus yards and all the closest schools it would service. This graph below shows the visualization of that: the pink circles show where the ideal bus yard, where the radius of each circle is a representation of how many schools it would pick up students for. The blue circles are where the current bus yards are and how many schools they service, using the same function as the pink circles to calculate which schools are closest to which bus yard given the current configuration of bus yards.

![alt-sytle](https://github.com/ryanscodebay/course-2017-spr-proj/blob/master/mrhoran_rnchen_vthomson/visualization/kmeans-visual/bus_yard_image.png "bus_yard visual")

#### Student Distance Averages:

The next analysis we did was to find some meaningful statistics about where students are located, calculating the average distance using a few different metrics.We then found two different distance averaging metrics, with one grouping averaging the distance of the closest 10 students per student, and one grouping averaging the distance between students in a .5 mile radius. We found the distance using vincenty distance, as we did in the k-means algorithm. We found that the average distance between the 10 closest students is 0.439337627979 miles and the average distance between students within a 0.5 mile radius is 0.4736018743886687. This data would be useful for buses to see how far they would have to travel between stops on average, in order for them to envision timing. Also, it would show us where to place optimal bus stops for students, and the data is malleable to group students by different end and start times for schools. 

## Conclusions:

We hope that in the future, other groups or interested parties will take this data and build from it to come closer to optimizing the bus routes. From the k-means algorithm, the bus yards give us an idea of where to have buses begin and end their journey to minimize the distance buses have to travel on their journey. Our hope is that someone will factor in these yards to begin and find a route based off these ideal bus yard starting locations. Also, anyone considering the time it takes to pick up students in a given radius can use the average distances we found in their calculations to see how long it might take for a bus to pick up x many students in a given area or on an optimized route they found. Overall we were happy that the data was so readily accessible so that we could obtain fecund results to further future research. One can see that there are many paths that groups can go down in hopes of optimizing the bus routes in a way that builds off of the data.

## To run the project:

### Installing Dependencies

dml
provr
rtree (requires libspatialindex; see below)
[libspatialindex] (https://libspatialindex.github.io/) * MAKE SURE YOU HAVE MONGOD RUNNING FIRST AND AUTH'D *

### To run the project:

#### To get the data:

busData.py

#### To run transformations:
1. python3 transformation_one_bus.py
  * finding the kmeans cost data and storing it in a csv
  * returning the ideal bus yards, their location, and the schools they service in the database
  * returning the current bus yards their location, and the schools they service in the database

2. python3 transformation_two_bus.py
  * finding the averages distance (miles) of students in a .5 mile radius
  * finding the averages distance (miles) of a student and the 10 closest students 

#### To run the visualizations:

1. go into the web_app folder
2. python 591_webvisual.py
3. go to http://127.0.0.1:5000/

