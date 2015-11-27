import csv
import uuid
import requests

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask import Flask, render_template, jsonify, session, url_for, request, g
app = Flask(__name__)

from data import questions, statements, steps


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/', methods=['POST'])
def start():
    print(request.form)

    # If a district has not yet been assigned to this session:
    if ('district' not in request.form):
        # Get the current district using the lat/long and postcodes.io API.
        r = requests.get('http://api.postcodes.io/postcodes',
                         params={'longitude': request.form['longitude'],
                                 'latitude': request.form['latitude']})

        if r.json()['result']:
            district = r.json()['result'][0]['admin_district']
        else:
            district = '*'

        print("Found user in district: {0}".format(district))

        # Ignore any districts other than 'Camden', 'Westminster',
        # 'City of London' and 'Kensington and Chelsea'.
        if district not in steps:
            district = '*'

        # Return starting question.
        return jsonify(question=questions['blue_badge'].to_json(),
                       district=district)
    else:
        current_question = request.form['id']
        district = request.form['district']

        print("Received an answer of {0} for question {1} for district {2}"
              .format(request.form['answer'], current_question, district))

        if request.form['answer'] == 'true':
            new_question = steps[district][current_question][0]
        else:
            new_question = steps[district][current_question][1]

        print("Moving to question/statement {0}".format(new_question))

        if new_question in statements:
            return jsonify(statement=statements[new_question].to_json())
        elif new_question in questions:
            return jsonify(question=questions[new_question].to_json())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
