# Project narrative

Our project seeks to explore the relationship between food accessibility, obesity and income in Boston's neighborhoods. We believe that we will find that a smaller income and a lack of close food sources in a neighborhood will correlate to a higher obesity percentage. In order to do this, we created a method to score each neighborhood based on how their accessible food sources are, and then we used this information to determine a correlation.
# Dataset descriptions

1. **Obesity Statistics in Massachusetts**: This dataset contains properties such as population over 20 and population with a BMI of 30 or higher in a certain area defined by geographic coordinates. (obesitystats.py)
2. **Boston Income information per neighborhood**: This dataset contains information concerning the median household income per neighborhood. (population.py)
3. **Farmers' Markets**: This dataset contains information about Farmers' Markets in Boston. (farmersmarkets.py)
4. **Corner Markets**: This dataset contains information about Corner Markets in Boston. (cornermarkets.py)
5. **Supermarkets**: This dataset contains information about the supermarkets in Boston. (supermarkets.py)
6. **Boston Neighborhood Shapefiles**: This dataset contains the geographic coordinates of the neighborhoods in Boston. (neighborhood.py)
7. **Master Address List**: This dataset contains all the residential addresses in the neighborhoods of Boston.

# Transformations

First, we combined the Farmers' Markets, Corner Markets, and Supermarkets datasets in order to create an overall Food Source dataset. In order to do this we needed to standardize the attribute names, as well as get rid of attributes that we deemed as unnecessary. Since not all of the datasets included latitude and longitude information, we used Google Maps Geocoding API in order to retrieve that information based on the address of the food source. (foodsources.py)

Second, we had to map the regions in the Obesity Statistics in Massachusetts to neighborhoods in Boston in order to calculate the percentage of people who had a BMI >= 30 per neighborhood. (obesityperneighborhood.py)

Third, we created a new dataset that combines information from all of the datasets to look at the relationships between information that will help us answer our overall project narrative. This new dataset includes the average income, total number of food sources and average obesity based on the neighborhood. (neighborhoodstatistics.py)

# Algorithms

### Calculating a Food Accessibility Score For Each Neighborhood: ###
In order to calculate a food accessibility score for each neighborhood we looked at three important factors: 
* The average number of food sources in the neighboorhood within walking distance of a residence. 
* The average distance to the closest food source for each residence.
* The average quality of the food source (based on how much of each type of food source there is) within walking distance

These three items have a huge impact on what it means to have a "good" food accessibility food score. Our main focus for the first metric was to get the average number of food sources that are within walking distance in the specified neighborhood. This is found by calculating the total number of food sources that are within walking distance per house and computing the mean. 

Next, we looked at what the average distance was to the closest food source per neighborhood. This was found by taking a list of closest food source distance per house for the specified neighborhood and calculating the mean. 

The last metric we look at, this one taking a bit more computation, was the average quality of food sources in the neighborhood. There were a few options that we considered when deciding how this number was going to be calculated. The one that seemed to make the most sense was to rank each type of food source and give it a 'weight'. So, a farmer's market had a weight of 1, a supermarket had a weight of 2/3, and a cornerstore had a weight of 1/3. We ranked them based on the healthiness of the food source, as well as the variety of foods that one could buy.

After finding these values for each house in the neighborhood, we calculated the mean of each metric (per house). After getting a matrix of the mean values, we converted each metric into z-scores, which standardizes the scores and allows each of the metrics to be compared. Then, we added them and then scaled these resulting values from 0 to 100 in order to create 1 final composite score for each neighborhood.

