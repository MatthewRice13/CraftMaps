var infoWindow;
var map;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var directionsMap;
var start;
var end;
//staticurl
var currentURL = window.location.href;
var currentProtocol = window.location.protocol;
var currentHost = window.location.host;
//breweries data
var breweriesJson = Brewery_JSON;
var startlatitude = latstart;
var startlongitude = lngstart;

var startPoint = new google.maps.LatLng(startlatitude, startlongitude);
//document ready function
$(document).ready(function(){
	initMap();
	$("#goBackButton").on('click', function(){
		location.href = currentProtocol+'//'+currentHost+'/';  //staticUrl;
	});
	$('#refreshButton').on('click', function(){
		location.href = currentURL;   //staticUrl+'routes/' ;
	});
});//ready end

function initMap(){
	// Map options
	var options = {
		zoom:10,
		center: new google.maps.LatLng(startlatitude, startlongitude)
	}
	// New map
	map = new google.maps.Map(document.getElementById('map'), options);
	var userMarker = new google.maps.Marker({
		position: {lat: startlatitude, lng: startlongitude},
		title: 'You are here',
		map: map,
		icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
	});
	// Loop through for making markers
	for(var i = 0;i < breweriesJson.length;i++){
		// Add marker
		addMarker(breweriesJson[i]);
	}
}

// Add Marker Function
function addMarker(props){
	var marker = new google.maps.Marker({
		position: props.coords,
		animation: google.maps.Animation.DROP,
		title: props.name,
		map: map,
	});
	// Check for customicon
	if(props.iconImage){
		// Set icon image
		marker.setIcon(props.iconImage);
	}
	// Check content
	if(props.Content){
		marker.addListener('click', function(){
			if(typeof infoWindow != 'undefined'){
				infoWindow.close();
			}
			infoWindow = new google.maps.InfoWindow({
				content: props.Content
			});
			infoWindow.open(map, marker);
		});
	}
}

//directions on the right panel
function getDirections(lati,longi) {
	directionsDisplay = new google.maps.DirectionsRenderer();
	var directionsOptions = {
		zoom:10,
		center: new google.maps.LatLng(startlatitude, startlongitude)
	}
	calcRoute(lati,longi,"TRANSIT");
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
}

// show route on the map
function calcRoute(lati,longi,mode) {
	$("#refreshButton").show();
	end = {lat:lati,lng:longi};
	var request = {
		origin: new google.maps.LatLng(startlatitude, startlongitude),
		destination:end,
		travelMode: google.maps.TravelMode[mode]
	};
	directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			$("#directionsPanel").empty();
			$("#directionsPanel").css("background-image", 'url("../static/img/beer-decks2.jpg")');
			directionsDisplay.setDirections(result);
		}
		else if (status == google.maps.DirectionsStatus.ZERO_RESULTS){
			if(mode == "TRANSIT"){
			alert('Public Transport route does not exist, Driving route will be shown');
			getDirectionsDrive(lati,longi);
			}
			else if(mode == "DRIVING"){
				alert("No routes available");
				location.href = currentURL;
			}
		}
	});
}

//get driving route if public not available
function getDirectionsDrive(lati,longi) {
	directionsDisplay = new google.maps.DirectionsRenderer();
	var directionsOptions = {
		zoom:10,
		center: new google.maps.LatLng(startlatitude, startlongitude)
	}
	calcRoute(lati,longi,"DRIVING");
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
}

//show modal on click of the name of the brewery
function showModal(e){
	var breweryName = e.target.id;//console.log(urllink);
	//breweryName = breweryName.replace(/\s/g, '');
	breweryName = breweryName.trim();
	var urllink = currentProtocol+'//'+currentHost+'/brewery/'+breweryName;
	var ret = window.showModalDialog(urllink, "", "dialogWidth:80%;dialogHeight:80%");
}