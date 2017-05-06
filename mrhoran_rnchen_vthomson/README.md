
PROJECT 2 Writeup:

  ** note trial is set to true for both transfromation_one_bus.py and transformation_two_bus.py
  ** All data is collected in the getbusData.py
  ** we are using the simulated students geojson file in the input data dir
  
  For this part of the project, we began to analyze the Boston Public School project. We wanted to focus on where students and schools are   located relative to busyards. There are a bunch of transformations to be fix this problem but for now we tackled two to get some 
  meaningful data.
  
  For our first transformation, we wanted to look at clustering of schools to find the hubs where the schools are located. We thought  
  this would be meanignful to see where the most schools are congregating, which could possibly influence where busyards are located or 
  potentially used to optimize bus routes around these hubs. So this optimization used Kmeans on the schools address: there are 89 
  coordinates in the schools.json file. So using this we wanted to test how many Ks or means gives us the best cost for the least amount 
  of means. In other words, we wanted to find how many means gave us the best distance to all the points. We found that about half the 
  number of points for means gaves us the best optimization, after that there was no dramatic benefit to the distance cost. This is 
  represented in the graph in kmeans_schools.png, where the means range from 1 to 89 ( the # of schools). In the trial mode, it is run on 
  half the data, taking a few seconds. So in our database we put 44 means into the database to show the school hubs. 
  
  In the second transformation, we wanted to do a statistical analysis of the average distance between students. This data would be useful 
  for buses to see how far they would have to travel between stops on average, in order for them to envision timing. Also, it would show  
  us where to place optimal bus stops for students, and the data is malleable to group students by different end and start times for  
  schools. In this transformation we use an rtree to do two groups: one grouping getting the average of the closest 10 students per 
  student, and one grouping based on the average distance in a .5 mile radius. We found the distance using vincenty distance, which takes 
  into account the earth's shape to find distance between coordinates. In trial mode, with the code split into 16ths, it runs in roughly 8 
  seconds. For the full set it will take 20 ish minutes. The sample outputs of the analysis are printed at the end.
  
