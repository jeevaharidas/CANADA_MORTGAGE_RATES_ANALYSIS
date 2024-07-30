import pandas as pd
import json
from pymongo import MongoClient

# Load the CSV file
csv_file_path = '/Users/ernestgaisie/Desktop/Final Projects/CANADA_MORTGAGE_RATES_ANALYSIS/cleaned_34100133.csv'
df = pd.read_csv(csv_file_path)

# Convert to JSON
json_data = json.loads(df.to_json(orient='records'))

# MongoDB connection details
mongo_uri = "mongodb+srv://ernestyawgaisie:ernestyawgaisie@cluster0.dvjsafm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "MortgageData"
collection_name = "Mortgages"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Insert JSON data into MongoDB
collection.insert_many(json_data)

print("Data has been uploaded to MongoDB")
