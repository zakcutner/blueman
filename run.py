import uuid

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask import Flask, render_template, jsonify, session, url_for, request, g
app = Flask(__name__)

questions = {
    'road': (['road.png'], 'On a road?', 'lines', 'carpark'),
    'lines': (['single_yellow.png', 'double_yellow.png'], 'On single or double yellow lines?', '3hours', 'meters/bays'),
    'meters/bays': (['meters.png', 'bays.png'], 'At a parking meter or marked disabled bay?', 'unlimited', 'none'),

    'carpark': (['carpark.png'], 'Check local signage for more information!', '', ''),
    'unlimited': ([], 'You can park for free, with no time limit unless signposted.', '', ''),
    '3hours': ([], 'You can park for up to 3 hours at a time, leaving 1 hour in between.', '', ''),
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
        # request.form['geolocation']

        # Check for borough (City of London / Kensington and Chelsea / Westminster / Part of Camden)

        # Return starting question.
        return jsonify(question=('road', questions['road'][0], questions['road'][1]),
                       uuid=user_id)
    else:
        user_id = uuid.UUID(request.form['uuid'])
        current_question = request.form['question_id']

        print(request.form['answer'])

        if request.form['answer']:
            new_question = questions[current_question][2]
        else:
            new_question = questions[current_question][3]

        print(questions[current_question] + questions[new_question])

        if questions[new_question][2]:
            return jsonify(question=(new_question, questions[new_question][0], questions[new_question][1]))
        else:
            return jsonify(statement=(new_question, questions[new_question][0], questions[new_question][1]))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
