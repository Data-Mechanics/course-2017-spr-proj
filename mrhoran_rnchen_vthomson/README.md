
# The Boston Public Schools Transportation Challenge
### Contributors Megan Horan, Ryan Chen, Victoria Thomson

[Boston Public Schools Transportation Challenge](http://bostonpublicschools.org/transportationchallenge)

## Abstract:
The problem our group chose to tackle was set forth by the Boston Public Schools, in an attempt to optimize school busing systems. This problem was interesting because it provided us with datasets that were accurate and easy to obtain, affording us the opportunity to obtain beneficial results for the lives of students and bus drivers. We chose to focus on the location of bus yards in relation to schools, and to get some useful numbers about the different average distances between students. While these two analyses do not optimize a bus route as a whole, they serve to bolster further research by providing useful representations of data for an ideal bus route. 

## Goals:
1. Optimize bus yard locations based of the congregations of schools, minimizing the distance between each bus yard and all the schools it services
2. Find the average distance between students using different metrics to group the students

## Optimization Algorithms

#### Bus yard optimization:
In order to analyze the bus yard locations, we used the **k-means algorithm** to find the hubs of where schools are located. We wanted to cluster the schools because if we could see where the schools were congregating, we would find out the locations for the bus yards that best served the largest amount of schools. If the bus yards were placed in their ideal areas, where they would be serving the most schools they possibly could, then the total travel time from start to finish for those buses would decrease drastically and shave off any unnecessary travel time. We then tried all the different means to find the **ideal number of k-values**, which would be a k-value after which adding more means would not decrease the cost significantly This graph below is the representation of data collected: on the x-axis is k values and on the y-axis is the average cost between all the schools and their respective means.

![alt-sytle](https://github.com/ryanscodebay/course-2017-spr-proj/blob/master/mrhoran_rnchen_vthomson/visualization/kmeans-visual/bus_yard_image.png "kmeans cost")

