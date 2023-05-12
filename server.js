const express = require('express');
const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );

const app = express();
const port = 3000;
app.set('json spaces', 2)
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public_html"));

var routeType = null; // store selected route type. null by default
var elevationGainType = "maximize"; // store selected elevation gain type. maximize by default
var maxDist = 0; // store max distance %. 0 by default


/*
Sets route type
*/
app.post('/set/route/type', function (req, res) {
  if (req.body.length == 0){
    res.status(400).send("noBody");
  }
  if (req.body.routeType == ""){
    routeType = null;
  }
  else{
    routeType = req.body.routeType;
  }
  res.status(200).send("success");
});


/*
Sends route type
*/
app.post('/get/route/type', function (req, res) {
  res.status(200).send({routeType: routeType});
});


/*
Sets gain type
*/
app.post('/set/gain/type', function (req, res) {
  if (req.body.length == 0){
    res.status(400).send("noBody");
  }
  elevationGainType = req.body.gainType;
  res.status(200).send("success");
});


/*
Sets max disance %
*/
app.post('/set/max/distance', function (req, res) {
  if (req.body.length == 0){
    res.status(400).send("noBody");
  }
  maxDist = req.body.maxDist;
  res.status(200).send("success");
});


/*
Sends info to flask backend to generate route.

*/
app.post('/get/route', function (req, res) {
  if (req.body.length == 0){
    res.status(400).send("noBody");
  }

  const data = {
    startLocation: req.body.data.startLocation,
    stopLocation: req.body.data.stopLocation,
    routeType: routeType,
    elevationGainType: elevationGainType,
    maxDist: maxDist
  };

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/get_route",
    data: JSON.stringify(data),
    contentType: "application/json",
    success: function(response) {
      console.log(response);
      res.status(200).send("success");
    },
    error: function(xhr, status, error) {
      console.error('Error:', error);
      res.status(400).send("error");
    }
  });

});



//respond to all other requests by displaying main webpage
app.use('/',express.static("public_html"));
app.listen(port, () =>
  console.log(`App listening at http://127.0.0.1:${port}`))
