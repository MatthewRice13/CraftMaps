//brewery and beer data
var breweryJson = Brewery_JSON;
var beerJson = Beer_JSON;
var startLat = breweryJson[0].coords.lat;
var startLng = breweryJson[0].coords.lng;

//document ready function
$(document).ready(function(){
	initMap();
	addProfilePic();
	populateBreweryInformation();
	populateTable();
});//ready ends

function initMap(){
	// Map options
	var options = {
		zoom:14,
		center: new google.maps.LatLng(startLat, startLng)
	}
	// New map
	map = new google.maps.Map(document.getElementById('brewery-map'), options);
	addMarker(breweryJson);
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
 // profile picture for the brewery
function addProfilePic(){
	var pic = breweryJson[0].pic;
	document.getElementById("profile-pic").setAttribute("src", pic);
}

//beers table for the brewery
function populateTable(){
	var len=beerJson.length;
	var rowTable='';
	for(i=0;i<len;i++){
		rowTable='<tr class="rowHead"><td class="tabName">'+beerJson[i].name+'</td><td class="tabType">'+beerJson[i].type+'</td><td class="tabPercent">'+beerJson[i].percent+'</td><td class="tabRating">'+beerJson[i].rating+'</td></tr>'
		$("#tabBody").append(rowTable);
	}
}
// brewery information
function populateBreweryInformation(){
	var name = breweryJson[0].address.name;
	var type = breweryJson[0].brewery_type;
	var rating = breweryJson[0].rating+'/5';
	var address = breweryJson[0].address.region+',&nbsp;Ireland';
	var url = breweryJson[0].social.website;
	var twitter = breweryJson[0].social.twitter
	var facebook = breweryJson[0].social.facebook;
	$("#name").append(name);
	$("#brName").append('&nbsp;'+name);
	$("#type").append(type);
	$("#rateNumber").append(rating);
	$("#address").append(address);
	//show social links only when available
	if(url != "www.google.com"){
		var temphref= 'https://www.'+url;
		var tempurl = '<a class="aLink" href="'+temphref+'" target="_blank">'+url+'</a>';
		$("#url").append(tempurl);
	}
	if(twitter != "irecraftbeer"){
		var temphref= 'https://www.twitter.com/'+twitter;
		var temptwitter = '<a class="aLink" href="'+temphref+'" target="_blank">twitter.com/'+twitter+'</a>';
		$("#twitter").append(temptwitter);
	}
	if(facebook != "www.facebook.com"){
		var temphref= 'https://www.'+facebook;
		var tempfb = '<a class="aLink" href="'+temphref+'" target="_blank">'+facebook+'</a>';
		$("#facebook").append(tempfb);
	}
}