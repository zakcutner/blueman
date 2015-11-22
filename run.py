import csv
import uuid
import requests
from geopy.distance import vincenty

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
                      result_no='meters', image='yellow_lines.png'),
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
    '3hours': Statement(id='3hours', text='You can park for up to 3 hours at a time, leaving 1 hour in between.'),
    'none': Statement(id='none', text='You cannot park in this area.'),
    'centrallondon': Statement(id='centrallondon', text='You are in central london.')
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

        if r.json()['result']:
            district = r.json()['result'][0]['admin_district']
        else:
            district = ''
        district = 'Barnet'

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

        if new_question == 'meters':
            with open('parking.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in reader:
                    latitude, longitude = row
                    distance = vincenty((latitude, longitude),
                                        (request.form['latitude'],
                                         request.form['longitude'])).miles

                    # If there's a parking bay within 50 meters, do not skip this question.
                    if distance.miles < 0.03:
                        new_question = 'bays'
                        break

        if type(pages[new_question]) == Statement:
            return jsonify(statement=pages[new_question].to_json())
        else:
            return jsonify(question=pages[new_question].to_json())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
