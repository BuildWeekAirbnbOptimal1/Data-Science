# Data-Science

For this project, our goal is to accurately predict the price of a potential listing for AirBnB in the city of Berlin, Germany.

## Notebook

The notebook for this repo 'airbnb_notebook.ipynb' is used to take 'Berlin.csv' which
is taken and cleaned up from the original at https://www.kaggle.com/brittabettendorf/berlin-airbnb-data and turn that into a predictive model for prices of airbnb listings in the Berlin area. This model is persisted to `berlin_model.gz` as a compressed joblib dump (instead of pickle). Next `app.py` reads this model and uses it to make predictions in the web interface, for now arranged as html under `templates/`. `features.json`contains a skeleton JSON of feature variables with default values set to '0', and is used to transform html form input into a format used to do the model prediction. `requirements.txt`, `runtime.txt`, and `Procfile` are all necessary to run on Heroku.