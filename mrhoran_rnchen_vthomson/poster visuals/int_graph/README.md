int_graph README


For this interactive graph, we plotted the average distance to a theoretical bus yard against the k chosen for the kmeans calculation. We then calculated the standard deviations and stored them all in a .csv file, kmeans_stats.csv. Then, using Plotly and d3, we generated a scatterplot that displays the error bars using the calculated standard deviation. If you hover over any point with your cursor, it displays the k value, the average costs of students to the bus yards, and the error dynamically.


In order to get the plot, you must run a webserver, for the extent of our purposes, we just used an inbuilt python server, it can be called as follows:

python -m SimpleHTTPServer


This runs on localhost:8080, and if you go to:

localhost:8080/int_graph.html

the script should run in the browser (tested in chrome) 
