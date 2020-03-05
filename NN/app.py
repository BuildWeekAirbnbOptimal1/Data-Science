"""
    __author__ = Beth
    __credits__ = Beth
    __license__ = MIT License
    __version__ = 1
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

"""create and configures an instance of a flask app"""
app = Flask(__name__)

encoder = pickle.load(open('encoder.pkl', 'rb'))

model = pickle.load(open('model.pkl', 'rb'))


@app.route('/', methods=['GET', 'POST'])
def root():
    """Root site directory for the app.Renders only the base.html template.
       :return: render_template
    """
    message = 'Hello'
    return render_template('base.html', message=message)


@app.route('/request', methods=['GET', 'POST'])
def request_data():
    """Gets data in JSON format and runs it through the model.
       :return: JSON file.
    """
    data = request.get_json()

    # Non-default values. Needs to have user input or breaks the app.
    # TODO Accomodate has a spelling error. Needs to be changed to "accommodate".
    accomodates = data['accomodates']
    bathrooms = data['bathrooms']
    bedrooms = data['bedrooms']
    beds = data['beds']
    bed_type = data['bed_type']
    instant_bookable = data['instant_bookable']
    minimum_nights = data['minimum_nights']
    neighborhood = data['neighborhood']
    room_type = data['room_type']
    wifi = data['wifi']

    # Defaulted values
    security_deposit = 0
    cleaning_fee = 10

    features = {'accomodates': accomodates, 'bathrooms': bathrooms, 'bedrooms': bedrooms,
                'beds': beds, 'bed_type': bed_type, 'instant_bookable': instant_bookable,
                'minimum_nights': minimum_nights, 'neighborhood': neighborhood,
                'room_type': room_type, 'wifi': wifi, 'security_deposit': security_deposit,
                'cleaning_fee': cleaning_fee}

    # Converts the data into a DataFrame object.
    predict_data = pd.DataFrame(features, index=[1])
    features_encoder = encoder.transform(predict_data)

    # Feeds the data into the model.
    prediction = model.predict(features_encoder)

    # Returns prediction in a JSON format and within, a float.
    return jsonify({'prediction': prediction[0]})


if __name__ == '__main__':
    app.run(debug=True)
