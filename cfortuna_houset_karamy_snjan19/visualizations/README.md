# How to view the visualizations

First, retrieve all the data to visualize:
```
python3 retrieveData.py
python3 optimalHospitals.py
python3 optimalEMSStations.py
```

Then, obtain an API key for the Google Maps API. And place it in `ems.html` and `hospitals.html` on line:
```
<script src="https://maps.google.com/maps/api/js?key=INSERT_API_KEY"></script>
```

Next, run an HTTP server:
```
python -m SimpleHTTPServer 8000
```

Lastly, on `localhost:8000/visualizations` view:
- `ems.html` to view the first visualization that shows the routes from optimal and actual EMS locations to crash sites and
- `hospitals.html` to view the second visualization that allows you to filter the views of optimal and actual hospital locations near crash sites

