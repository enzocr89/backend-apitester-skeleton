
## VERSION SANS FLASK_CORS
import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
data = pl.Path(__file__).parent.absolute() / 'data'

associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')


def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = make_response()
    return add_cors_headers(response)


# Vérifier si le serveur est actif
@app.route('/api/alive', methods=['GET'])
def check_alive():
    response = jsonify({"message": "Alive"})
    return add_cors_headers(response)

@app.route('/api/associations', methods=['GET'])
def get_all_associations():
    response = jsonify(associations_df['id'].tolist())
    return add_cors_headers(response)

# Détails d'une association
@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        response = jsonify({"error": "Association not found"}), 404
    else:
        response = jsonify(association.iloc[0].to_dict())
    return add_cors_headers(response)


@app.route('/api/evenements', methods=['GET'])
def get_all_events():
    response = jsonify(evenements_df['id'].tolist())
    return add_cors_headers(response)

@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_event(id):
    event = evenements_df[evenements_df['id'] == id]
    if event.empty:
        response = jsonify({"error": "Event not found"}), 404
    else:
        response = jsonify(event.iloc[0].to_dict())
    return add_cors_headers(response)

# Liste des événements d'une association
@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_association_events(id):
    # Vérifier si l'association existe
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        response = jsonify({"error": "Association not found"}), 404
    else:
        # Récupérer les événements de cette association
        events = evenements_df[evenements_df['association_id'] == id]
        response = jsonify(events.to_dict(orient='records'))
    return add_cors_headers(response)

@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    filtered_associations = associations_df[associations_df['type'] == type]
    response = jsonify(filtered_associations.to_dict(orient='records'))
    return add_cors_headers(response)


@app.after_request
def after_request(response):
    return add_cors_headers(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
