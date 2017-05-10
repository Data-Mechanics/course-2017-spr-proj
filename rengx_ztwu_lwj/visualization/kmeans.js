
  var map;

  /*42.2820028,-71.0871498*/
  function initMap() {
    document.getElementById('right').innerHTML='<div id="z0"></div><div id="z1"></div><div id="z2"></div><div id="z3"></div><div id="z4"></div><div id="z5"></div><div id="z6"></div>';
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: new google.maps.LatLng(42.3223948,-71.0943483),
      mapTypeId: 'roadmap'
    });

    var iconUrl = 'http://maps.google.com/mapfiles/kml/pushpin/';
    var colortxt = ['blue', 'grn', 'ltblu', 'purple', 'pink', 'ylw', "wht"];
    var colortxt_stars = ['blu', 'grn', 'ltblu', 'purple', 'pink', 'ylw', "wht"];
    var cluster = document.getElementById('cluster').value;
    var hcounter = 0;
    $.ajax({
        url: "http://datamechanics.io/data/rengx_ztwu_lwj/km" + cluster + ".json",
        success: function (data) {
            var obj = JSON.parse(data);
            var c1 = [];
                c2 = [];
                c3 = [];
                c4 = [];
                c5 = [];
                c6 = [];
                c7 = [];
                cs = [c1,c2,c3,c4,c5,c6,c7];
                avgs = [];
                amounts = [];
            obj.forEach(function(i){
                var cid = parseInt(i.cid);
                cs[cid].push(i)
            });
            var counter = 0
            cs.forEach(function(c){
              var sum = 0;
              for( var i = 0; i < c.length; i++ ){
                  sum += parseInt( c[i].access_score, 10 );
              }
              var avg = sum/c.length;
              avgs.push(avg.toFixed(2));
              amounts.push(c.length);
              c.sort(function(a, b) {
                return parseFloat(b.access_score) - parseFloat(a.access_score);
              });
              cs[counter] = c.slice(0,3);
              counter += 1;
            });

            obj.sort(function(a, b) {
              return parseFloat(b.access_score) - parseFloat(a.access_score);
            });

            data = [];
            obj.forEach(function(s) {
              var x = s.x/(1.0*1000000);
              var y = s.y/(-1.0*1000000);
              var name = s.name;
              var addr = s.addr;
              var zipp = s.zipp;
              var cid = parseInt(s.cid);
              var score = s.access_score;
              var txt = name + "<br>" + addr + "<br>" + zipp + "<br>Position: " + x + ", " + y + "<br><b>Score: " + score + "</b>";
              var image = {
                url: iconUrl + colortxt[cid] + '-pushpin.png',
                size: new google.maps.Size(32, 32),
                scaledSize: new google.maps.Size(32, 32)
              };

              var marker = new google.maps.Marker({
                  position: new google.maps.LatLng(x, y),
                  icon: image,
                  map: map
                });
              var infowindow = new google.maps.InfoWindow({
                  content: txt,
                  extra: s.name
                });


              google.maps.event.addListener(marker, 'mouseover', (function () {
                  infowindow.open(map, marker);
                }));
              google.maps.event.addListener(marker, 'mouseout', (function () {
                  infowindow.close();
                }));


              cs[cid].forEach(function(t){
                if(s.name == t.name){
                  var imageH = {
                    url: 'http://maps.google.com/mapfiles/kml/paddle/' + colortxt_stars[cid] + '-stars.png',
                    size: new google.maps.Size(50, 50),
                    scaledSize: new google.maps.Size(50, 50)
                  };
                  marker.setIcon(imageH);
                  var fid = "z" + cid;
                  var zone = document.getElementById(fid);
                  if (zone.innerHTML=="") {
                    zone.style.display="block";
                    zone.innerHTML = "<p class='zones'>Zone " + (cid+1) + ": </p>" +
                                     "<p class='det'>Average Score of Zone: " + avgs[cid] + "</p>" +
                                     "<p class='det'>Number of Schools: " + amounts[cid] + "</p>";
                  }
                  var hid = "hid" + hcounter;
                  hcounter += 1;
                  var item = document.createElement('a');
                  item.id = hid;
                  item.href = "#";
                  item.class = "tops";
                  item.innerHTML = t.name;
                  item.addEventListener('mouseover', (function () {
                      infowindow.open(map, marker);
                  }));
                  item.addEventListener('mouseout', (function () {
                      infowindow.close();
                  }));
                  zone.appendChild(item);
                  var br = document.createElement('br');
                  zone.appendChild(br);
                }
              });
            }); /*end of for each*/
        }
    });

  }

  document.getElementById('sbtn').addEventListener('click', (function () {
    initMap();
  }));
