from flask import Flask
from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
import pickle
import joblib
import numpy as np
from diamond_util import label_cat_encode
import pandas as pd
# https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166

app = Flask(__name__)
api = Api(app)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictDiamondPrice(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']
        
        # TODO: Complete the external parameters part
        x0 = {
            'carat': [0.23],\
            'cut': ['Ideal'],\
            'color': ['E'],\
            'clarity': ['SI2'],\
            'depth': [61.5],\
            'table': [55.0],\
            'price': [326],\
            'x': [3.95],\
            'y': [3.98],\
            'z': [2.43]
        }
        
        x = pd.DataFrame.from_dict(x0)

        # Preprocessing
        cat_columns=['cut', 'color', 'clarity']
        for cat in cat_columns:
            x=label_cat_encode(x, cat).copy()
            x[cat] = x[cat].astype(int)

        # Model
        model_filename = '../models/model_Gradient_boosted_regression.pkl'
        model = joblib.load(open(model_filename, 'rb'))

        y_true = x['price'].values
        y_pred = np.round(model.predict(x.drop('price', axis=1).values), 2)
        output= {'Price predicted': str(y_pred[0]), 'Price true value': str(y_true[0])}

        #prediction = mdl.predict(user_query)
        #prediction_proba = mdl.predict_proba(user_query)

        # create JSON object
        #output = {'prediction': prediction, 'confidence': confidence}
        
        return jsonify(output)
        

api.add_resource(PredictDiamondPrice, '/')

if __name__ == '__main__':
    app.run(debug=True)