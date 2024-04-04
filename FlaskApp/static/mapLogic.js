let zoomHome = 17;
let marker;

function updateStatusMsg(inputNumber){

    if (inputNumber == 0) {
        document.getElementById("griffStatus").innerText = "off";
        document.getElementById("griffStatus2").innerText = ".";

    } else {
        document.getElementById("griffStatus").innerText = "on";
        document.getElementById("griffStatus2").innerText = "!";
    }

}

function initMap(mapToInit) {
    $.get('/map_data', function(data) {
        mapToInit.setMaxBounds([[data.lat_a, data.long_a], [data.lat_b, data.long_b]]);
        mapToInit.setView([(data.latitude + data.markerlat) / 2, (data.longitude + data.markerlong) / 2], zoomHome);
        mapToInit.options.minZoom = zoomHome;
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        marker = L.marker([data.markerlat, data.markerlong]).addTo(mapToInit);
        updateStatusMsg(data.markerlat);
        marker.bindTooltip("Griff is here!");
        console.log("Map created with latitude:", data.markerlat, "longitude:", data.markerlong);
    }).fail(function() {
        console.log("Failed to init map data.");
    });
}

// Init map
var map = L.map('map');
initMap(map) 

function updateMap() {
    $.get('/map_data', function(data) {
        // Update map with new data
        map.setView([(data.latitude + data.markerlat) / 2, (data.longitude + data.markerlong) / 2]);

        marker.setLatLng([data.markerlat, data.markerlong]);
        updateStatusMsg(data.markerlat);
        console.log("Marker updated with latitude:", data.markerlat, "longitude:", data.markerlong);
    }).fail(function() {
        console.log("Failed to fetch marker data.");
    });
}

function updateCountdown(seconds) {
    document.getElementById('countdown').innerText = seconds;
}

// Update the map every 60 seconds
setInterval(function() {
    updateMap();
    updateCountdown(60);
}, 60000);

// Update the countdown every second
setInterval(function() {
    var countdownElement = document.getElementById('countdown');
    var seconds = parseInt(countdownElement.innerText);
    if (seconds > 0) {
        updateCountdown(seconds - 1);
    }
}, 1000);