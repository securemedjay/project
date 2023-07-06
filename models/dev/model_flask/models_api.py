#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# swagger to generate UI
import pickle
from flask import Flask, request
from flasgger import Swagger
import numpy as np
import pandas as pd

# it is good practice to use relative file path instead of absolute so that if the file is 
# copied to another system the code will not break
with open('./rfc.pkl', 'rb') as rfc_model:
    rfc = pickle.load(rfc_model)

with open('./deep_learn.pkl', 'rb') as dl_model:
    dl = pickle.load(dl_model)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return 'Hello there'

# # Swagger requires that a docstring be provided using the specified format
# @app.route('/rfc')
# def predict_iris():
#     """
#     Example endpoint returning a prediction of iris
#     ---
#     responses:
#         200:
#             description: "OK"
#     parameters:
#         -   name: s_length
#             in: query
#             type: number
#             required: true
#         -   name: s_width
#             in: query
#             type: number
#             required: true
#         -   name: p_length
#             in: query
#             type: number
#             required: true
#         -   name: p_width
#             in: query
#             type: number
#             required: true
#     """
#     s_length = request.args.get('s_length')
#     s_width = request.args.get('s_width')
#     p_length = request.args.get('p_length')
#     p_width = request.args.get('p_width')

#     # below when using post also set route(methods=['POST'])
#     # s_length = request.form['s_length']
#     # s_width = request.form['s_width']
#     # p_length = request.form['p_length']
#     # p_width = request.form['p_width']

#     prediction = model.predict(np.array([[s_length, s_width, p_length, p_width]]))

#     return str(list(prediction))

# providing input as a file
# header = None because pandas read the first role as header and since our files
# don't have headers
@app.route('/rfc', methods=['POST'])
def predict_rfc():
    """
    Endpoint returning a Random Forest model prediction of phishing URL
    ---
    responses:
        200:
            description: "OK"
    parameters:
        -   name: input_file
            in: formData
            type: file
            required: true
    """
    input_data = pd.read_csv(request.files.get('input_file'), header=None)

    prediction = rfc.predict(input_data)

    return str(list(prediction))

@app.route('/deep_learn', methods=['POST'])
def predict_dl():
    """
    Endpoint returning a Deep Learn model prediction of phishing URL
    ---
    responses:
        200:
            description: "OK"
    parameters:
        -   name: input_file
            in: formData
            type: file
            required: true
    """
    input_data = pd.read_csv(request.files.get('input_file'), header=None)

    prediction = dl.predict(input_data)

    return str(list(prediction))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)