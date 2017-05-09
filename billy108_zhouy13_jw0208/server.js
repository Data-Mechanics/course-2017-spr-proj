const express = require('express');
const app = express();
const bodyParser = require('body-parser')
const MongoClient = require('mongodb').MongoClient

var db

MongoClient.connect('mongodb://billy108_zhouy13_jw0208:billy108_zhouy13_jw0208@localhost:27017/repo', (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(process.env.PORT || 3000, () => {
    console.log('listening on 3000')
  })
})

app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json())
app.use(express.static('public'))


app.get('/', (req, res) => {
  db.collection("billy108_zhouy13_jw0208.RecreatPlacesStats").find().toArray((err, result) => {
    if (err) return console.log(err)
    res.render('bubbles.ejs', {tdata: result})
  })
})

app.post('/histogram', (req, res) => {
  db.collection("billy108_zhouy13_jw0208.allRecreationalPlaces").find().toArray((err, result) => {
    if (err) return console.log(err)
//    console.log('saved to database')
    res.render('histogram.ejs', {tdata: result})
  })
})

app.post('/bubble', (req, res) => {
  db.collection("billy108_zhouy13_jw0208.RecreatPlacesStats").find().toArray((err, result) => {
    if (err) return console.log(err)
//    console.log('saved to database')
    res.render('bubbles.ejs', {tdata: result})
  })
})

// Note: request and response are usually written as req and res respectively.