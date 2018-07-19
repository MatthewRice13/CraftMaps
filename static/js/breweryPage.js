var breweryJson = Brewery_JSON;
var startLat = breweryJson[0].coords.lat;
var startLng = breweryJson[0].coords.lng;

//document ready function
$(document).ready(function(){
	//getLocation(); // will give the current position
	initMap();
	addTwitterFeed();
	addProfilePic();
});

function initMap(){
	// Map options
	var options = {
		zoom:11,
		//center: new google.maps.LatLng(currentLat, currentLng)
		//setting center as the spire tower
		center: new google.maps.LatLng(startLat, startLng)
	}
	// New map
	map = new google.maps.Map(document.getElementById('map'), options);
	addMarker(breweryJson);
	populateBreweriesList();
}

// Add Marker Function
function addMarker(props){
	var marker = new google.maps.Marker({
		position: props[0].coords,
		title: props[0].name,
		map: map,
	});
	// Check content
	if(props[0].Content){
		marker.addListener('click', function(){
			if(typeof infoWindow != 'undefined'){
				infoWindow.close();
			}
			infoWindow = new google.maps.InfoWindow({
				content: props[0].Content
			});
			infoWindow.open(map, marker);
		});
	}
}

function populateBreweriesList(){
    var listBrew = '';
    listBrew = "<h2>"+ breweryJson[0].name + "</h2>"
	+ "<br><h3>" + breweryJson[0].address + "<h3></h3>";
    $("#listOfBreweries").append(listBrew);
}

function addTwitterFeed() {
    var twitter = breweryJson[0].twitter;
    var link = "https://www." + twitter + "?ref_src=twsrc%5Etfw";
    document.getElementById("twitter").setAttribute("href", link);
    $("#twitter").append(breweryJson[0].name);
}


function addProfilePic(){
	var pic = breweryJson[0].pic;
	document.getElementById("profile-pic").setAttribute("src", pic);
}/**/
