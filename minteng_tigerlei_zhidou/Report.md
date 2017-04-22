# Find the best place of living in Boston area and corresponding analysis

 *by Minteng Xie, Yue Lei, Zhi Dou*

## 1. Introduction

We want to find a best office location for a new company. The first factor we consider is the rent of the location, so we find the data of average rent for different cities in Greater-Boston. The second factor is convenient transportation, then we fetch the MBTA data, and we assume that the location will be more convenient if there are more stops around this location. The third factor is food, we think the location is better if there are many restaurants around it. Similarly, the fourth factor is safety, we do not want too many crimes appeared near the location. The last factor is salary, we may add some fuctions related to different types of jobs.

## 2. Datasets

1. [Average Rent](http://datamechanics.io/data/minteng_zhidou/rent.txt)
2. [MBTA Stops](http://datamechanics.io/data/minteng_zhidou/stops.txt)
3. [Food Data](https://data.cityofboston.gov/Permitting/Active-Food-Establishment-Licenses/gb6y-34cq)
4. [Safety(Crime 2015-2017)](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-August-2015-To-Date-Source-/fqn4-4qap)
5. [Salary 2015](https://data.cityofboston.gov/Finance/Employee-Earnings-Report-2015/ah28-sywy)
6. [Salary 2014](https://data.cityofboston.gov/Finance/Employee-Earnings-Report-2014/4swk-wcg8)
7. [Goolge Maps](https://www.google.com/maps)

## 3. Preprocessing

## 4. Methodologies 

## 5. Results

## 6. Future Work

## Reference

1. In first transformations, we combine rent table with zipcode of accorsponding area. First we fetch longitude and latitude based on the name of area in rent table via google maps api and then using this location information as input to fetch zipcode also with the help of google maps api. Then combine location table with rent table and implement aggregation to get the final data set with rent and the zipcode.

To run this transformation:
```python
python3 rent.py
```

2. Project MBTA, Food and Safety data, besides the needed infomation, for the value of key "location", we add tags such that (location, "transport") for MBTA data, (location, "food") for Food data and (location, "crime") for Safety data. Then implement union of three datasets into the second new dataset. After union, implement selection to remove data with invalid locations (for example, with longitude and latitude equal to 0).

To run this transformation:
```python
python3 location.py
```

3. After project the needed information, combine the two Salary data, then aggragate the dataset using the job title as the key, get the average salary for different jobs. The third new dataset contain the key: job title, values: average salary and other infomation such as company name, year and so on.

To run this transformation:
```python
python3 salary.py
```

# Project 2
### *by Minteng Xie, Yue Lei, Zhi Dou*

## 1.
A new team is formed by Minteng Xie, Yue Lei and Zhi Dou. All scripts and files of project 2 is under new folder ```minteng_tigerlei_zhidou```. We modify part of ```location.py``` in project 1 and add a new transformation ```crime.py``` to retrieve and store new crime data into database. All ```.ipynb``` files are just used to plot and show graphs in case of running error inspected by ```execute.py```.

### auth.json
This project use app token from ```boston data portal``` and ```googlemaps geocoding API```. To retrieve data automatically, app token should be added into `auth.json` file as follow format:
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

## 2. Narrative & Problems
### Problem 1: Optimization
Following the idea of project 1, our goal is to find a best office location for a new company. Since a detailed coordinate is meaningless, we try to find a suitable area. Project 1 has helped us gather all the licensed restaurants/ crime incidents/ MBTA stops/ rent price in boston area. We gonna find the best area that maximize **```#restaurant```**, **```#MBTA stops```** and minimize **```#crime incidents```** and **```rent price```**. 

We use googlemaps api to find the left bottom/ right top coordinates of boston area. With these coordinates, we could build a big rectangle containing boston area. Then we separate this rectangle into 10 x 10 grids(user could set this scale manually). 

![boston_grid](http://datamechanics.io/data/minteng_zhidou/Boston_grid.png)

Removing those blank grids which don't contain any useful data, we have 52 grids left. Each grid represents a possible target area which contains a suitable place for opening a company. Therefore, we could count the number of restaurant/ crime incidents/ MBTA stops(including buses and subway) in every grid and evaluate these numbers by mapping them into scores from 1-5. And according to the center coordinate of this grid, googlemaps api could help us to find it belongs to which area(like Allston/ Back Bay/ Fenway/...). 

![box_count](http://datamechanics.io/data/minteng_zhidou/map_with_label.png) 

*(This graph was generated by Boston_Grid_Count.ipynb)*

Then our database would search and find matched rent price, which also should be mapped into reversed scores from 1-5. Then we get the tuple of ratings(The higher the better) for each grid in the format of 
```
(transport, food, safety, rent) 
```
All these data would be stored in a new collection named ```box_count```.

User could customize rating due to their preference in ```optimization.py```. It would search user's ratings requirement in database. If it finds results with every rating of ```(transport, food, safety, rent)``` above requirement, return the result with maximal sum of these four ratings. Else it would return the result with minimal distance from the requirement ratings. 

We provide an example that our algorithm rank all 52 grid area according to user's requirement of grades: **```(3, 4, 3, 4)```** and provide top choices as well as its bound coordinates, area name & zipcode, average rent and ratings.
```
Top fitted areas:
Bound: [[42.2622102, -71.0835318], [42.2793753, -71.0566365]]
Area: Mattapan 02126    Avg rent: 1403
Grades: {'safety': 3, 'rent': 5, 'food': 4, 'transport': 4} 

Bound: [[42.2622102, -71.1642177], [42.2793753, -71.1373224]]
Area: West Roxbury 02132    Avg rent: 1476
Grades: {'safety': 3, 'rent': 4, 'food': 4, 'transport': 3} 

Bound: [[42.2793753, -71.0566365], [42.2965404, -71.0297412]]
Area: Dorchester 02122    Avg rent: 1524
Grades: {'safety': 2, 'rent': 4, 'food': 4, 'transport': 3} 

Bound: [[42.2622102, -71.1373224], [42.2793753, -71.11042710000001]]
Area: Roslindale 02131    Avg rent: 1685
Grades: {'safety': 2, 'rent': 3, 'food': 4, 'transport': 3} 

Bound: [[42.3137055, -71.1373224], [42.330870600000004, -71.11042710000001]]
Area: Jamaica Plain 02130    Avg rent: 2214
Grades: {'safety': 3, 'rent': 3, 'food': 5, 'transport': 2} 
```

Assuming ```rent.py```, ```location.py```, ```salary.py```, ```crime.py```(retrieve and transformations procedure) has been run.

To solve this optimization problem, first run the ```box_count.py```:
```python
python3 box_count.py
```
And then run ```optimization.py```:
```python
python3 optimization.py
```
Remember to uncomment the last lines in the file:
```python
# <filename>.execute()
```

### Problem 2: Statistical Analysis
After finding ideal area for a new company, we would like to dig deeper into those areas, because this area might be the best choice for now, but it might change, with the variation of rental, crime and transportations. So based on current data, we want to study on the trend of these factors, and for now we mainly focus on crime in different blocks(grids). A new dataset [Safety(Crime 2012-2015)](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-July-2012-August-2015-Sourc/7cdf-6fgx) has been added.

Now let *X<sub>ij</sub>* as the the number of crimes happens in block *i* in year *j*. If *X<sub>ij</sub>* and *X<sub>i(j + 1)</sub>* are highly correlated, then we could claim the number of crimes of these two year in this block have similar distribution. Thus if these random variables continuously related to each other, then we could use such correlation to predict the trend of the criminal events in this year.

For each block(grid), we could count the number of crime incidents of each month in different years(2013- 2016). We build a matrix with **```year```** x  **```#blocks```** x **```#month```**(5 x 52 x 12). Then we calculate **correlation coefficient** and **p-value** for each block so that we could compare them in consistent years. We find that for some blocks, these **correlation coefficient** are close to 0 and **p-value** are close to 1, which means for these blocks, their crime incidents in consistent years are not related. However, we have the ability to do reasonable prediction for those blocks which have high **correlation coefficient** and low **p-value** year by year. 

For example, block 27```[[42.34893792999999, -71.0586156], [42.36623191999999, -71.0144498]]```(02109) has a good performance as follow: 

|     year      | correlation coefficient |       p value       |
|:-------------:|:-----------------------:|:-------------------:|
|   2012-2013   |  0.764868546433         |  0.000643432484115  |
|   2013-2014   |  0.836472540464         |  0.003345903249322  |
|   2014-2015   |  0.735134468067         |  0.006447586595446  |
|   2015-2016   |  0.882368732529         |  0.001234912479238  |

From the graph below we could see the trend of block 27 in the consistent four years(2013-2016) are in similar mode.

![block27](http://datamechanics.io/data/minteng_zhidou/Block27.png) 

*(This graph is generated by fitting.ipynb)*

Because this data of these four year have strong linear relationship, there is a high probability that their criminal records have the same tendency through the entire year. Therefore, we fit all the data in four year to find a common pattern of block 27. Now assume, 2016-2017 could still maintain such strong linear relationship, and then we could use this fitting funtion to simulate the trend of crime of block 27 in this year.

![fitting](http://datamechanics.io/data/minteng_zhidou/fitting.png) 

*(This graph is generated by fitting.ipynb)*

To solve this analysis problem, first run the ```crime.py```:
```python
python3 crime.py
```
And then run ```crimeAnalysis.py```:
```python
python3 crimeAnalysis.py
```
Remember to uncomment the last lines in the file:
```python
# <filename>.execute()
```

## 3.a 
### Provenance information
All provenance information could be seen in ```provenance.html``` after running:
```python
python3 execute.py minteng_tigerlei_zhidou
```

## 3.b 
### Trial mode
In trial mode, the algorithm would complete its execution very quickly (in at most a few seconds) by operating on a very small portion of the input data set(s). All retreieve and transformation are limited to 500 records.

Remember to uncomment last few lines of the file
```python
# if 'trial' in sys.argv:
#     <filename>.execute(True)
# else:
#     <filename>.execute()
```
To run trial mode on all files:
```python
python3 execute.py --trial
```

To run trial mode on separate files:
```python
python3 <filename>.py --trial
```
