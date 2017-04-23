## Project 1
# Datasets we are using
1. CDC500 - https://chronicdata.cdc.gov/500-Cities/500-Cities-Local-Data-for-Better-Health/6vp6-wxuq
2. Higher Education Dataset - https://inventory.data.gov/dataset/032e19b4-5a90-41dc-83ff-6e4cd234f565/resource/38625c3d-5388-4c16-a30f-d105432553a4

3. Healthy Corner Stores in Boston – https://data.cityofboston.gov/Health/Healthy-Corner-Stores/ekiy-2qmz

4. Public Swimming Pools in Boston – https://data.cityofboston.gov/Public-Property/Year-Round-Swimming-Pools/rtqb-8pht/data

5. Boston Hospitals – https://data.cityofboston.gov/Public-Health/Hospital-Locations/46f7-2snz

# Narrative

For this project, we wanted to create datasets that could tell us whether certain medical conditions or measures (as they are called on the CDC dataset) can be correlated with given attributes of where the person lives (e.g. if a person lives near a hospital). We collect all the necessary datasets in retrieveData.py. We use the GeoPy API to find coordinates for datasets that do not provide that information.

The first dataset (created by transformation0.py) is a dataset that has all records in the CDC500 dataset of people in Boston visiting their doctors and maps them to the hospital nearest to them. We suspect that the closer one lives to a hospital the more often they would go visit their doctor. A lack of check ups could lead to undiagnosed diseases/injury so based on this information we can see the areas in Boston where doctors need to be more accessible.

The second dataset (created by transformation1.py) is a dataset that has all the people in Boston and Cambridge who sleep less than 7 hours and maps them to the nearest colleges/universities in Boston/Cambridge. We expect that these areas are populated by almost college students exclusively and therefore will have many people who sleep less than 7 hours.

The third dataset (created by transformation2.py) is a dataset that has the obesity rates of people in Boston and maps them to pools and "healthy corner stores" nearest to them. We want to see whether being close to either or both of these facilities reduce obesity rates, and could signal that there should be more of these facilities around.


## Project 2

With correlation_checkups_hospitals.py and correlation_pools_obesity.py, we want to find out if we are able to attribute certain behaviors, in this case annual check ups, to a characteristic of where one resides or how the number of swimming pools in one's proximity affects (if it does) obesity rates. 

In correlation_checkups_hospitals.py, we find the correlation coefficient and p-value between whether someone in Boston visited their doctor for an annual check up within the last year and their proximity to a hospital. We also give the user the option to restrict the distance from the hospital to see if there is a correlation between people who live within, say, a 1 mile radius of the hospital. Using this data, if there is a negative correlation between distance from the hospital and going to the doctors for an annual check up, we can determine whether people a given distance away from the hospital need to be given better access to their doctors.


In correlation_pools_obesity.py, we first find the number of pools within a user-given distance from a obesity rate data point. We then find the correlation coefficient and p-value between the number of pools around a given obesity rate data point and that data point's obesity rate. 

Both correlation1 and correlation2 give us a p-value, meaning we can determine whether the correlation is statistically significant (at least by current statistics standards) not only for the entire dataset but for slices of the data set, depending on the distance the user chooses. 