| Neighborhood                |   Avg # of Food Sources* |   Avg Distance To Closest Food Source (km) |   Quality of Food Sources* |   Score |
|:----------------------------|-------------------------:|-------------------------------------------:|---------------------------:|--------------------:|
| Financial District/Downtown |                     8.50 |                                       0.23 |                       0.39 |              100.00 |
| Bay Village                 |                     2.00 |                                       0.19 |                       0.33 |               63.05 |
| Dorchester                  |                     7.14 |                                       0.37 |                       0.10 |               61.93 |
| Mission Hill                |                     2.86 |                                       0.23 |                       0.62 |               87.91 |
| Beacon Hill                 |                     1.00 |                                       0.30 |                       0.33 |               50.89 |
| Charlestown                 |                     5.70 |                                       0.28 |                       0.40 |               83.44 |
| East Boston                 |                     6.83 |                                       0.23 |                       0.19 |               76.14 |
| West End                    |                     4.00 |                                       0.29 |                       0.42 |               74.65 |
| Mattapan                    |                     4.16 |                                       0.42 |                       0.19 |               49.59 |
| Roxbury                     |                     4.26 |                                       0.38 |                       0.13 |               48.52 |
| North End                   |                     4.86 |                                       0.15 |                       0.46 |               90.73 |
| South End                   |                     7.88 |                                       0.19 |                       0.34 |               94.98 |
| West Roxbury                |                     0.95 |                                       1.05 |                       0.26 |                0.00 |
| Allston/Brighton            |                     4.26 |                                       0.38 |                       0.11 |               46.78 |
| South Boston                |                     4.55 |                                       0.36 |                       0.20 |               56.93 |
| Back Bay                    |                     4.12 |                                       0.30 |                       0.62 |               90.34 |
| Fenway/Kenmore              |                     7.76 |                                       0.20 |                       0.36 |               95.94 |
| Jamaica Plain               |                     4.70 |                                       0.45 |                       0.29 |               58.97 |
| Hyde Park                   |                     2.82 |                                       0.57 |                       0.12 |               28.20 |
| Roslindale                  |                     2.84 |                                       0.48 |                       0.24 |               43.50 |


\* *Within walking distance of a residence, which we defined to be < 1km*

A high score denotes that the food accessibility is better in that neighborhood compared to other neighborhoods in Boston.  In our case, the best neighborhood in regards to food accessibility belongs is Financial District/Downtown, whereas the worst is West Roxbury. Considering that the next smallest score is 28.2 (Hyde Park), this suggests that there is a very large difference in food accessbility between West Roxbury and Financial District/Downtown. This could be due to the fact that Financial District/Downtown is a smaller area and thus more dense than West Roxbury. 

### Determining Correlation: Our Coefficient Correlation Array ###

|       | Food Score |   Income |   Obesity |
|:----------------------------|-------------------------:|-------------------------------------------:|---------------------------:|
|**Food Score** | 1.0         |   -0.0243  |  -0.466  |                       
|**Income** | -0.0243  |   1.0         |  -0.543  |                       
|**Obesity** | -0.466 |   -0.543|  1.0          |

Shown above is our coefficient correlation array for our three variables containing data from food score, income, and obesity. The correlation coefficient array shows that there is a relatively strong negative correlation between obesity and income, as well as between the food accessibility score and obesity. However, there doesn't seem to be any correlation between the food accessbility score and the income. 

This negative correlation between obesity and income, as well as food accessbility and obesity are relationships that we expected to see when undertaking this project. 

# Visualizations

We created a web server in Python (using Flask) in order to interact with MongoDB and render the HTML pages.

The first visualization is a chloropleth map of Boston that shows Boston's neighborhoods shaded with the average value of either obesity, food accessibility score, average # of food sources within walking distance, and the average quality of those food sources within walking distance. Higher values correspond to a darker, more intense color. This map was created using d3.js (Javascript library). 

![](https://github.com/velvetbleurose/course-2017-spr-proj/blob/master/jguerero_mgarcia7/visualization1.gif)

The second visualization plots two variables against each other, and displays the corresponding correlation coefficient. This allows you to quickly visualize whether two variables have positive, negative, or no correlation. [INSERT HOW IT WAS CREATED]

# Conclusion/Future Work

Based on data characterizing Boston’s neighborhoods, we can conclude that there is a definite relationship between income and food accessibility on incidence of obesity. In both cases, it was found that the higher the income and the higher the food score, the lower the obesity. This resonates with research being done that frame obesity as a social problem, and one that  can thus be fixed by improving the overall economic outlook of a neighborhood, as well as increasing food accessibility to better quality food sources. However, though the results looks promising, our sample size of 20 neighborhoods is too small to really allow us to make any meaningful conclusions about the relationship between food accessibility,  income, and obesity. In the future, we would look to extend this method of analysis to more cities and their neighborhoods.

In addition, more analysis can be done on the food accessibility scoring method. Future researchers can come up with more metrics to score a neighborhood, and then decide using statistical analysis which metrics have the largest effect on the overall score and the largest effect on obesity. In addition, one can also alter the metrics already used in order to take into account the total area of the neighborhood, so that neighborhoods such as West Roxbury and Financial District/Downtown can be more easily compared.

# Required libraries and tools
The libraries pyshp, shapely, geopy, numpy, pickle, scipy, sklearn will need to be installed before the program can be executed. They can be installed with these pip commands:
```
pip install pyshp
pip install shapely
pip install geopy
pip install numpy
pip install pickle
pip install scipy
pip install sklearn
```
