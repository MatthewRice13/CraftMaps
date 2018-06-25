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
var img = "K:/UCD/sem 3/project/beermarkr.png"

//breweries data
var breweriesJson = Brewery_JSON;
console.log(breweriesJson);

//document ready function
$(document).ready(function(){
	getLocation();
	$("#getDirecButton").on('click', function(){
		getDirections();
	});
	$("#getItenDirecButton").on('click', function(){
		makeItenary();
	});
	$("#goToMaps").on('click', function(){
		var loc = $("#defaultAddress").val();
		getCoords(loc);
	});
});

function populateBreweriesList(){
    var listBrew = '';
	for(i=0; i < breweriesJson.length; i++){
		listBrew = "<li><input type='checkbox' name="+breweriesJson[i].coords.lng
		    +" class='checkboxList' value="+ breweriesJson[i].coords.lat+">"
		    + breweriesJson[i].name + "</li>"
		console.log(listBrew);
		$("#listOfBreweries").append(listBrew);
	}
}

function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition);
	} else {
		console.log('error')//x.innerHTML = "Geolocation is not supported by this browser.";
	}
}

function showPosition(position) {
	currentLat = position.coords.latitude;
	currentLng = position.coords.longitude;
	startPoint = new google.maps.LatLng(currentLat, currentLng);
	initMap();
}

function initMap(){
	// Map options
	var options = {
		zoom:10,
		center: new google.maps.LatLng(currentLat, currentLng)
	}
	// New map
	map = new google.maps.Map(document.getElementById('map'), options);

	// Loop through markers
	for(var i = 0;i < breweriesJson.length;i++){
		// Add marker
		addMarker(breweriesJson[i]);
	}
	populateBreweriesList();
}

// Add Marker Function
function addMarker(props){
	var marker = new google.maps.Marker({
		position:props.coords,
		title: props.name,
		map:map,
	});

	// Check for customicon
	if(props.iconImage){
		// Set icon image
		marker.setIcon(props.iconImage);
	}

	// Check content
	if(props.content){
		marker.addListener('click', function(){
			if(typeof infoWindow != 'undefined'){
				infoWindow.close();
			}
			infoWindow = new google.maps.InfoWindow({
				content:props.content
			});
			infoWindow.open(map, marker);
		});
	}
}

function getDirections() {
	//$("#map").empty();
	$("#directionsPanel").empty();
	//console.log('getDirections');
	directionsDisplay = new google.maps.DirectionsRenderer();
	//start = new google.maps.LatLng(directionsLatLng);
	var directionsOptions = {
		zoom:10,
		center: startPoint
	}
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
	calcRoute();
}

function calcRoute() {
	//console.log("calcRoute");
	start = startPoint;//directionsLatLng;
	end = {lat:53.2989858,lng:-6.4627311};//"50 Rue Ste-Catherine O Montréal, QC H2X 1Z6";
	var request = {
		origin:start,
		destination:end,
		travelMode: google.maps.TravelMode.TRANSIT
	};
	directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
		directionsDisplay.setDirections(result);
		}
	});
}

function getItenDirections() {
	//$("#map").empty();
	$("#directionsPanel").empty();
	//console.log('getDirections');
	directionsDisplay = new google.maps.DirectionsRenderer();
	//start = new google.maps.LatLng(directionsLatLng);
	var directionsOptions = {
		zoom:10,
		center: startPoint
	}
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
	calcItenRoute();
}

function calcItenRoute() {
	//console.log("calcRoute");
	//var wayPt = [];
	console.log(itenaryPoints.length);
	for(i=0; i < itenaryPoints.length-1; i++){
		wayPt.push({"location":{"lat":itenaryPoints[i].location.lat,"lng":itenaryPoints[i].location.lng},"stopover":true});
	}
	console.log(wayPt);
	start = startPoint;//directionsLatLng;
	end = {lat:itenaryPoints[itenaryPoints.length-1].location.lat,lng:itenaryPoints[itenaryPoints.length-1].location.lng}; //{lat:53.2989858,lng:-6.4627311};//"50 Rue Ste-Catherine O Montréal, QC H2X 1Z6";
	var request = {
		origin:start,
		destination:end,
		waypoints:wayPt,
		travelMode:google.maps.TravelMode.DRIVING
	};
	directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
		directionsDisplay.setDirections(result);
		}
	});
}

function makeItenary(){
	wayPt = [];
	itenaryPoints = [];
	$('input[class="checkboxList"]:checked').each(function() {
		var lati = parseFloat(this.value);//console.log(lati);
		var longi = parseFloat(this.name);//console.log(longi);
		itenaryPoints.push({"location":{"lat":lati,"lng":longi}});
		//itenaryPoints.push({"location":{"lat":lati,"lng":longi},"stopover":true});
		console.log(itenaryPoints);
		//console.log(wayPt);
		/*console.log(this.value);
		console.log(this.name);*/
	});
	getItenDirections();
}

function getCoords(address){
	var startLng = 0.0;
	var startLat = 0.0;
	if(address == ""){
		// default for spire tower
		startLat = 53.349722;
		startLng = -6.260278;
		//console.log(startLat+' '+startLng);
	}
	else{
		axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
			params:{
			  address:address,
			  key:'AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8'
			}
		})
		.then(function(response){
			//console.log(response.data.status);
			//console.log(response);
			if(response.data.status === "OK"){
				startLat = response.data.results["0"].geometry.location.lat;
				startLng = response.data.results["0"].geometry.location.lng;
				//console.log(startLat+' '+startLng);
			}
			else{
				alert('Geocode was not successful for the following reason: ' + response.data.status);
			}
		});
	}
}
