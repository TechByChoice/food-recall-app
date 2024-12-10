import os
from fastapi import FastAPI
from pymongo import MongoClient



load_dotenv()

app = FastAPI()

# MongoDB connection
# mongodb+srv://<username>:<password>@palabras-express-api.whbeh.mongodb.net/?retryWrites=true&w=majority&
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


@app.get("/")
def root():
    return {"message": "Welcome to the FDA Enforcement Data API."}