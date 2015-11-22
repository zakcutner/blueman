var uuid;
var counter = 0;

var question = {
    init: function(details) {
        counter++;
        this.question = details.id;

        $('nav').prepend('<span>' + counter + '</span>');
        $('.question p').html(details.text);
        $('.question img').attr('src', details.image);
    },

    submit: function(answer) {
        $.post('/api/', {uuid: uuid, question_id: this.question, answer: answer}, function(data) {
            if(data.question) question.init(data.question);
            else if(data.statement) statement.init(data.statement);
        });
    }
};

var statement = {
    init: function(details) {
        counter++;

        $('nav').prepend('<span>' + counter + '</span>');
        $('.question p').html(details.text);

        if(details.image) $('.question img').attr('src', details.image);
        else $('.question img').hide();

        $('#yes, #no').hide();
        $('#restart').show();
    },

    submit: function() {
        $('.question.img').removeAttr('src').show();
        $('#yes, #no').show();
        $('#restart').hide();
        $('nav').empty();
        counter = 0;
        init();
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

$('#restart').click(function(e) {
    e.preventDefault();
    statement.submit();
});

function init() {
    if('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            $.post('/api/', {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            }, function(data) {
                uuid = data.uuid;
                if(data.question) question.init(data.question);
                else if(data.statement) statement.init(data.statement);
            });
        });
    } else {
        console.log('Geolocation has been blocked or is not supported on this device!');
    }
}

init();
