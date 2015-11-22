var uuid;
var counter = 0;

var question = {
    init: function(details) {
        counter++;
        this.question = details[0];

        $('nav').prepend('<span>' + counter + '</span>');
        $('.question p').html(details[2]);
        $('.question img').attr('src', '/static/' + details[1][0]);
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
                uuid = data.uuid;
                question.init(data.question);
            });
        });
    } else {
        console.log('Geolocation has been blocked or is not supported on this device!');
    }
})();
