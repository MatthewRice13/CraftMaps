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
//var staticUrl = "http://127.0.0.1:8000/";
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
		getCoords(loc,"routes/");
	});
	$("#goToMultiMaps").on('click', function(){
		var loc = $("#defaultAddress").val();
		if(loc == ""){
		    alert('No location entered! Your default location will be "The Spire Tower"');
		}
		getCoords(loc,"multiRoutes/");
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

/*function getCoords(address,newPage){
	var startLng = 0.0;
	var startLat = 0.0;
	if(address == ""){
		// default for spire tower
		startLat = 53.349722;
		startLng = -6.260278;
		postRequest(startLat,startLng,newPage)

	}
	else{
		axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
			params:{
			  address:address,
			  key:'AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8'
			}
		})
		.then(function(response){
			if(response.data.status === "OK"){
				if(response.data.results["0"].address_components[3].long_name != "Ireland"){
					alert("Enter a more detailed Irish Location");
				}
				else{
					startLat = response.data.results["0"].geometry.location.lat;
					startLng = response.data.results["0"].geometry.location.lng;
					var locCord= startLat+','+startLng;
					postRequest(startLat,startLng,newPage);

				}
			}
			else{
				//alert('Geocode was not successful for the following reason: ' + response.data.status);
				alert('You are not drunk yet! Please enter a valid location');
			}
		});
	}
}*/
function getCoords(address,newPage){
	var startLng = 0.0;
	var startLat = 0.0;
	if(address == ""){
		// default for spire tower
		startLat = 53.349722;
		startLng = -6.260278;
		postRequest(startLat,startLng,newPage)

	}
	else{
		axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
			params:{
			  address:address,
			  key:'AIzaSyDFK8QRiUl8jx5YYQwDMQ31GMyXwXz-et8'
			}
		})
		.then(function(response){
			if(response.data.status === "OK"){
				for(i=0; i<response.data.results["0"].address_components.length; i++){
					if(response.data.results["0"].address_components[i].long_name == "Ireland"){
						startLat = response.data.results["0"].geometry.location.lat;
						startLng = response.data.results["0"].geometry.location.lng;
						var locCord= startLat+','+startLng;
						postRequest(startLat,startLng,newPage);
						return;
					}
				}
				alert("Enter a more detailed Irish Location");
				/*if(response.data.results["0"].address_components[3].long_name != "Ireland"){
					alert("Enter a more detailed Irish Location");
				}*/
				/*else{
					startLat = response.data.results["0"].geometry.location.lat;
					startLng = response.data.results["0"].geometry.location.lng;
					var locCord= startLat+','+startLng;
					postRequest(startLat,startLng,newPage);

				}*/
			}
			else{
				//alert('Geocode was not successful for the following reason: ' + response.data.status);
				alert('You are not drunk yet! Please enter a valid location');
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
function postRequest(lati,longi,newPage){
	var csrftoken = getCookie('csrftoken');
	var url = currentURL+newPage;
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
}