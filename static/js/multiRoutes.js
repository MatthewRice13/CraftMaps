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
var currentlatitude = latstart;
var currentlongitude = lngstart;
var downloadText = '';
var tripCounter = 1;

var startPoint = new google.maps.LatLng(startlatitude, startlongitude);
//document ready function
$(document).ready(function(){
	
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
	$('#downloadFile').on('click', function(){
		downloadPDF();
	});
	//flags for brewery numbers
	for(b=1;b<=breweriesJson.length;b++)
	{
		var str = "flag"+b+"=false";
		eval(str);
	}
	//modal function calling
	/*$("headerLabel").on('click', function(e){
		var urllink= e.target.id;
		console.log(urllink);
		//var ret = window.showModalDialog("http://woodkeybrewing.ie/", "", "dialogWidth:80%;dialogHeight:80%");
	});*/
});//ready end

function populateBreweriesList(){
    var listBrew = '';
	var buttonListBrew = '';
	var startPointButton = "<button class='btn btn-outline auto-btn' type='button' onClick='showDirections("+startlatitude+","+startlongitude+")'>Start Point</button><br><br>";
	$("#listOfBreweries").append(startPointButton);
	for(i=0; i < breweriesJson.length; i++){
		//listBrew = "<li><input type='checkbox' name="+breweriesJson[i].coords.lng+" class='checkboxList' value="+ breweriesJson[i].coords.lat+">"+ breweriesJson[i].name + "</li>";
		var number = i+1;
		buttonListBrew = "<button class='btn btn-outline auto-btn' type='button' onClick='checkForItenary("+breweriesJson[i].coords.lat+","+breweriesJson[i].coords.lng+","+number+")'>"+number+": "+breweriesJson[i].name+"</button><br>";
		//$("#listOfBreweries").append(listBrew);
		$("#listOfBreweries").append(buttonListBrew);
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



function showModal(e){
	var urllink = e.target.id;//console.log(urllink);
	var ret = window.showModalDialog(urllink, "", "dialogWidth:80%;dialogHeight:80%");
}
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
	directionsService.route(request, function(result, status) {//console.log(result);
		if (status == google.maps.DirectionsStatus.OK) {
			directionsDisplay.setDirections(result);
			directionRoute = result.routes["0"].legs["0"].steps;
			for(i=0;i<directionRoute.length;i++){
				//console.log(directionRoute[i].instructions);  //correct
				directionText = directionText + directionRoute[i].instructions+"\n";
				for(var x in directionRoute[i]){
					if(x=="steps"){
						for(j=0;j<directionRoute[i].steps.length;j++){
							//console.log(directionRoute[i].steps[j].instructions);  //correct
							directionText = directionText + directionRoute[i].steps[j].instructions+"\n";
						}
					}
				}
			}
			//var finalDirection = $('<p>'+directionText+'</p>').text();
			prepareText(directionText);                      //finalDirection);     // directionText);
			$("#directionsPanel").empty();
			$("#directionsPanel").css("background-color", "white");
			currentlatitude = lati;
			currentlongitude = longi;
		}
		else if (status == google.maps.DirectionsStatus.ZERO_RESULTS){
			alert('Public Transport route does not exist, Driving route will be shown');
			if(mode == "TRANSIT"){
			alert('Public Transport route does not exist, Driving route will be shown');
			getDirectionsDrive(lati,longi);
			}
			if(mode == "DRIVING"){
				alert("Sorry, No routes available");
				location.href = currentURL;
			}
		}
	});
}

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

function prepareText(directions){
	var directionDetails = "<b>TRIP "+tripCounter+":</b>"+"<div>";
	directionDetails = directionDetails + directions+"</div>"
	tripCounter = tripCounter+1;
	downloadText = downloadText + directionDetails;
	//console.log(downloadText);
}
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
	pdf.save("CraftMapsItenary.pdf");
}