import csv
import uuid
import requests

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask import Flask, render_template, jsonify, session, url_for, request, g
app = Flask(__name__)

from models import Question, Statement

pages = {
    'holder': Question(id='holder', text='With a blue badge holder?',
                       result_yes='road', result_no='none', image='badge.png'),

    'road': Question(id='road', text='On a road?',
                     result_yes='lines', result_no='carpark', image='road.png'),

    'lines': Question(id='lines',
                      text='On <strong>single</strong> or <strong>double yellow lines</strong>?', result_yes='3hours',
                      result_no='bays', image='yellow_lines.png'),

    'cityoflondon': Question(id='cityoflondon_redbadge', text='With a disabled Red Badge?', image='red_badge.png',
                             result_yes='singleyellow_cityoflondon', result_no='disabledbay_cityoflondon'),
    'disabledbay_cityoflondon': Question(id='disabledbay_cityoflondon', text='In a disabled bay?',
                                         result_yes='weekdaylimit', result_no='lines_cityoflondon'),
    'lines_cityoflondon': Question(id='lines_cityoflondon', text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                   result_yes='none', result_no='payanddisplay_cityoflondon'),
    'singleyellow_cityoflondon': Question(id='singleyellow_cityoflondon', text='On a <strong>single yellow line</strong>?',
                                          result_yes='30minutes', result_no='payanddisplay_cityoflondon_redbadge'),
    'payanddisplay_cityoflondon_redbadge': Question(id='payanddisplay_cityoflondon_redbadge', text='In a pay and display bay?',
                                           result_yes='unlimited', result_no='none'),
    'payanddisplay_cityoflondon': Question(id='payanddisplay_cityoflondon', text='In a pay and display bay?',
                                           result_yes='normalfeewithextension', result_no='none'),

    'kensington': Question(id='kensington', text='With a disabled Purple Badge?', image='purple_badge.png',
                           result_yes='yellow_cityoflondon', result_no='lines_cityoflondon'),
    'lines_kensington': Question(id='yellow_cityoflondon', text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                 result_yes='20minutes_dropoff', result_no='resident_payanddisplay_kensington'),
    'resident_payanddisplay_kensington': Question(id='resident_payanddisplay_kensington', text='In a resident bay or pay and display bay?',
                                                  result_yes='unlimited', result_no='none'),

    'westminster': Question(id='westminster', text='On a single yellow line?', image='single_yellow.png',
                            result_yes='uncontrolledhours', result_no='westminster_doubleyellow'),
    'westminster_doubleyellow': Question(id='westminster_doubleyellow', text='On a double yellow line?', image='double_yellow.png',
                                         result_yes='none', result_no='resident_payanddisplay_kensington'),
    'westminster_whitebadge': Question(id='westminster', text='With a disabled White Badge?', image='white_badge.png',
                                       result_yes='westminster_disabledbay', result_no='lines_cityoflondon'),
    'westminster_disabledbay': Question(id='westminster_disabledbay', text='In a Blue Badge disabled bay?', image='disabled_bay.png',
                                        result_yes='4hours', result_no='resident_payanddisplay_kensington'),

    'camden': Question(id='camden', text='In a disabled bay?',
                                   result_yes='unlimited', result_no='camden_greenbadge'),
    'camden_greenbadge': Question(id='camden_greenbadge', text='With a disabled Green Badge?', image='green_badge.png',
                                  result_yes='resident_payanddisplay_kensington', result_no='none'),

    'bays': Question(id='bays', text='At a marked disabled bay?',
                     result_yes='unlimited', result_no='meters',
                     image='bays.png'),

    'meters': Question(id='meters',
                       text='At a parking meter?',
                       result_yes='unlimited', result_no='none',
                       image='meters.png'),

    'carpark': Statement(id='carpark',
                         text='Check local signage for more information!',
                         image='carpark.png'),
    'unlimited': Statement(id='unlimited', text='You can park for free, with no time limit unless signposted.'),
    '20minutes_dropoff': Statement(id='20minutes_dropoff', text='You can park here for 20 minutes, to pick up or drop off a disabled person.'),
    '30minutes': Statement(id='30minutes', text='You can park here for up to 30 minutes.'),
    '4hours': Statement(id='4hours', text='You can park here for up to 4 hours.'),
    '3hours': Statement(id='3hours', text='You can park for up to 3 hours at a time, leaving 1 hour in between.'),
    'weekdaylimit': Statement(id='weekdaylimit', text='You can park here for free, but only for four hours on weekdays.'),
    'none': Statement(id='none', text='You must follow normal restrictions.'),
    'normalfeewithextension': Statement(id='payanddisplay', text='You must pay the normal fee, but you can stay for an extra hour.'),
    'uncontrolledhours': Statement(id='uncontrolledhours', text='You can park for free in uncontrolled hours.')
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['POST'])
def start():
    if 'uuid' in request.form:
        print(uuid.UUID(request.form['uuid']))

    if ('uuid' not in request.form):
        # Store unique user ID.
        user_id = uuid.uuid4()

        # Query geolocation.
        r = requests.get('http://api.postcodes.io/postcodes',
                         params={'longitude': request.form['longitude'],
                                 'latitude': request.form['latitude']})

        if r.json()['result']:
            district = r.json()['result'][0]['admin_district']
        else:
            district = ''

        print("Located in district: {0}".format(district))

        # Check for borough (City of London / Kensington and Chelsea / Westminster / Part of Camden)
        if district == 'City of London':
            return jsonify(question=pages['cityoflondon'].to_json())
        elif district == 'Kensington and Chelsea':
            return jsonify(question=pages['kensington'].to_json())
        elif district == 'Westminster':
            return jsonify(question=pages['westminster'].to_json())
        elif district == 'Camden':
            return jsonify(question=pages['camden'].to_json())

        # Return starting question.
        return jsonify(question=pages['holder'].to_json(),
                       uuid=user_id)
    else:
        user_id = uuid.UUID(request.form['uuid'])
        current_question = request.form['id']

        print(request.form['answer'])

        if request.form['answer'] == 'true':
            new_question = pages[current_question].result_yes
        else:
            new_question = pages[current_question].result_no

        print(new_question)
        print(type(pages[new_question]))

        if type(pages[new_question]) == Statement:
            return jsonify(statement=pages[new_question].to_json())
        else:
            return jsonify(question=pages[new_question].to_json())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
