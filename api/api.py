from flask import Flask
from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import joblib
import numpy as np
from diamond_util import label_cat_encode
import pandas as pd
# https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166

# Model
model_filename = '../models/model_Gradient_boosted_regression.pkl'
model = joblib.load(open(model_filename, 'rb'))

app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = request.get_json(force=True)

    # convert data into dataframe
    data.update((x, [y]) for x, y in data.items())
    x = pd.DataFrame.from_dict(data)

    # predictions
    cat_columns=['cut', 'color', 'clarity']
    for cat in cat_columns:
        x=label_cat_encode(x, cat).copy()
        x[cat] = x[cat].astype(int)
   
    y_true = x['price'].values
    y_pred = np.round(model.predict(x.drop('price', axis=1).values), 2)
    output= {'Price predicted': str(y_pred[0]), 'Price true value': str(y_true[0])}

    return jsonify(output)

    


if __name__ == '__main__':
    app.run(debug=True, port=5000)