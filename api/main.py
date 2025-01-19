import os
import requests
import schedule
import time 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables from a .env file (if it exists)
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # Allow all requests, Alternative is to use allow_origins["http://localhost:3000"]
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# MongoDB configuration using environment variables
# mongodb+srv://<username>:<password>@palabras-express-api.whbeh.mongodb.net/?retryWrites=true&w=majority&
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# API endpoint
FDA_API_URL = "https://api.fda.gov/food/enforcement.json"
FDA_API_QUERY = {"search": 'distribution_pattern:"nationwide"', "limit": 15}

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def format_data(record):
	"""
	Convert MongoDB records to JSON serialable format.
	"""
	if "_id" in record:
		record["_id"] = str(record["_id"])
	return record

def get_data():
	"""
	Retrieve data from the MongoDB database.
	"""
	try:
		data = list(collection.find())
		print(data)
		return data
	except Exception as e:
		print(f"Error: {e}")

def fetch_and_update_data():
	"""
	Fetch data from the FDA API and update MongoDB.
	"""
	try:
		response = requests.get(FDA_API_URL, params=FDA_API_QUERY)
		response.raise_for_status() # Raise an error for bad status codes
		data = response.json()

		# Insert or update records in MongoDB
		for record in data.get("results", []):
			collection.update_one(
				{"_id": record["recall_number"]}, # Use recall_number as unique ID
				{"$set": record},
				upsert=True
			)
		print("Data successfully updated.")
	except Exception as e:
		print(f"Error fetching data: {e}")
		
# Schedule the task to run once a week
schedule.every().week.do(fetch_and_update_data)

# Background job for running the schedule
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.get("/")
def root():
	"""
	Root endpoint to provide a welcome message.
	"""
	return {"message": "Welcome to the FDA Enforcement Data API. Visit /update-data to manually update data."}

# Get Data from MongoDB
@app.get("/data")
def get_data():
	"""
	Retrieve data from MongoDB.
	"""
	try:
		data = list(collection.find())
		# Convert ObjectId to string for JSON serialization
		formatted_data = [format_data(record) for record in data]
		return {"data": formatted_data}
	except Exception as e:
		return {"error": f"An error occorred: {e}"}

# FastAPI route to trigger data update manually
@app.get("/update-data")
def update_data():
	"""
	Endpoint to trigger data fetching and updating manually.
	"""
	fetch_and_update_data()
	return {"message": "Data update triggered."}

if __name__ == "__main__":
    import threading
    # Run the scheduler in a separate thread
    threading.Thread(target=run_schedule, daemon=True).start()
    
    # Start FastAPI
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)