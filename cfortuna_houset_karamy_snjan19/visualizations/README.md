# How to view the visualizations

First, retrieve all the data to visualize:

```
python3 retrieveData.py
python3 optimalHospitals.py
python3 optimalEMSStations.py
```

Then, run an HTTP server:

```
python -m SimpleHTTPServer 8000
```

Then, on `localhost:8000/visualizations` view:
- `ems.html` to view the first visualization that shows the routes from optimal and actual EMS locations to crash sites and
- `hospitals.html` to view the second visualization that allows you to filter the views of optimal and actual hospital locations near crash sites

