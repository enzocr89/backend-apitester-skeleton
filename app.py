import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Routes de l'API

# Vérifier si le serveur est actif
@app.route('/api/alive', methods=['GET'])
def check_alive():
    return jsonify({"message": "Alive"})

@app.route('/api/associations', methods=['GET'])
def get_all_associations():
    return jsonify(associations_df['id'].tolist())
    
@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(association.iloc[0].to_dict())

# Liste de tous les événements
@app.route('/api/evenements', methods=['GET'])
def get_all_events():
    return jsonify(evenements_df['id'].tolist())

@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_event(id):
    event = evenements_df[evenements_df['id'] == id]
    if event.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.iloc[0].to_dict())

@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_association_events(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        return jsonify({"error": "Association not found"}), 404
    
    events = evenements_df[evenements_df['association_id'] == id]
    return jsonify(events.to_dict(orient='records'))

@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    filtered_associations = associations_df[associations_df['type'] == type]
    return jsonify(filtered_associations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=False)

