var uuid;

var position = {
    locate: function() {
        if('geolocation' in navigator) {
            navigation.geolocation.getCurrentPosition(function(position) {
                this.latitude = position.coords.latitude;
                this.longitude = position.coords.longitude;
            });
        } else {
            console.log('Geolocation has been blocked or is not supported on this device!');
        }
    },

    retrieve: function() {
        if('latitude' in this && 'longitude' in this) {
            return [this.latitude, this.longitude]
        } else {
            locate();
            retrieve();
        }
    }
};

var question = {
    init: function(details) {
        this.text = details.text;
        this.images = details.images;
    },

    submit: function(answer) {
        $.post('/api/', {uuid: uuid, answer: answer}, function(data) {
            question.init(data.question);
        });
    }
};

(function() {
    $.post('/api/', {position: position.retrieve()}, function(data) {
        uuid = data.uuid;
        question.init(data.question);
    });
});
