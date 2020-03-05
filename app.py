import pandas as pd
from pandas.io.json import json_normalize
from flask import Flask, jsonify, request, render_template
import joblib                               ## TO unpack
import pickle                             ## To use .pkl model
import json                               ## To load in 'features.json'
# from flask_sqlalchemy import SQLAlchemy ## Use with db
# from flask_migrate import Migrate       ## Use with db
# import psycopg2                         ## To connect to PostgreSQL Database
# from dotenv import load_dotenv          ## To get .env
# import os                               ## To get .env

# load_dotenv()

# db = SQLAlchemy()

# migrate = Migrate()

# DB_NAME=os.getenv('DB_NAME', default='OOPS')
# DB_USER=os.getenv('DB_USER', default='OOPS')
# DB_PASS=os.getenv('DB_PASS', default='OOPS')
# DB_HOST=os.getenv('DB_HOST', default='OOPS')

# conn = psycopg2.connect(dbname='DB_NAME', user='DB_USER',
#                         password='DB_PASS', host='DB_HOST')
# cur = conn.cursor()

# Load the model from 'berlin_model.pkl' file or 'berlin_model.gz'
# model = pickle.load(open('berlin_model.pkl', 'rb'))
model = joblib.load(open('berlin_model.gz', 'rb'))

# App
app = Flask(__name__)

# Could Remove: vvvv
# Setting this to True makes the returned JSON look not-so-jumbled
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

### FOR DATABASE ###
# class AirBnB_features(db.Model):
#     id = db.Column(db.BigInteger, primary_key=True)
#     accommodates = db.Column(db.Integer)
#     bedrooms = db.Column(db.Integer)
#     cleaning_fee = db.Column(db.Integer)
#     extra_people = db.Column(db.Integer)
#     guests_included = db.Column(db.Integer)
#     minimum_nights = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Mitte = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Pankow = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Tempelhof-Schoneberg = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Friedrichshain-Kreuzberg = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Neukolln = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Charlottenburg-Wilm. = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Treptow_Kopenick = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Steglitz-Zehlendorf = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Reinickendorf = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Lichtenberg = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Marzahn-Hellersdorf = db.Column(db.Integer)
#     neighbourhood_group_cleansed_Spandau = db.Column(db.Integer) 
#     property_type_Guesthouse = db.Column(db.Integer)
#     property_type_Apartment = db.Column(db.Integer)
#     property_type_Condominium = db.Column(db.Integer)
#     property_type_Loft = db.Column(db.Integer)
#     property_type_House = db.Column(db.Integer)
#     property_type_Serviced_apartment = db.Column(db.Integer)
#     property_type_Townhouse = db.Column(db.Integer)
#     property_type_Other = db.Column(db.Integer)
#     property_type_Bed_and_breakfast = db.Column(db.Integer)
#     property_type_Guest_suite = db.Column(db.Integer)
#     property_type_Hostel = db.Column(db.Integer)
#     room_type_Entire_home/apt = db.Column(db.Integer)
#     room_type_Private_room = db.Column(db.Integer)
#     room_type_Shared_room = db.Column(db.Integer)
#     bed_type_Real_Bed = db.Column(db.Integer)
#     bed_type_Sofa_Other = db.Column(db.Integer)
#     instant_bookable_f = db.Column(db.Integer)
#     instant_bookable_t = db.Column(db.Integer)
#     cancellation_policy_strict = db.Column(db.Integer)
#     cancellation_policy_flexible = db.Column(db.Integer)
#     cancellation_policy_moderate = db.Column(db.Integer)
#     feat_id = relationship('AirBnB_prices', uselist=False, back_populates='price_id')

# class AirBnB_prices(db.Model):
#     id = db.Column(db.BigInteger, primary_key=True)
#     price = db.Column(db.Integer)
#     price_id = relationship('AirBnB_features', uselist=False, back_populates='feat_id')

# Routes
@app.route('/')
def index():
    return render_template('feature_input.html')

@app.route('/price', methods=['POST'])
def predict_price():

    # Takes data entered at index route via the 'feature_input.html' template
    data = dict(request.form)
    
    # Parse the file 'features.json' containing a skeleton JSON of feature variables with
    # default values set to '0'.  This block of code compares the data from the request form
    # to the default values from the JSON file and makes changes depending on what the input
    # was.  For features that have multiple permutations (neighbourhood_group_cleansed, etc),
    # whichever was chosen in the drop-down list will be reassigned as an integer(1) while
    # the others remain an integer(0) which denotes that the listing is not a particular
    # feature permutation and thus, can be ran through the model.
    with open('features.json', 'r') as f:
        features_dict = json.load(f)
        for key, value in data.items():
            if key in features_dict:
                try:
                    features_dict[key] = float(value)
                except:
                    features_dict[key] = 0
            elif value in features_dict:
                features_dict[value] = 1
        # print(features_dict)
        data = features_dict

    # This code will take the variable 'data' and convert it from JSON into a Pandas
    # Dataframe which can be used with the next line of code
    df = pd.json_normalize(data)

    # Prediction based on the Dataframe containing feature values.
    # model.predict(df) returns the prediction as an n-dimensional array which is not able
    # to be 'jsonified' so you must grab the index at [0] to take it out of the array and
    # convert to JSON.  The prediction is rounded to the nearest integer.
    results = int(model.predict(df)[0])

    # Return the features and predicted price as JSON
    # return jsonify(features=data, price=results)
    return jsonify(price=results)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
