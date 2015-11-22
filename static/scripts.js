var uuid;
var counter = 0;

var question = {
    init: function(details) {
        counter++;
        this.question = details.id;

        $('nav').prepend('<span>' + counter + '</span>');
        $('.question p').html(details.text);
        $('.question img').attr('src', '/static/' + details.image);
    },

    submit: function(answer) {
        $.post('/api/', {uuid: uuid, question_id: this.question, answer: answer}, function(data) {
            question.init(data.question);
        });
    }
};

$('#yes').click(function(e) {
    e.preventDefault();
    question.submit(true);
});

$('#no').click(function(e) {
    e.preventDefault();
    question.submit(false);
});

(function() {
    if('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            $.post('/api/', {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            }, function(data) {
                console.log(data);
                uuid = data.uuid;
                question.init(data.question);
            });
        });
    } else {
        console.log('Geolocation has been blocked or is not supported on this device!');
    }
})();
