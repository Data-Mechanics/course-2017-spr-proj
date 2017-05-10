# Introduction
The city of Boston provides sets of data for different city services. We chose to use datasets of different healthy locations and locations with high percentages of adult obesity. With this information, we aimed to determine if there was a correlation between obesity percentages and ease of access to a healthy location through public transportation. With our results, we determined whether these healthy programs and locations are present in neighborhoods with higher levels of obesity, which need them the most.

# Datasets
The healthy locations datasets we used and created are:
* Orchards [1]: Urban orchards and fruit trees in and around the city of Boston.
* Healthy Corner Stores [2]: Corner stores and bodegas participating in the Healthy Corner Stores Initiative sponsored by the Boston Public Health Commission and other community health center healthy corner store project locations.
* Community Culinary and Nutrition Programs [3]: Institutions and programs offering community-based culinary and nutrition education programming.
* Healthy Locations: Combines the three data sets above and only includes the type of healthy location and its longitude and latitude coordinates.

The following are the other datasets we gathered online:
* Obesity among Adults [4]: Provides a list of obesity percentages for each location
* MBTA Bus and Subway Stops [5]: List of subway and bus stops on the MBTA for each route
* Big Belly Locations [6]: Locations of all Big Belly trash receptacles in the city.

The following are all the datasets we created in the transformations:
* Closest MBTA (Control/Health/Obesity): A list of closest MBTA stops for each control, healthy, and obesity location. It is combined from MBTA routes, big belly locations, healthy locations, and obesity data.
* Health Obesity and Control Obesity: The closest healthy/control location for each obesity location. Modified from the previous dataset. Each data entry also contains the shortest travel time (in minutes) from the obese location to the healthy/control location.
* Results and Linear Regression Data: Linear regression data contains the RMSE, slope, MSE, and y-intercepts of the best fit linear regression for obesity percentage vs. minimum travel time. Results contain the same data but with control linear regression as well.

# Transformations Performed
## Healthy Locations
We aggregated all of the health programs, stores, and orchards into one dataset, with its type and location. We used select and project to clean and reformat the datasets. This generalizes the notion of a healthy location and allows us to have coordinates of healthy points.

## Closest MBTA stops to Control/Healthy/Obesity Locations
In order to prepare our data for calculating distance, we transformed each longitude and latitude coordinate into radians and stored it in the dataset as well as the rectangular coordinates we originally had. This reduced runtime significantly because converting to radians each time we calculated distance took almost three times the current runtime.

We then calculated the closest public transportation stops to each obese area. We defined close as equal to or less than a mile away. We used product to map all possible stop and obese combinations and calculated the distance between both using project. After we used select to filter out all the stops further away than our defined 1 mile radius. We then aggregated each obsese area together to form a list of stops. Some limitations of these transformations were because of the size of the datasets. Because product creates every possible combination of MBTA stops and locations, the program takes some time to run. 

## Closest Health Location to each Control/Obesity Location
For each control/obesity location, we calculated the closest healthy location. We put these in a dataset, with closest MBTA data included as well (calculated above). We performed the same transformations as the previous closest MBTA transformations, but instead of the closest list of MBTA stops, we found the first closest healthy location. 

## Shortest Path
Using the closest MBTA stops (to obese and healthy locations) found above, we calculate the shortest route to a healthy location from an obese location. We use Dijkstra's algorithm and the MBTA dataset to find the shortest path between each obesity location and its closest healthy location. To do this, we create a graph of the MBTA (subway only) using networkx's DiGraph class. We then take a combination of the estimated time it would take to travel that route and the time it takes to walk the remaining distance and add that to a travel times list. 

For each location we use the shortest path function from networkx to receive an estimated travel time (in minutes) from nearby stops to a healthy locations MBTA stop. To account for travel to an MBTA stop, via bus travel and walking travel, we used the Google Maps API to calculate the minimum travel time and append it to the travel times list. In order to find the minimum travel time overall, we simply took the minimum of the list of travel times.

