import csv
import uuid
import requests

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask import Flask, render_template, jsonify, session, url_for, request, g
app = Flask(__name__)

from models import Question, Statement

pages = {
    'holder': Question(id='holder', text='With a <strong>Blue Badge</strong> holder?',
                       result_yes='road', result_no='none', image='blue_badge.png'),

    'road': Question(id='road', text='On a <strong>road</strong>?',
                     result_yes='lines', result_no='carpark', image='road.png'),

    'lines': Question(id='lines', text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                      result_yes='3hours', result_no='bays', image='yellow_lines.png'),

    'cityoflondon': Question(id='cityoflondon', text='With a <strong>Blue Badge</strong> holder?',
                             result_yes='road_cityoflondon', result_no='none', image='blue_badge.png'),
    'road_cityoflondon': Question(id='road_cityoflondon', text='On a <strong>road</strong>?',
                                  result_yes='redbadge_cityoflondon', result_no='carpark', image='road.png'),
    'redbadge_cityoflondon': Question(id='redbadge_cityoflondon', text='With a disabled <strong>Red Badge</strong>?',
                                      result_yes='singleyellow_cityoflondon', result_no='disabledbay_cityoflondon'),
    'disabledbay_cityoflondon': Question(id='disabledbay_cityoflondon', text='In a <strong>disabled bay</strong>?', image='disabled_bay.png',
                                         result_yes='weekdaylimit', result_no='lines_cityoflondon'),
    'lines_cityoflondon': Question(id='lines_cityoflondon', text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                   image='yellow_lines.png',
                                   result_yes='none', result_no='payanddisplay_cityoflondon'),
    'singleyellow_cityoflondon': Question(id='singleyellow_cityoflondon', text='On a <strong>single yellow line</strong>?',
                                          image='single_yellow.png',
                                          result_yes='30minutes', result_no='payanddisplay_cityoflondon_redbadge'),
    'payanddisplay_cityoflondon_redbadge': Question(id='payanddisplay_cityoflondon_redbadge', text='In a <strong>pay and display bay</strong>?',
                                                    image='pay_and_display.png', result_yes='unlimited', result_no='none'),
    'payanddisplay_cityoflondon': Question(id='payanddisplay_cityoflondon', text='In a <strong>pay and display bay</strong>?',
                                           image='pay_and_display.png',
                                           result_yes='normalfeewithextension', result_no='none'),

    'kensington': Question(id='kensington', text='With a <strong>Blue Badge</strong> holder?',
                           result_yes='road_kensington', result_no='none', image='blue_badge.png'),
    'road_kensington': Question(id='road_kensington', text='On a <strong>road</strong>?',
                                result_yes='purplebadge_kensington', result_no='carpark', image='road.png'),
    'purplebadge_kensington': Question(id='purplebadge_kensington', text='With a disabled <strong>Purple Badge</strong>?',
                                       result_yes='lines_kensington', result_no='lines_cityoflondon'),
    'lines_kensington': Question(id='lines_kensington', text='On <strong>single</strong> or <strong>double yellow lines</strong>?',
                                 image='yellow_lines.png',
                                 result_yes='20minutes_dropoff', result_no='resident_payanddisplay_kensington'),
    'resident_payanddisplay_kensington': Question(id='resident_payanddisplay_kensington',
                                                  text='In a <strong>resident bay</strong> or <strong>pay and display bay</strong>?',
                                                  image='pay_and_display.png',
                                                  result_yes='unlimited', result_no='none'),

    'westminster': Question(id='westminster', text='With a <strong>Blue Badge</strong> holder?',
                            result_yes='westminster_road', result_no='none', image='blue_badge.png'),
    'westminster_road': Question(id='westminster_road', text='On a <strong>road</strong>?',
                                 result_yes='westminster_yellowline', result_no='carpark', image='road.png'),
    'westminster_yellowline': Question(id='westminster_yellowline', text='On a <strong>single yellow line</strong>?', image='single_yellow.png',
                                       result_yes='uncontrolledhours', result_no='westminster_doubleyellow'),
    'westminster_doubleyellow': Question(id='westminster_doubleyellow', text='On a <strong>double yellow line</strong>?', image='double_yellow.png',
                                         result_yes='none', result_no='westminster_disabledbay'),
    'westminster_disabledbay': Question(id='westminster_disabledbay', text='In a <strong>Blue Badge disabled bay</strong>?', image='disabled_bay.png',
                                        result_yes='4hours', result_no='westminster_whitebadge'),
    'westminster_whitebadge': Question(id='westminster_whitebadge', text='With a disabled <strong>White Badge</strong>?',
                                       result_yes='resident_payanddisplay_kensington', result_no='westminster_resident'),
    'westminster_resident': Question(id='westminster_resident', text='In a <strong>resident bay</strong>?',
                                     result_yes='uncontrolledhours', result_no='payanddisplay_cityoflondon'),

    'camden': Question(id='camden', text='With a <strong>Blue Badge</strong> holder?',
                       result_yes='camden_road', result_no='none', image='blue_badge.png'),
    'camden_road': Question(id='camden_road', text='On a <strong>road</strong>?',
                            result_yes='camden_disabledbay', result_no='carpark', image='road.png'),
    'camden_disabledbay': Question(id='camden_disabledbay', text='In a <strong>disabled bay</strong>?', image='disabled_bay.png',
                                   result_yes='unlimited', result_no='camden_greenbadge'),
    'camden_greenbadge': Question(id='camden_greenbadge', text='With a disabled <strong>Green Badge</strong>?',
                                  result_yes='resident_payanddisplay_kensington', result_no='none'),

    'bays': Question(id='bays', text='In a <strong>disabled bay</strong>?',
                     result_yes='unlimited', result_no='meters',
                     image='disabled_bay.png'),

    'meters': Question(id='meters',
                       text='At a <strong>parking meter</strong>?',
                       result_yes='unlimited', result_no='none',
                       image='meters.png'),

    'carpark': Statement(id='carpark',
                         text='Check <strong>local signage</strong> for more information!'),
    'unlimited': Statement(id='unlimited', text='For <strong>free</strong>, with <stnog>no time limit</strong> unless signposted.'),
    '20minutes_dropoff': Statement(id='20minutes_dropoff', text='For <strong>20 minutes</strong>, to <strong>pick up or drop off</strong> a <strong>disabled person</strong>.'),
    '30minutes': Statement(id='30minutes', text='For up to <strong>30 minutes</strong>.'),
    '4hours': Statement(id='4hours', text='For up to <strong>4 hours</strong> in <strong>controlled time</strong>, otherwise <strong>unlimited</strong>.'),
    '3hours': Statement(id='3hours', text='For up to <strong>3 hours</strong> at a time, leaving <strong>1 hour in between</strong>.'),
    'weekdaylimit': Statement(id='weekdaylimit', text='For <strong>free</strong>, but only for <strong>four hours on weekdays</strong>.'),
    'none': Statement(id='none', text='Only if <strong>normal restrictions</strong> allow you to.'),
    'normalfeewithextension': Statement(id='payanddisplay', text='If you pay the <strong>normal fee</strong>, but you can stay for an <strong>extra hour</strong>.'),
    'uncontrolledhours': Statement(id='uncontrolledhours', text='For <strong>free</strong> in <strong>uncontrolled hours</strong>.')
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['POST'])
def start():
    if 'uuid' in request.form:
        print(uuid.UUID(request.form['uuid']))

    print(request.form)

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
            return jsonify(question=pages['cityoflondon'].to_json(), uuid=user_id)
        elif district == 'Kensington and Chelsea':
            return jsonify(question=pages['kensington'].to_json(), uuid=user_id)
        elif district == 'Westminster':
            return jsonify(question=pages['westminster'].to_json(), uuid=user_id)
        elif district == 'Camden':
            return jsonify(question=pages['camden'].to_json(), uuid=user_id)

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
