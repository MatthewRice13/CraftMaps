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
//start point
//var startPoint;
//staticurl
var staticUrl = "http://127.0.0.1:8000/";
//var img = "K:/UCD/sem 3/project/beermarkr.png"

//breweries data
var breweriesJson = Brewery_JSON;
//console.log(breweriesJson[0].coords.lng);
//console.log(breweriesJson);

//document ready function
$(document).ready(function(){
	//getLocation(); // will give the current position
	initMap();
	$("#getDirecButton").on('click', function(){
		getDirections();
	});
	$("#getItenDirecButton").on('click', function(){
		makeItenary();
	});
	$("#goToMaps").on('click', function(){
		var loc = $("#defaultAddress").val();
		if(loc == ""){
		    alert('No location entered! Your default location will be "The Spire Tower"');
		}
		getCoords(loc);
	});
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
/*get current location*/
/*function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition);
	} else {
		console.log('error');
	}
}*/

/*set start point*/
/*function showPosition(position) {
	currentLat = position.coords.latitude;
	currentLng = position.coords.longitude;
	startPoint = new google.maps.LatLng(currentLat, currentLng);
	initMap();
}*/

function initMap(){
	// Map options
	var options = {
		zoom:9,
		//center: new google.maps.LatLng(currentLat, currentLng)
		//setting center as the spire tower
		center: new google.maps.LatLng(53.349722, -6.260278)
	}
	// New map
	map = new google.maps.Map(document.getElementById('map'), options);

	// Loop through for making markers
	for(var i = 0;i < breweriesJson.length;i++){
		// Add marker
		addMarker(breweriesJson[i]);
	}
	populateBreweriesList();
}

// Add Marker Function
function addMarker(props){
	var marker = new google.maps.Marker({
		position: props.coords,
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

/*function getDirections(lati,longi) {
	$("#directionsPanel").empty();
	directionsDisplay = new google.maps.DirectionsRenderer();
	var directionsOptions = {
		zoom:10,
		center: startPoint
	}
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
	calcRoute(lati,longi);
}*/

/*function calcRoute(lati,longi) {
	start = startPoint;
	end = {lat:lati,lng:longi};
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
}*/

/*function getItenDirections() {
	$("#directionsPanel").empty();
	directionsDisplay = new google.maps.DirectionsRenderer();
	var directionsOptions = {
		zoom:10,
		center: startPoint
	}
	directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
	directionsDisplay.setMap(directionsMap);
	directionsDisplay.setPanel(document.getElementById("directionsPanel"));
	calcItenRoute();
}*/

/*function calcItenRoute() {
	console.log(itenaryPoints.length);
	for(i=0; i < itenaryPoints.length-1; i++){
		wayPt.push({"location":{"lat":itenaryPoints[i].location.lat,"lng":itenaryPoints[i].location.lng},"stopover":true});
	}
	console.log(wayPt);
	start = startPoint;
	end = {lat:itenaryPoints[itenaryPoints.length-1].location.lat,lng:itenaryPoints[itenaryPoints.length-1].location.lng};
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
}*/

/*function makeItenary(){
	wayPt = [];
	itenaryPoints = [];
	$('input[class="checkboxList"]:checked').each(function() {
		var lati = parseFloat(this.value);
		var longi = parseFloat(this.name);
		itenaryPoints.push({"location":{"lat":lati,"lng":longi}});
		//console.log(itenaryPoints);
	});
	getItenDirections();
}*/

function getCoords(address){console.log(address)
	var startLng = 0.0;
	var startLat = 0.0;
	if(address == ""){
		// default for spire tower
		startLat = 53.349722;
		startLng = -6.260278;
		// set startpoint for second page
		//startPoint = new google.maps.LatLng(startLat, startLng);
		//console.log(startLat+' '+startLng);
		/* send cordinate to the service*/
		//window.location =staticUrl+'routes/'+startLat+','+startLng;
		//var locCord= startLat+','+startLng;
		//postRequest(locCord);
		postRequest(startLat,startLng)

	}
	else{
		axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
			params:{
			  address:address,
			  key:'AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8'
			}
		})
		.then(function(response){
			//console.log(response);
			//console.log(response.data.status);
			if(response.data.status === "OK"){
				if(response.data.results["0"].address_components[3].long_name != "Ireland"){
					alert("Enter a more detailed Irish Location");
				}
				else{
					startLat = response.data.results["0"].geometry.location.lat;
					startLng = response.data.results["0"].geometry.location.lng;
					// set startpoint for second page
					//startPoint = new google.maps.LatLng(startLat, startLng);
					//console.log(startLat+' '+startLng);
					/* send cordinate to the service*/
					//window.location ='';
					//window.location =staticUrl+'routes/'+startLat+','+startLng;
					var locCord= startLat+','+startLng;
					//postRequest(locCord);
					postRequest(startLat,startLng);

				}
				/*startLat = response.data.results["0"].geometry.location.lat;
				startLng = response.data.results["0"].geometry.location.lng;
				console.log(startLat+' '+startLng);*/
			}
			else{
				alert('Geocode was not successful for the following reason: ' + response.data.status);
			}
		});
	}
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
function postRequest(lati,longi){
	var csrftoken = getCookie('csrftoken');
	var url = staticUrl+'routes/';
	var postdata={
		'value1':lati,
		'value2':longi,
		'csrfmiddlewaretoken': csrftoken
	};
	
	$.ajax({
		url: url,
		type: "POST",
		data: postdata,
		success: function(data) {
			window.location = url;
		}
	});
	/*$.post(url,postdata,function(data,status){
		//console.log(url);
		if(status == 'success')
		{
			window.location = staticUrl+'routes/';
		}
		else{
			alert(error)
		}
	});*/
}