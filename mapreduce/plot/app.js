var app = angular.module('plunker', []);

app.controller('MainCtrl', function($scope, $http) {
  vm = this;

  // Set the Map Options to be applied when the map is set.
  var mapOptions = {
    zoom: 11,
    scrollwheel: false,
    center: new google.maps.LatLng(40.7529, -73.9942),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    mapTypeControl: false,
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.TERRAIN]
    }
  }

  // Set a blank infoWindow to be used for each to state on click
  var infoWindow = new google.maps.InfoWindow({
    content: ""
  });

  // Set the map to the element ID and give it the map options to be applied
  vm.map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  // Create the state data layer and load the GeoJson Data
  var stateLayer = new google.maps.Data();
  stateLayer.loadGeoJson('https://raw.githubusercontent.com/jializhou/big-data-project/master/ny_with_color.geojson');

  // Set and apply styling to the stateLayer
  stateLayer.setStyle(function(feature) {
    return {
      fillColor: feature.getProperty('color'),
      strokeColor: feature.getProperty('color'),
      strokeWeight: 2,
    };
  });


  // Final step here sets the stateLayer GeoJSON data onto the map
  stateLayer.setMap(vm.map);

});