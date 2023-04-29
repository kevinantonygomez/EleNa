// Initializes embedded map. setView([coordinates], zoom level). Coordinates set to Umass (Du Bois Library)
var map = L.map('map-div').setView([42.390074647680514, -72.52807366888675], 14);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
maxZoom: 19,
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
