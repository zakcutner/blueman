import uuid
import requests

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask import Flask, render_template, jsonify, session, url_for, request, g
app = Flask(__name__)

from models import Question, Statement

pages = {
    'holder': Question(id='holder', image='badge.png', text='With a blue badge holder?',
                       result_yes='road', result_no='none'),
    'road': Question(id='road', image='road.png', text='On a road?',
                     result_yes='lines', result_no='carpark'),
    'lines': Question(id='lines', image='yellow_lines.png',
                      text='On <strong>single</strong> or <strong>double yellow lines</strong>?', result_yes='3hours',
                      result_no='meters/bays'),
    'meters/bays': Question(id='meters/bays', image='meters/bays.png',
                            text='At a parking meter or marked disabled bay?',
                            result_yes='unlimited', result_no='none'),

    'carpark': Statement(id='carpark', image='carpark.png',
                         text='Check local signage for more information!'),
    'unlimited': Statement(id='unlimited', image='',
                           text='You can park for free, with no time limit unless signposted.'),
    '3hours': Statement(id='3hours', image='',
                        text='You can park for up to 3 hours at a time, leaving 1 hour in between.'),
    'none': Statement(id='none', image='',
                      text='You cannot park in this area.'),
    'centrallondon': Statement(id='centrallondon', image='',
                               text='You are in central london.')
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

        print(r.json())

        district = r.json()['result'][0]['admin_district']

        print("Located in district: {0}".format(district))

        # Check for borough (City of London / Kensington and Chelsea / Westminster / Part of Camden)
        if district in ['Westminster', 'City of London', 'Kensington and Chelsea']:
            print("In central london: {0}".format(district))
            return jsonify(statement=pages['centrallondon'].to_json())
        elif district == 'Camden':
            # Check if south of Euston Road.
            print("In central london: {0}".format(district))
            return jsonify(statement=pages['centrallondon'].to_json())

        # Return starting question.
        return jsonify(question=pages['road'].to_json(),
                       uuid=user_id)
    else:
        user_id = uuid.UUID(request.form['uuid'])
        current_question = request.form['question_id']

        print(request.form['answer'])

        if request.form['answer']:
            new_question = pages[current_question].result_yes
        else:
            new_question = pages[current_question].result_no

        if type(pages[new_question]) == Statement:
            return jsonify(question=pages[new_question].to_json())
        else:
            return jsonify(statement=pages[new_question].to_json())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
