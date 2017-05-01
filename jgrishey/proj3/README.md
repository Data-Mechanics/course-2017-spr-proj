# CS 591 L1 Project Report

Jacob Grishey
May 1st, 2017

# Introduction

This project is centered around the optimal placement of hospitals in the Boston area. This is an important topic to discuss when contemplating the infrastructure of a modern city. Hospitals need to be built where they can be best utilized. There are a myriad of factors that you can consider when deciding on the location of a new hospital. For this project, I decided to use the City of Boston's extensive crime data as the only factor.

The City of Boston's crime data was extremely easy to retrieve and work with. Using the Socrata API, I was able to retrieve all of the data. I used Python to do this. The crime data included the type of crime, date, and so on, but I only used the latitude and longitude since I was mainly focusing on location for this project.

I also used a GeoJSON file that consisted of the main hospitals in the Boston area. Using this, I was able to create a visualization of current hospitals in the area and their respective "loads," which I will describe later in this report.

The motivation to do this project is to provide the City of Boston with a better insight of where their hospitals and infrastructure should be placed throughout the city. While this is obviously not a multi-factored project that has gone through rigorous testing, it could still be a useful beginning tool.

# Hospital Loads Visualization

Using the crime data and the GeoJSON file of hospitals, I was able to create a visualization that provided "loads" for the respective hospitals. The load is defined as the number of crimes that are closest to each specific hospital, divided by the number of beds each hospital has. The number of beds was calculated by dividing the square footage of each hospital by 100.

Using Python, I attached each crime in the data to its closest hospital. After this, I calculated the loads for each hospital. Then, using D3.js and HTML, I drew a map of Boston and overlayed it with circles for each crime and each hospital. I also added a layer for displaying the load of each hospital.

![alt text](http://datamechanics.io/data/visualization.png)

If you click on one of the hospitals (red circles), then its corresponding load on the left will light up and the name of the hopsital will be displayed in the top right corner.

I thought that this was an interesting visualization to work with. Although you can't really tell if the hospitals are in the right places, it can still tell you how heavily these hospitals are hit with traffic.

# K Means Visualization

This visualization also uses the crime data, but does not use the GeoJSON file of hospitals. This visualization is based on the K-Means clustering algorithm.

Using Python, I used a K-Means library with the crime dataset in order to create clusters from 2 to 10 means. These means represent where the hospitals should be placed, since K-Means minimizes the average distance from a point to its respective mean. You can interpret the number of means as the number of hospitals you would like to build.

Using this resulting data, I was able to construct a visualization where you can view the placement of hospitals depending on the number of means that you select.

![alt text](http://datamechanics.io/data/visualization2.png)

As you can see in this screenshot, I have selected 10 means and it has given me the results as red circles on the map.

An interesting sidenote to this visualization: if you look at where the current hospitals are and where the K-Means algorithm places them, they line up decently. You can view this as possibly a good job by the City of Boston already in the placement of their hospitals.

# Conclusions and Future Work

This was an extremely interesting project to work on. Looking at real data and manipulating it to get results is a rewarding process and also eye-opening.

While conclusions can be drawn from this work, there are also numerous improvements that can be made to it as well. In the first visualization, there were no hospitals that were over their load, which is a good sign when it comes to the current placement of hospitals. In the second visualization, you could see that the means lined up relatively well with the current setup. One conclusion that you can draw from this is that Boston is doing a good job in the placement of their hospitals. However, even if they were not doing a good job, it is very costly to move and/or construct new hospitals.

Crime is not the only factor in the placement of hospitals. If you could combine this data along with population density information, it could become a more useful and insightful project. However, this is a good start.

Overall, I do not believe that the City of Boston would use this project, but it was a great introduction into the process of manipulating data and displaying the results. In the future, more complex and significant work would be even more fun and interesting to look at and work on.




