var uuid;

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

$(document).ready(function() {
    if('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            $.post('/api/', {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            }, function(data) {
                uuid = data.uuid;
                question.init(data.question);
                console.log(uuid);
            });
        });
    } else {
        console.log('Geolocation has been blocked or is not supported on this device!');
    }
});
