# Find the best living area in Boston and corresponding analysis

 *by Minteng Xie, Yue Lei, Zhi Dou*

## 1. Introduction
The City of Boston has performed a significant effort on collecting data over different services and other public information. The diversity of these publicly available datasets allows us to explore various areas in Boston. Particularly, in this project, we are focusing on building a website to help people find the best living area in Boston and provide corresponding analysis to their choices.

Since it is a really complex problem to define which area of Boston is most suitable for living, we simplify it by four main factors: `Rent`, `Transport`, `Food`, `Safety` and map them to ratings in 1~5. Through our website, users could customize the ratings of these four aspects based on their personal requirements so that they could find the ideal place of living.

Besides, the interactive statistical analysis is provided. Users could either view the overall analysis of four aspects based on great Boston area or get a 4-year-long detailed crime analysis graph based on their possible targets, which could help them make better decisions. 

## 2. Datasets

- [Average Rent](http://datamechanics.io/data/minteng_zhidou/rent.txt)
- [MBTA Stops](http://datamechanics.io/data/minteng_zhidou/stops.txt)
- [Active Food Establishment Licenses](https://data.cityofboston.gov/Permitting/Active-Food-Establishment-Licenses/gb6y-34cq)
- [Crime Incidents In Boston(2012-2015)](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-July-2012-August-2015-Sourc/7cdf-6fgx)
- [Crime Incidents In Boston(2015-2017)](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-August-2015-To-Date-Source-/fqn4-4qap)

## 3. Preprocessing
The preprocessing steps were performed based on relational data and map-reduce paradigm.
- Combine rent data with the zip code of a corresponding area. To achieve that goal, we fetch longitude and latitude based on the name of the area in rent dataset via google maps API and then using this location information as input to fetch zip code also with the help of google maps API. Then we combine location information with rent data and implement aggregation to get the final data set with rent and the zip code. The data looks like as below:
```json
{ 
    "avg_rent" : 2359, 
    "area" : "Allston", 
    "postal_code" : "02134" 
}
```
- Projecting MBTA, Food and Safety data, besides the needed infomation, for the value of key "location", we add tags such that (location, "transport") for MBTA data, (location, "food") for Food data and (location, "crime") for Safety data. Then we create a union of three datasets into the second new dataset. After union operation, selection is used to to remove data with invalid locations (for example, with longitude and latitude equal to 0).
```json
{   
    "address" : "1159 Washington", 
    "location" : [ 42.272239, -71.068856 ], 
    "type" : "food", 
    "zip" : "02126", 
    "businessname" : "SPUKIES PIZZA RESTAURANT", 
    "city" : "Mattapan" 
}
```
- Postal code and area in the first dataset imply the location, thus taking location as key, via the help of google maps, we aggregate above two datasets. After that, selection is applied to get data in with in certain square then sum aggregation used to compute the total number of crime, food and transpotation in this area. Finally, based on certain function, project these sum to grade. 
```json
{
    "postal_code" : "02136", 
    "area" : "Hyde Park", 
    "avg_rent" : 1597, 
    "count" : { "crime" : 96, "transport" : 15, "food" : 14 },
    "grade" : { "rent" : 3, "safety" : 4, "transport" : 1, "food" : 1 },
    "box" : [ [ 42.22788, -71.1642177 ], [ 42.2450451, -71.1373224 ] ] 
}
```
- Then based on dataset "box_count", more analysis could be implied. Taking box attribute in "box_count" and selector, go throught crime dataset, a new dataset about monthly total number of crime each block could be built.
```json
{
    "area" : "Dorchester", 
    "box" : [ [ 42.2793753, -71.0835318 ], [ 42.2965404, -71.0566365 ] ],
    "crimeNum":[ 396, 328, 380, ..., 497, 456, 393 ],
    "crimeRatio" : [ 0.05765, 0.05664, ..., 0.05242]
}
```
## 4. Methodologies 

### Optimization
Given all the licensed restaurants/ crime incidents/ MBTA stops/ rent price in Boston area, We gonna find the best living area with maximizing **`#restaurant`**, **`#MBTA stops`** and minimize **`#crime incidents`** and **`rent price`**. 

We use GoogleMaps API to find the left bottom/ right top coordinates of Boston area. With these coordinates, we could build a big rectangle containing Boston area. Then we separate this rectangle into 10 x 10 grids. 

![boston_grid](http://datamechanics.io/data/minteng_zhidou/Boston_grid.png)

Removing those blank grids which don't belong to Boston area, we have 52 grids left. Each grid represents a possible target area which contains a potential place for living. Therefore, we could count the number of restaurant/ crime incidents/ MBTA stops(including buses and subway) in every grid and evaluate these numbers by mapping them into scores from 1-5(safety score is reversed by crime). And according to the center coordinate of this grid, google maps API could help us to find it belongs to which area(like Allston/ Back Bay/ Fenway/...). 

![box_count](http://datamechanics.io/data/minteng_zhidou/map_with_label.png) 

*(This graph was generated by Boston_Grid_Count.ipynb)*

Then our database would search and find matched rent price, which also should be mapped into reversed scores from 1-5. Then we get the tuple of ratings(The higher the better) for each grid in the format of 
```
(transport, food, safety, rent) 
```
All these data would be stored in a new collection named ```box_count``` as follow.
```json
{   "_id" : 1, 
    "avg_rent" : 1597, 
    "box" : [ [ 42.22788, -71.1642177 ], [ 42.2450451, -71.1373224 ] ],
    "postal_code" : "02136", 
    "grade" : { "transport" : 1, "food" : 1, "safety" : 4, "rent" : 3 }, 
    "area" : "Hyde Park", 
    "count" : { "transport" : 15, "food" : 14, "crime" : 96 } }
```
User could customize rating due to their preference in website. It would search user's ratings requirement in database. If it finds results with every rating of `(transport, food, safety, rent)` above requirement, return the result with maximal sum of these four ratings. Else it would return the result with minimal distance from the requirement ratings. Detailed algorithm could be found under `web/optimization_algorithm.py`


### Statistical Analysis
After finding an ideal area for a living place, we would like to dig deeper into those areas because this area might be the best choice for now, but it might change, with the variation of rental, crime, and transportations. So based on current data, we want to study on the trend of these factors, and for now, we mainly focus on crime in different blocks(grids). 

Now let *X<sub>ij</sub>* as the number of crimes happens in block *i* in the year *j*. If *X<sub>ij</sub>* and *X<sub>i(j + 1)</sub>* are highly correlated, then we could claim the number of the crime of these two years in this block have the similar distribution. Thus if these random variables continuously related to each other, then we could use such correlation to predict the trend of the criminal events in this year.

For each block(grid), we could count the number of crime incidents of each month in different years(2013- 2016). We build a matrix with **```year```** x  **```#blocks```** x **```#month```**(5 x 52 x 12). Then we calculate **correlation coefficient** to the degree these two variables linearly related. Since this linear property may happen coincidentally, we want to compute how much we could trust this result. Thus Hypothesis testing is applied. Assume the correlation coefficient is wrong, then by computing **p-value** to test our assumption. We find that for some blocks, these **correlation coefficients** are close to 0 and **p-values** are close to 1, which means for these blocks, their crime incidents in consistent years are not related. However, we have the ability to do the reasonable prediction for those blocks which have high **correlation coefficient** and low **p-value** year by year. 

For example, block 42 -- Downtown```[ [ 42.348035700000004, -71.0566365 ], [ 42.365200800000004, -71.0297412 ] ]```(02109) has a good performance as follow:


|     year      | correlation coefficient |      P-value      |
|:-------------:|:-----------------------:|:-----------------:|
|   2013-2014   |  0.782569291953         |  0.0026219859084  |
|   2014-2015   |  0.796445834967         |  0.0019334569301  |
|   2015-2016   |  0.928294156304         |  0.0000132251510  |


From the graph below we could see the trend of block 42 in the consistent four years(2013-2016) are in the similar mode.

![block42](http://datamechanics.io/data/minteng_zhidou/block42.png) 

*(This graph is generated by fitting.ipynb)*

Because this data of these four years have a strong linear relationship, and their P-value is very small, thus we should deny the assumption, which means there is a high probability that their criminal records have the same tendency through the entire year. Therefore, we fit all the data in four years to find a common pattern of block 42. Now assume, 2016-2017 could still maintain such strong linear relationship, and then we could use this fitting function to simulate the trend of the crime of block 42 in this year.

![fitting](http://datamechanics.io/data/minteng_zhidou/fitting.png) 

*(This graph is generated by fitting.ipynb)*

## 5. Results 
We use [Flask](http://flask.pocoo.org/docs/0.12/) and [MongoDB](https://www.mongodb.com/) to implement the web service. The homepage:
![homepage](http://datamechanics.io/data/minteng_zhidou/web_pages/1_home.png) 

The first new feature/component under `Optimization` part is to visualize the optimization problem in project2. 
Users could select and choose their preferred grades for 4 attributes, the ratings are in 1 ~ 5, the higher the better:
![input11](http://datamechanics.io/data/minteng_zhidou/web_pages/3_input11.png)

Then, we could get the top fitted location results using the algorithms described in the above Methodologies:
![table](http://datamechanics.io/data/minteng_zhidou/web_pages/5_table1.png)

Users could view these areas on an interactive map with labeled blocks filled in different colors, which is created by [Leaflet](http://leafletjs.com/) :
![map11](http://datamechanics.io/data/minteng_zhidou/web_pages/6_map1.png)

Besides, crime analysis for those results is present by clicking on `Crime analysis` button. The user could get the crime ratio of the certain block in the total crime number for different month/year:
![crime-analysis](http://datamechanics.io/data/minteng_zhidou/web_pages/7_crime-analysis.png)

The second new feature/component is under `Statistical Analysis` part. We randomly choose 30 blocks and use [D3.js](https://d3js.org/) to show four grades for each block in a bar chart:
![grades](http://datamechanics.io/data/minteng_zhidou/web_pages/9_grade1.png)

To study the relationship between these four attributes, correlation coefficient and p-value were calculated based on these 30 random blocks:
![values](http://datamechanics.io/data/minteng_zhidou/web_pages/10_four-nodes-cc.png)

With these values, we visualize their relationship by setting four attributes as the nodes and the value of `(1-abs(Correlation Coefficient))*500` as the edge length, which means that if two attributes have higher Correlation Coefficient, they will be much closer than others:
![4nodes](http://datamechanics.io/data/minteng_zhidou/web_pages/11_four-nodes-plot.png)
As the graph shows above, it is quite obviously that "Transport" and "Safety" has high Correlation Coefficient

At last, we do some more interesting things focus on predicting the potential development of each block, especially on crime. Assuming the number of the crime of one certain block within one month in the certain year as a random variable. To find out the relationship of such random variable with next year, correlation coefficients and P-values were computed: 
![plots](http://datamechanics.io/data/minteng_zhidou/web_pages/12_cc-pvalue.png)

As for `Project Link` part, it will direct to our GitHub folder.

## 6. Future Work
- Due to the limitation of the data resource, our analysis particular emphasize on crime part. For instance, we just got average rent price of last year so that we couldn't analyze more detailed information from that. In the future, the City of Boston may post more datasets publicly, which means more useful data will be collected. We plan to extend our factors deeper and richer to make our model more accurate. Traffic condition or accidents can be added as a supplement for parts of transportation. Besides, more influence factor will be counted such as entertainment, public facility and so on.
- With sufficient data resources, way better analytical approaches can be applied in our project. Correlation coefficient and ratio have many limitations and deficiency in statistical analysis. We can do the factor analysis to figure out which of these factors are the most important. And time series analysis is a powerful tool to present the changes and trend of different factors. 

## Reference
[1] http://flask.pocoo.org/docs/0.12/

[2] http://bl.ocks.org/juan-cb/ac731adaeadd3e855d26

[3] https://bl.ocks.org/mbostock/4062045

[4] http://bl.ocks.org/ndobie/878f34d2810058c5b821

# Instructions

All scripts and files are under folder `minteng_tigerlei_zhidou`. We modified `execute.py` into `initiate.py` so that it won't traverse subdirectory like `/web`, which contains all the scripts of running web server. `initiate.py` just takes the job of automatically retrieving data into MongoDB and does all transformations. So you just need to run it once and control web server mannully every time. All `.ipynb` files are just used to plot and show graphs in the case of running error inspected by `initial.py`.

### auth.json
This project use app token from `Boston data portal` and `google maps geocoding API`. To retrieve data automatically, app token should be added into `auth.json` file as following the format:
```
{
    "services": {
        "googlemapsportal": {
            "service": "https://developers.google.com/maps/",
            "username": "alice_bob@example.org",
            "key": "xxXxXXXXXXxxXXXxXXXXXXxxXxxxxXXxXxxX"
        },
        "cityofbostondataportal": {
            "service": "https://data.cityofboston.gov/",
            "username": "alice_bob@example.org",
            "token": "XxXXXXxXxXxXxxXXXXxxXxXxX",
            "key": "xxXxXXXXXXxxXXXxXXXXXXxxXxxxxXXxXxxX"
        }
    }
}
```

### Trial mode
This project provides a trial mode to complete data retrieve and transformations very quickly (in at most a few seconds) by operating on a very small portion of the input data set(s). All retrieve requests and transformations are limited to 500 records.

Locate to project folder with:
```shell
cd minteng_tigerlei_zhidou
```

To run trial mode on all files:
```python
python3 initial.py --trial
```

To run trial mode on seperate files, remember to uncomment last few lines of the file
```python
if 'trial' in sys.argv:
     <filename>.execute(True)
else:
     <filename>.execute()
```
Then run it with :
```python
python3 <filename>.py --trial
```

### Prepare Database
First, make sure `mongod` process is running on your machine. 

Locate to project folder with:
```shell
cd minteng_tigerlei_zhidou
```

Then run the following command:
```python
python3 initiate.py 
```

### Start Web Server
Locate to web service folder with:
```shell
cd minteng_tigerlei_zhidou/web
```
Then run the following command:
```python
python3 web.py
```
To view the website, open a browser on your machine and type: 
```sh
127.0.0.1:5000
``` 

### Provenance Information
All provenance information could be seen in ```provenance.html``` after running:
```python
python3 initiate.py minteng_tigerlei_zhidou
```
