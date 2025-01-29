from litestar import Litestar, get
from litestar.response import Response
from typing import Dict, List
from litestar.config.cors import CORSConfig
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import httpx
import os
from dotenv import load_dotenv
from bson.json_util import dumps, loads

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# FDA API configuration 
FDA_API_URL = "https://api.fda.gov/food/enforcement.json"
FDA_API_QUERY = {"search": 'distribution_pattern:"nationwide"', "limit": 15}

async def get_db():
	client = AsyncIOMotorClient(MONGO_URI)
	return client[DB_NAME]

def format_data(record):
	"""
	Convert MongoDB records to JSON serializable format
	"""
	if "_id" in record:
		record["_id"] = str(record["_id"])
	return record


@get("/")
async def index() -> str:
	return "Welcome to the FDA Recall API"

@get("/data")
async def get_recalls() -> Response[Dict[str, List[dict]]]:
	db = await get_db()
	recalls = await db[COLLECTION_NAME].find().to_list(1000)
	# Convert BSON to JSON-serializable format
	serialized_recalls = [format_data(record) for record in recalls]
	return Response({"recalls": serialized_recalls})

@get("/update")
async def update_recalls() -> Dict[str, str]:
	async with httpx.AsyncClient() as client:
		response = await client.get(FDA_API_URL, params=FDA_API_QUERY)
		data = response.json()
		
		# Print FDA API response data
		print("FDA API Response:")
		print("Total Results:", len(data.get("results", [])))
		for recall in data.get("results", []):
				print(f"Recall Number: {recall.get('recall_number')}")
				print(f"Product: {recall.get('product_description')}")
				print(f"Reason: {recall.get('reason_for_recall')}")
				print("---")
		
	db = await get_db()
	await db[COLLECTION_NAME].delete_many({})
	
	if data.get("results"):
		await db[COLLECTION_NAME].insert_many(data["results"])
		
	return {"message": "Database updated successfully"}

# CORS configuration
cors_config = CORSConfig(
	allow_origins=["http://localhost:3000"],
	allow_methods=["GET"],
	allow_headers=["*"]
)

# Create Litestar app
app = Litestar(
	route_handlers=[index, get_recalls, update_recalls],
	cors_config=cors_config
)