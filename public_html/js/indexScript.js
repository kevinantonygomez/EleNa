/*
Embeds map on document load
Must set API Key below
Get key from: https://developers.arcgis.com/
*/

var searchWidgetStart;
var searchWidgetStop;

function initEsri(searchTerm1, searchTerm2){
  const apiKey = "Your_API_KEY"
  require(["esri/config", "esri/Map", "esri/views/MapView", "esri/widgets/Search"], function(esriConfig, Map, MapView, Search){

    esriConfig.apiKey = apiKey; // Set API Key

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

function swapAddresses(){
  var tmp = document.getElementById("start-search-input").value;
  searchWidgetStart.searchTerm = document.getElementById("stop-search-div-input").value;
  searchWidgetStop.searchTerm = tmp;
  searchWidgetStart.search();
}

function showInfoModal(){
  const modal = document.getElementById('modal');
  modal.style.display = 'block';
}

function hideInfoModal(){
  const modal = document.getElementById('modal');
  modal.style.display = 'none';
}

document.body.addEventListener("load", initEsri(null, null));
document.getElementById("swap-btn").addEventListener("click", swapAddresses);
document.getElementById("info-btn").addEventListener("click", showInfoModal);
document.getElementById("close-modal").addEventListener("click", hideInfoModal);