The biggest limitation of this technique is that we find the closest healthy location using the distance formula. Because the distance formula does not take the MBTA into account, it is entirely possible that there is a healthy location that is slightly farther away but would take less time to reach. Another limitation we ran into is the way the MBTA stores their bus data. It was impossible to use this in the algorithm or even to transform it to the format we needed primarily due to the data structure, which often accounted numerous locations for single stop. Instead, we used the Google API to calculate bus travel time.

## Linear Regression
We used linear regression to see how strong the correlation between access to healthy locations and obesity is. We formatted our data so that the X dataset is the estimated travel time and the Y dataset is the corresponding obesity percentage. By having our data formatted this way, we have results that will show decreasing travel time to a healthy location decreases the obesity levels in an area.

We used trash bins as a control to make sure that any correlation we found is specific to the obesity locations. Because trash cans are likely unrelated to the obesity in an area, we expected little or no correlation. We found that there was a positive correlation with a slope of 16 between obesity and distance from a healthy location. This means that if we decrease the distance a person has to go to reach a healthy location (program, store, etc.), we can drastically decrease the levels of obesity in that area. 

# Results and Conclusions
Given the obesity and healthy locations data, we created a map of Boston that shows where each location is. The obesity locations are in yellow and healthy locations in purple. Obesity locations are sized based off of obesity percentage of the area population. 

![Map of Boston with obesity and healthy locations:](../visuals_site/images/bostonmap.png)

Our data analysis found that there was a huge correlation between obesity and distance from a healthy location. The linear regression suggests that for every minute more it takes to get to a healthy location, the obesity rate increases by .2 percent (because the slope of the linear regression is .2256). This occurs with a baseline obesity percentage of 16 (based on a y-intercept of 16.5). Meaning that in the best case where there is an area directly by a healthy location, that area is predicted to have an obesity rate of 16. The further the area is from a healthy location, the more severe the obesity rate becomes. The mean squared error was 10.4, which suggests some variance despite an overall trend.


![Results for Linear Regression:](../visuals_site/images/linregressgraph.png)

We ran our algorithm on control data and found that there was a slight correlation between obesity and distance from a trash bin with an obesity rate increase of .02 % per minute longer it takes to get to a big belly location. This is less than one tenth the correlation healthy locations had. Surprisingly, our control data had a similar MSE to our Healthy locations data. While this does mean that there may be external factors contributing to the correlations, the correlation between obesity and distance of healthy locations was much stronger. 

Overall, healthy locations are not located in areas with higher obesity. It is possible that healthy locations are lowering current rates of obesity. It is also possible that the city of Boston needs to do a better job placing healthy locations. In order to get a more definite answer, we would need to do further work, highlighted below.

# Future Work
A few questions that we would like to address in future work that we were not able to pursue are:
* Do areas with more than one healthy location have lower rates of obesity? If so, how much are these healthy locations helping lower obesity percentage?
* Would the introduction of a healthy location into an obese area lower the obesity rate over time?
* Could we predict an optimal point or points to place a healthy location based on our data?

# References
1.  [Urban Orchards](https://data.cityofboston.gov/Health/Urban-Orchards/c7cz-29ak)
2.  [Healthy Corner Stores](https://data.cityofboston.gov/Health/Healthy-Corner-Stores/ekiy-2qmz)
3.  [Community Culinary and Nutrition Programs](https://data.cityofboston.gov/Health/Community-Culinary-And-Nutrition-Programs/tma6-pdxu)
4.  [Obesity Among Adults](https://chronicdata.cdc.gov/500-Cities/500-Cities-Obesity-among-adults-aged-18-years/bjvu-3y7d)
5.  [MBTA Routes](http://realtime.mbta.com/developer/api/v2/routes)
6.  [Big Belly Locations](https://data.cityofboston.gov/City-Services/Big-Belly-Locations/42qi-w8d7/)