var location = {
    locate: function() {
        if('geolocation' in navigator) navigation.geolocation.getCurrentPosition(function(position) {
            self.latitude = position.coords.latitude;
            self.longitude = position.coords.longitude;
        });
    },

    retrieve: function() {
        if('latitude' in self && 'longitude' in self) {
            return(self.latitude, self.longitude);
        } else {
            locate();
            retrieve();
        }
    }
}
