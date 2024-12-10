import os
import requests
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv

FDA_API_URL = "https://api.fda.gov/food/enforcement.json"
FDA_API_QUERY = {"search": 'distribution_pattern:"nationwide"', "limit": 5}

load_dotenv()

app = FastAPI()

# MongoDB connection
# mongodb+srv://<username>:<password>@palabras-express-api.whbeh.mongodb.net/?retryWrites=true&w=majority&
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.get("/")
def root():
    return {"message": "Welcome to the FDA Enforcement Data API."}
    
@app.get("/update-data")
def update_data():
    response = requests.get(FDA_API_URL, params=FDA_API_QUERY)
    data = response.json()
    return data