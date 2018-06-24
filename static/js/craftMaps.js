var infoWindow;
var currentLat = 0.0;
var currentLng = 0.0;
var map;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var directionsMap;
//geolocation
//var geocoder = new google.maps.Geocoder();
var start;
var end;
var itenaryPoints = [];
var wayPt = [];
var img = "K:/UCD/sem 3/project/beermarkr.png"
//breweries data
var breweriesJson = [
	{
	  name: 'Wood Key Brewing',
	  coords:{lat:53.2989858,lng:-6.2603187},
	  //iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
	  //iconImage: img,
	  content:"<h1 class='hi'>WKB</h1>"
	},
	{
	  name: 'Rascals Brewing',
	  coords:{lat:53.2989858,lng:-6.4627311},
	 // iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
	  content:"<h1 class='hi'>RB</h1>"
	},
	{
	  name: 'Stone Barrel Brewing',
	  coords:{lat:53.3311481,lng:-6.2603187},
	 // iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
	  content:"<h1 class='hi'>SBB</h1>"
	}
];
//document ready function
$(document).ready(function(){
	getLocation();
	//populateBreweriesList();
	$("#getDirecButton").on('click', function(){
		//console.log("clicked");
		getDirections();
	});
	$("#getItenDirecButton").on('click', function(){
		//console.log("clicked");
		//getItenDirections();
		makeItenary();
	});
	$("#goToMaps").on('click', function(){
		//console.log("clicked");
		//getItenDirections();
		var loc = $("#enterLocation").val();
		//console.log(loc);
		if(loc == ""){
		    alert('No location entered! Your default location will be "The Spire Tower"');
		}
		getCoords(loc);
	});
	//initMap();
});//ready end


function populateBreweriesList(){
var listBrew = '';
	for(i=0; i < breweriesJson.length; i++){
		listBrew = "<li><input type='checkbox' name="+breweriesJson[i].coords.lng+" class='checkboxList' value="+ breweriesJson[i].coords.lat+">" + breweriesJson[i].name + "</li>"
		//console.log(listBrew);
		$("#listOfBreweries").append(listBrew);
	}
}


function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition);
	} else { 
		console.log('error')//x.innerHTML = "Geolocation is not supported by this browser.";
	}
	//initMap();
}
function showPosition(position) {
	//console.log(position.coords.latitude);
	currentLat = position.coords.latitude;
	//console.log(position.coords.longitude);
	currentLng = position.coords.longitude;
	/*x.innerHTML = "Latitude: " + position.coords.latitude + 
	"<br>Longitude: " + position.coords.longitude;*/
	startPoint = new google.maps.LatLng(currentLat, currentLng);
	initMap();
}
function initMap(){
	// Map options
	var options = {
		zoom:9,
		//center:{lat:53.3498,lng:-6.2603}
		//center:{lat:currentLat,lng:currentLng}
		//center: new google.maps.LatLng(currentLat, currentLng)
		// center = the spire tower
		center: new google.maps.LatLng(53.349722, -6.260278)
	}
	
	// New map
	//var map = new google.maps.Map(document.getElementById('map'), options);
	map = new google.maps.Map(document.getElementById('map'), options);
	
	// Listen for click on map
	/*google.maps.event.addListener(map, 'click', function(event){
		// Add marker
		addMarker({coords:event.latLng});
	});*/
	
	
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
		//icon:props.iconImage
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
//var wayPt = [];
/*for(i=0; i < itenaryPoints.length-1; i++){
	wayPt.push({"location":{"lat":itenaryPoints[i].location.lat,"lng":itenaryPoints[i].location.lng},"stopover":true});
}*/
//console.log(wayPt);

//this is not used because it includes the last location as well
/*for (wypoints in breweriesJson){//console.log(breweriesJson[wypoints].coords.lat);
	wayPt.push({"location":{"lat":breweriesJson[wypoints].coords.lat,"lng":breweriesJson[wypoints].coords.lng},"stopover":true});
	//wayPt.push({"location":{"lat":wypoints.coords.lat,"lng":wypoints.coords.lng},"stopover":true});
}*/
//var wayPoint = [{"location":{"lat":53.2989858,"lng":-6.2603187},"stopover":true},{"location":{"lat":53.3311481,"lng":-6.2603187},"stopover":true}];
function calcItenRoute() {
	//console.log("calcRoute");
	//var wayPt = [];
	console.log(itenaryPoints.length);
	for(i=0; i < itenaryPoints.length-1; i++){
		wayPt.push({"location":{"lat":itenaryPoints[i].location.lat,"lng":itenaryPoints[i].location.lng},"stopover":true});
	}
	//console.log(wayPt);
	start = startPoint;//directionsLatLng;
	end = {lat:itenaryPoints[itenaryPoints.length-1].location.lat,lng:itenaryPoints[itenaryPoints.length-1].location.lng}; //{lat:53.2989858,lng:-6.4627311};//"50 Rue Ste-Catherine O Montréal, QC H2X 1Z6";
	var request = {
		origin:start,
		destination:end,
		waypoints: wayPt,
		travelMode: google.maps.TravelMode.DRIVING
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
		/* send cordinate to the service*/
		//window.location ='';
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
				//console.log(startLat+' '+startLng);
				/* send cordinate to the service*/
				//window.location ='';
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