var infoWindow;
var currentLat = 0.0;
var currentLng = 0.0;
var map;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var directionsMap;
var start;
var end;
var itenaryPoints = [];
var wayPt = [];
var img = "Images/beer_PNG.png"

//staticurl
var currentURL = window.location.href;
var currentProtocol = window.location.protocol;
var currentHost = window.location.host;
//var staticUrl = "http://127.0.0.1:8000/";
//breweries data
var breweriesJson = Brewery_JSON;
//console.log(breweriesJson);
var startlatitude = latstart;
var startlongitude = lngstart;

var startPoint = new google.maps.LatLng(startlatitude, startlongitude);
//document ready function
$(document).ready(function(){
	//getLocation(); // will give the current position
	initMap();
	$("#goBackButton").on('click', function(){
		location.href = currentProtocol+'//'+currentHost+'/';  //staticUrl;
	});
	/*$("#getItenDirecButton").on('click', function(){
		var listLen = $('input[class="checkboxList"]:checked').length;
		console.log(listLen);
		if(listLen <= 1)
		{
			alert('Please select 2 or more breweries');
		}
		else{
			makeItenary();
		}
	});*/
	$('#refreshButton').on('click', function(){
		location.href = currentURL;   //staticUrl+'routes/' ;
	});
	//modal function calling
	/*$("headerLabel").on('click', function(e){
		var urllink= e.target.id;
		console.log(urllink);
		//var ret = window.showModalDialog("http://woodkeybrewing.ie/", "", "dialogWidth:80%;dialogHeight:80%");
	});*/
});//ready end

function populateBreweriesList(){
    var listBrew = '';
	for(i=0; i < breweriesJson.length; i++){
		listBrew = "<li><input type='checkbox' name="+breweriesJson[i].coords.lng
		    +" class='checkboxList' value="+ breweriesJson[i].coords.lat+">"
		    + breweriesJson[i].name + "</li>"
		$("#listOfBreweries").append(listBrew);
	}
}

function initMap(){
	// Map options
	var options = {
		zoom:10,
		//center: new google.maps.LatLng(currentLat, currentLng)
		center: new google.maps.LatLng(startlatitude, startlongitude)
		//center: startPoint
	}
	// New map
	map = new google.maps.Map(document.getElementById('map'), options);
	//{lat: 53.3471532, lng: -6.2603187}
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
	populateBreweriesList();
}

// Add Marker Function
function addMarker(props){//console.log(props.coords);
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

function calcRoute(lati,longi,mode) {
	$("#refreshButton").show();
	end = {lat:lati,lng:longi};
	var request = {
		origin: new google.maps.LatLng(startlatitude, startlongitude),
		destination:end,
		travelMode: google.maps.TravelMode[mode]
	};
	directionsService.route(request, function(result, status) {//console.log(result);
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

/*function makeItenary(){
	wayPt = [];
	itenaryPoints = [];
	//itenaryPoints.push({"location":{"lat":startlatitude,"lng":startlongitude}});
	$('input[class="checkboxList"]:checked').each(function() {
		var lati = parseFloat(this.value);
		var longi = parseFloat(this.name);
		itenaryPoints.push({"location":{"lat":lati,"lng":longi}});
	});
	//console.log(itenaryPoints);
	getItenDirections();
}*/

/*function getItenDirections() {
	$("#directionsPanel").empty();
	$("#directionsPanel").css("background-color", "white");
	directionsDisplay = new google.maps.DirectionsRenderer();
	var directionsOptions = {
		zoom:10,
		center: new google.maps.LatLng(startlatitude, startlongitude)
	}
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
	calcItenRoute();
}*/

/*function calcItenRoute() {
	//console.log(itenaryPoints.length);
	$("#refreshButton").show();
	for(i=0; i < itenaryPoints.length-1; i++){
		wayPt.push({"location":{"lat":itenaryPoints[i].location.lat,"lng":itenaryPoints[i].location.lng},"stopover":true});
	}
	//console.log(wayPt);
	start = new google.maps.LatLng(startlatitude, startlongitude);
	end = {lat:itenaryPoints[itenaryPoints.length-1].location.lat,lng:itenaryPoints[itenaryPoints.length-1].location.lng};
	var request = {
		origin: start,
		destination: end,
		waypoints: wayPt,
		travelMode: google.maps.TravelMode.DRIVING
	};
	directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
		directionsDisplay.setDirections(result);
		}
	});
}*/

function showModal(e){
	var urllink = e.target.id;//console.log(urllink);
	var ret = window.showModalDialog(urllink, "", "dialogWidth:80%;dialogHeight:80%");
}