var http = require('http');
var fs = require('fs');
var d3 = require("d3");

var html = fs.readFileSync('test.html');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(html);
}).listen(8888);