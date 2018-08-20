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
var currentlatitude = latstart;
var currentlongitude = lngstart;
var downloadText = '';
var tripCounter = 1;

var startPoint = new google.maps.LatLng(startlatitude, startlongitude);
//document ready function
$(document).ready(function(){
	
	initMap();
	$("#goBackButton").on('click', function(){
		location.href = currentProtocol+'//'+currentHost+'/';  
	});
	$('#refreshButton').on('click', function(){
		location.href = currentURL;
	});
	$('#downloadFile').on('click', function(){
		downloadPDF();
	});
	//flags for brewery numbers
	for(b=1;b<=breweriesJson.length;b++)
	{
		var str = "flag"+b+"=false";
		eval(str);
	}
});//ready end

// dynamically create brewery buttons
function populateBreweriesList(){
    var listBrew = '';
	var buttonListBrew = '';
	var startPointButton = "<button class='btn btn-outline auto-btn' type='button' onClick='showDirections("+startlatitude+","+startlongitude+")'>Start Point</button><br><br>";
	$("#listOfBreweries").append(startPointButton);
	for(i=0; i < breweriesJson.length; i++){
		var number = i+1;
		buttonListBrew = "<button class='btn btn-outline auto-btn' type='button' onClick='checkForItenary("+breweriesJson[i].coords.lat+","+breweriesJson[i].coords.lng+","+number+")'>"+number+": "+breweriesJson[i].name+"</button><br>";
		$("#listOfBreweries").append(buttonListBrew);
	}
}

function initMap(){
	// Map options
	var options = {
		zoom:10,
		center: new google.maps.LatLng(startlatitude, startlongitude)
		//center: startPoint
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
	populateBreweriesList();
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
// show modal on click of brewery name
function showModal(e){
	var breweryName = e.target.id;
	breweryName = breweryName.trim();
	var urllink = currentProtocol+'//'+currentHost+'/brewery/'+breweryName;
	var ret = window.showModalDialog(urllink, "", "dialogWidth:80%;dialogHeight:80%");
}
// function to check if the brewery is already added in the itinerary
function checkForItenary(lati,longi,num){
	for(a=1;a<=breweriesJson.length;a++){
		if(num == a){
			if(eval("flag"+a)){
				alert("This brewery is already added to the itenary.");
			}
			else{
				showDirections(lati,longi);
				var str = "flag"+a+"=true";
				eval(str);
			}
		}
	}
}
// show directions on the right panel
function showDirections(lati,longi){
	if(lati == currentlatitude && longi == currentlongitude){
		alert('You are already on the clicked position. Please clicked on another option');
	}
	else{
		directionsDisplay = new google.maps.DirectionsRenderer();
		var directionsOptions = {
			zoom:10,
			center: new google.maps.LatLng(currentlatitude, currentlongitude)
		}
		showRoute(lati,longi,"TRANSIT");
		directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
		directionsDisplay.setMap(directionsMap);
		directionsDisplay.setPanel(document.getElementById("directionsPanel"));
		
	}
}

// show routes on the map
function showRoute(lati,longi,mode) {
	$("#refreshButton").show();
	$("#downloadFile").show();
	var directionRoute;
	var directionText = '';
	end = {lat:lati,lng:longi};
	var request = {
		origin: new google.maps.LatLng(currentlatitude, currentlongitude),
		destination:end,
		travelMode: google.maps.TravelMode[mode]
	};
	directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			directionsDisplay.setDirections(result);
			directionRoute = result.routes["0"].legs["0"].steps;
			for(i=0;i<directionRoute.length;i++){
				directionText = directionText + directionRoute[i].instructions+"\n";
				for(var x in directionRoute[i]){
					if(x=="steps"){
						for(j=0;j<directionRoute[i].steps.length;j++){
							directionText = directionText + directionRoute[i].steps[j].instructions+"\n";
						}
					}
				}
			}
			prepareText(directionText);
			$("#directionsPanel").empty();
			$("#directionsPanel").css("background-image", 'url("../static/img/beer-decks2.jpg")');
			currentlatitude = lati;
			currentlongitude = longi;
		}
		else if (status == google.maps.DirectionsStatus.ZERO_RESULTS){
			if(mode == "TRANSIT"){
			alert('Public Transport route does not exist, Driving route will be shown');
			showDirectionsDrive(lati,longi);
			}
			else if(mode == "DRIVING"){
				alert("Sorry, No routes available");
				location.href = currentURL;
			}
		}
	});
}

//directions for driving option if public not available
function showDirectionsDrive(lati,longi){
	if(lati == currentlatitude && longi == currentlongitude){
		alert('You are already on the clicked position. Please clicked on another option');
	}
	else{
		directionsDisplay = new google.maps.DirectionsRenderer();
		var directionsOptions = {
			zoom:10,
			center: new google.maps.LatLng(currentlatitude, currentlongitude)
		}
		showRoute(lati,longi,"DRIVING");
		directionsMap = new google.maps.Map(document.getElementById('map'), directionsOptions);
		directionsDisplay.setMap(directionsMap);
		directionsDisplay.setPanel(document.getElementById("directionsPanel"));
		
	}
}

// prepare HTML text for the PDF
function prepareText(directions){
	var directionDetails = "<b>TRIP "+tripCounter+":</b>"+"<div>";
	directionDetails = directionDetails + directions+"</div>"
	tripCounter = tripCounter+1;
	downloadText = downloadText + directionDetails;
}
//download the PDF file
function downloadPDF(){
	var specialElementHandlers = {
		'#editor': function (element, renderer) {
			return true;
		}
	};
	var pdf = new jsPDF('p', 'pt', 'a4');
	
	pdf.fromHTML(downloadText, 15, 15, {
        'width': 500,
		'margin': 1,
		'pagesplit': true,
        'elementHandlers': specialElementHandlers
    });	
	pdf.save("CraftMapsItinerary.pdf");
}