from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

# MongoDB connection details
mongo_uri = "mongodb+srv://ernestyawgaisie:ernestyawgaisie@cluster0.dvjsafm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "MortgageData"
collection_name = "Mortgages"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

@app.route('/data', methods=['GET'])
def get_data():
    # Get filter parameters from the query string
    filters = {}
    if 'type_of_unit' in request.args:
        filters['Type of unit'] = request.args['type_of_unit']
    if 'type_of_structure' in request.args:
        filters['Type of structure'] = request.args['type_of_structure']
    if 'geo' in request.args:
        filters['GEO'] = request.args['geo']
    if 'terminated' in request.args:
        filters['TERMINATED'] = request.args['terminated']
    if 'value_min' in request.args and 'value_max' in request.args:
        filters['VALUE'] = {'$gte': float(request.args['value_min']), '$lte': float(request.args['value_max'])}
    if 'ref_date_min' in request.args and 'ref_date_max' in request.args:
        filters['REF_DATE'] = {'$gte': int(request.args['ref_date_min']), '$lte': int(request.args['ref_date_max'])}
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    skip = (page - 1) * limit

    # Fetch data from MongoDB based on filters with pagination
    data = list(collection.find(filters).skip(skip).limit(limit))
    for item in data:
        item['_id'] = str(item['_id'])
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
