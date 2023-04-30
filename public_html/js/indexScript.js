/*
Embeds map on document load
Must set API Key below
Get key from: https://developers.arcgis.com/
*/
function initEsri(){
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

    var searchWidgetStart = new Search({
      id: "start-search",
      view: view, // zooms in on searched address on map
      container: "start-search-div"
    });

    var searchWidgetStop = new Search({
      container: "stop-search-div"
    });

  });
}

document.body.addEventListener("load", initEsri());
