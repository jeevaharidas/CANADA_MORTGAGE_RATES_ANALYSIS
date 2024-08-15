from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB connection details
mongo_uri = "mongodb+srv://ernestyawgaisie:ernestyawgaisie@cluster0.dvjsafm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "MortgageData"
collection_name = "Mortgages"

# Connecting to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Sample request: /data?geo=Toronto&value_min=500000&value_max=1000000&ref_date_min=202001&ref_date_max=202012&page=1&limit=10


@app.route('/data', methods=['GET'])
def get_data():
    filters = {'Type of unit': 'One bedroom units'}
    if 'type_of_structure' in request.args:
        filters['Type of structure'] = request.args['type_of_structure']
    if 'geo' in request.args:
        filters['GEO'] = {"$regex": request.args['geo'], "$options": "i"}
    if 'terminated' in request.args:
        filters['TERMINATED'] = request.args['terminated']
    if 'value_min' in request.args and 'value_max' in request.args:
        filters['VALUE'] = {'$gte': float(
            request.args['value_min']), '$lte': float(request.args['value_max'])}
    if 'ref_date_min' in request.args and 'ref_date_max' in request.args:
        filters['REF_DATE'] = {'$gte': int(
            request.args['ref_date_min']), '$lte': int(request.args['ref_date_max'])}

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    skip = (page - 1) * limit

    data = list(collection.find(filters).skip(skip).limit(limit))
    for item in data:
        item['_id'] = str(item['_id'])

    return jsonify(data)

# Sample request: /data/average_price?location=Toronto


@app.route('/data/average_price', methods=['GET'])
def get_average_price():
    location = request.args.get('location')
    if location:
        avg_price = collection.aggregate([
            {"$match": {"GEO": {"$regex": location, "$options": "i"},
                        "Type of unit": "One bedroom units"}},
            {"$group": {"_id": None, "average_price": {"$avg": "$VALUE"}}}
        ])
        avg_price = list(avg_price)
        if avg_price:
            return jsonify({"location": location, "type_of_unit": "One bedroom units", "average_price": avg_price[0]["average_price"]})
    return jsonify({"error": "Location not found or no data available"}), 404

# Sample request: /data/listings_count?location=Toronto


@app.route('/data/listings_count', methods=['GET'])
def get_listings_count():
    location = request.args.get('location')
    if location:
        listings_count = collection.count_documents(
            {"GEO": {"$regex": location, "$options": "i"}, "Type of unit": "One bedroom units"})
        return jsonify({"location": location, "type_of_unit": "One bedroom units", "listings_count": listings_count})
    return jsonify({"error": "Location not found or no data available"}), 404

# Sample request: /data/price_trend?location=Toronto&year=2024


@app.route('/data/price_trend', methods=['GET'])
def get_price_trend():
    location = request.args.get('location')
    year = int(request.args.get('year'))

    if location and year:
        price_trend = collection.aggregate([
            {"$match": {"GEO": {"$regex": location, "$options": "i"},
                        "REF_DATE": year, "Type of unit": "One bedroom units"}},
            {"$group": {
                "_id": {"year": "$REF_DATE"},
                "average_price": {"$avg": "$VALUE"}
            }},
            {"$sort": {"_id.year": 1}}
        ])
        trend_data = [{"year": result["_id"]["year"],
                       "average_price": result["average_price"]} for result in price_trend]
        return jsonify(trend_data)
    return jsonify({"error": "Location or year not found or no data available"}), 404

# New endpoint: /data/mortgage_range?location=Toronto


@app.route('/data/mortgage_range', methods=['GET'])
def get_mortgage_range():
    location = request.args.get('location')

    if location:
        result = collection.aggregate([
            {"$match": {"GEO": {"$regex": location, "$options": "i"},
                        "Type of unit": "One bedroom units"}},
            {"$group": {
                "_id": None,
                "highest_mortgage": {"$max": "$VALUE"},
                "lowest_mortgage": {"$min": "$VALUE"}
            }}
        ])
        result = list(result)
        if result:
            return jsonify({
                "location": location,
                "type_of_unit": "One bedroom units",
                "highest_mortgage": result[0]["highest_mortgage"],
                "lowest_mortgage": result[0]["lowest_mortgage"]
            })
    return jsonify({"error": "Location not found or no data available"}), 404


@app.route('/data/prices_over_time/<location>', methods=['GET'])
def get_prices_over_time(location):
    # Default to 1987 if not provided
    year_min = int(request.args.get('year_min', 1987))
    # Default to 2024 if not provided
    year_max = int(request.args.get('year_max', 2024))

    # MongoDB aggregation pipeline
    price_trend = collection.aggregate([
        {"$match": {
            "GEO": {"$regex": location, "$options": "i"},
            "REF_DATE": {"$gte": year_min, "$lte": year_max}
        }},
        {"$group": {
            "_id": "$REF_DATE",
            "average_price": {"$avg": "$VALUE"}
        }},
        {"$sort": {"_id": 1}}
    ])

    trend_data = [{"year": result["_id"], "average_price": result["average_price"]}
                  for result in price_trend]

    if trend_data:
        return jsonify({"location": location, "price_trend": trend_data})
    else:
        return jsonify({"error": "No data found for the specified location and year range"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=6002)
