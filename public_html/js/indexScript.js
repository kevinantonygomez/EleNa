var searchWidgetStart; // store current start location
var searchWidgetStop; // store current stop location


/*
Embeds map on document load
Must set API Key below
Get key from: https://developers.arcgis.com/
*/
function initEsri(searchTerm1, searchTerm2){
  const apiKey = "YOUR_API_KEY" // Set API Key
  require(["esri/config", "esri/Map", "esri/views/MapView", "esri/widgets/Search"], function(esriConfig, Map, MapView, Search){

    esriConfig.apiKey = apiKey;

    const map = new Map({
      basemap: "arcgis-navigation"
    });

    const view = new MapView({
      map: map,
      center: [-72.52807366888675,42.390074647680514], // latitude, longitude (set to Umass (Du Bois library))
      zoom: 12,
      container: "map-div" // div id of container
    });

    searchWidgetStart = new Search({
      id: "start-search",
      view: view, // zooms in on searched address on map
      container: "start-search-div"
    });

    searchWidgetStop = new Search({
      container: "stop-search-div"
    });

  });
}



/*
Swaps start and stop addresses when swap button is clicked. Automatically updates maps
*/
function swapAddresses(){
  var tmp = document.getElementById("start-search-input").value;
  searchWidgetStart.searchTerm = document.getElementById("stop-search-div-input").value;
  searchWidgetStop.searchTerm = tmp;
  searchWidgetStart.search();
}


/*
Displays modal for max distance info button
*/
function showInfoModal(){
  const modal = document.getElementById('modal');
  modal.style.display = 'block';
}


/*
Hides modal for max distance info button
*/
function hideInfoModal(){
  const modal = document.getElementById('modal');
  modal.style.display = 'none';
}


/*
Callback function to get route type from server. Called by getRoute()
*/
function getRouteType(callback){
  $.ajax({
    url: '/get/route/type',
    method: 'POST',
    success: function(response) {
      callback(response);
    },
    error: function(xhr, status, error) {
      console.log('An error occurred: ', error);
    }
  });
}


/*
Handles selection of route type. Sets selected route button to active and rest
to inactive. Sends selected route to server.
*/
function setRouteType(thisBtn, transportBtns){
  var routeType = null;

  if (thisBtn.className == "inactiveRoute"){
    for (let i = 0; i < transportBtns.length; i++){
      if (transportBtns[i] != thisBtn){
        transportBtns[i].className = "inactiveRoute"
      }
      else{
        transportBtns[i].className = "activeRoute"
        routeType = transportBtns[i].getAttribute('id');
      }
    }
  }
  else{
    for (let i = 0; i < transportBtns.length; i++){
      transportBtns[i].className = "inactiveRoute"
    }
  }

  $.ajax({
    url: '/set/route/type',
    method: 'POST',
    data: {routeType:routeType}
  })
  .done(function(data, statusText, xhr){
    if(xhr.status != 200) {
      if(xhr.responseText == "noBody"){
        console.log("noBody");
      }
    }
  });
}


/*
Handles selection of gain type (max or min). Sends selected gain type to server.
*/
function setGainType(thisBtn){
  $.ajax({
    url: '/set/gain/type',
    method: 'POST',
    data: {gainType:thisBtn.value}
  })
  .done(function(data, statusText, xhr){
    if(xhr.status != 200) {
      if(xhr.responseText == "noBody"){
        console.log("noBody");
      }
    }
  });
}


/*
Handles setting of maximum distance value. Sends selected distance to server.
*/
function setMaxDist(){
  maxDistVal = document.getElementById("distance-input").value;
  if ((maxDistVal < 0) || (maxDistVal > 100) ){  // Must handle exp *****
    alert("Max Distance must be between 0 and 100");
    return;
  }
  $.ajax({
    url: '/set/max/distance',
    method: 'POST',
    data: {maxDist:maxDistVal}
  })
  .done(function(data, statusText, xhr){
    if(xhr.status != 200) {
      if(xhr.responseText == "noBody"){
        console.log("noBody");
      }
    }
  });
}


/*
Sends required info to python back end to generate a route. Sends start/stop
addresses to server which further appends other info prior to communicating with
flask app.
*/
function getRoute(){
  startLocation = searchWidgetStart.searchTerm
  stopLocation = searchWidgetStop.searchTerm

  if ((startLocation.length == 0)||(stopLocation.length == 0)){
    alert("Please enter a start and stop location");
    return;
  }

  getRouteType(function(routeTypeJSON) {
    if (routeTypeJSON.routeType == null){
      alert("Please choose a route type");
      return;
    }
    data = {
      startLocation: startLocation,
      stopLocation: stopLocation,
    }

    $.ajax({
      url: '/get/route',
      method: 'POST',
      data: {data:data}
    })
    .done(function(data, statusText, xhr){
      if(xhr.status != 200) {
        console.log(xhr.responseText);
      }
    });
  });

}


document.body.addEventListener("load", initEsri(null, null));

window.addEventListener('DOMContentLoaded', function() {
  document.getElementById("swap-btn").addEventListener("click", swapAddresses);
  document.getElementById("info-btn").addEventListener("click", showInfoModal);
  document.getElementById("close-modal").addEventListener("click", hideInfoModal);
  document.getElementById("go-btn").addEventListener("click", getRoute);

  var transportBtns = document.querySelectorAll('#transport-select-div button');
  transportBtns.forEach(function(thisBtn) {
  thisBtn.addEventListener("click", function() {
    setRouteType(thisBtn, transportBtns);
    });
  });

  var gainBtns = document.getElementsByName("gain-radio");
  gainBtns.forEach(function(thisBtn) {
  thisBtn.addEventListener("change", function() {
    setGainType(thisBtn);
    });
  });

  document.getElementById("distance-input").addEventListener("change", setMaxDist);
});
