# Building a Food Recall Tracking App with Python, FastAPI, and MongoDB (Part 0)

Food recalls can have significant impacts on public health and safety, but tracking and understanding these recalls can be challenging. This multipart tutorial series will guide you through creating a food recall tracking tool that leverages the FDA's food recall API. In this first part, we'll focus on building the backend API with Python, FastAPI, and MongoDB to pull and store data from the FDA API. Future installments will cover the frontend, built using Next.js, and additional features like machine learning and conversational interfaces.

---

## Why Python and FastAPI?

### Python + FastAPI
FastAPI is a modern web framework for building APIs in Python. It is:
- **Fast**: Built on Starlette and Pydantic, it offers excellent performance.
- **Easy to use**: Automatic data validation and documentation.
- **Scalable**: Asynchronous support makes it well-suited for high-concurrency applications.

Other Python API libraries, like Flask or Django REST Framework, are powerful but may require additional configuration for asynchronous support and automatic validation.

### Why Not Node.js or Full-Stack Next.js?
While Node.js or a full-stack Next.js app could also handle this project, Python's robust data-processing libraries make it ideal for adding machine learning (ML) capabilities later. With Python, I can integrate ML models to analyze and predict trends in food recalls or implement retrieval-augmented generation (RAG) systems to enable conversational interactions.

All that being true, I chose Python because I wanted to build something with Python. I've been intrigued by the tool for years and I've built plenty of tools with Node.js. I'm excited to learn more about Python and this won't be the last thing I build with it.

---

## Backend Architecture Overview

The backend will:
1. **Fetch data from the FDA API**: Regularly query the FDA's food enforcement API for updates on food recalls.
2. **Store data in MongoDB**: Use MongoDB to persist food recall data, ensuring users can query historical data.
3. **Expose API endpoints**: Provide endpoints for manual updates and status checks.

Technologies used:
- **Python**: Core programming language.
- **FastAPI**: Framework for building the API.
- **MongoDB**: NoSQL database to store food recall data.
- **Requests**: Library for making HTTP calls to the FDA API.
- **Schedule**: Library to automate weekly data-fetching tasks.

---

## Step-by-Step Guide

### Step 1: Set Up the Environment

#### Create a Virtual Environment
Using a virtual environment helps isolate your project’s dependencies.

```bash
# Create and activate a virtual environment
python -m venv tbcvenv # venv initiates the virtual environment and tbcvenv is the name of the virtual environment. You may use any name you choose
source tbcvenv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Required Libraries
We’ll use the following dependencies:
- **FastAPI**: The framework to create our API.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **pymongo**: Python driver for MongoDB.
- **python-dotenv**: To manage environment variables.
- **requests**: To fetch data from the FDA API.
- **schedule**: For automating periodic tasks.

Install them with:

```bash
pip install fastapi uvicorn pymongo python-dotenv requests schedule
```

---

### Step 2: Start with a Simple API

Create a file named `main.py` and write a very basic FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FDA Enforcement Data API."}
```

#### Explanation:
- **FastAPI**: Provides the `FastAPI` class to define the app and the `@app.get` decorator to define endpoints.
- **Root Endpoint**: Displays a simple welcome message.

Run the server with:

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the message.

---

### Step 3: Connect to MongoDB

Add MongoDB support by installing and using `pymongo`. Update `main.py`:

```python
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
```

#### Explanation:
- **pymongo**: Connects to the MongoDB server.
- **MongoClient**: Initializes the client using the MongoDB URI.
- **Database/Collection**: We define `fda_db` as the database and `enforcements` as the collection for storing data.

Ensure MongoDB is running locally or use a cloud-hosted MongoDB instance (e.g., MongoDB Atlas).

---

### Step 4: Fetch Data from the FDA API

Update `main.py` to fetch data using `requests`:

```python
import requests
from fastapi import FastAPI
from pymongo import MongoClient
import os
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
```

#### Explanation:
- **requests**: Fetches data from the FDA API.
- **FDA_API_URL**: Endpoint to retrieve food recall data.
- **FDA_API_QUERY**: Parameters for the API call.

Visit [http://127.0.0.1:8000/update-data](http://127.0.0.1:8000/update-data) to see the data fetched from the FDA API.

---

### Step 5: Store Data in MongoDB

Extend `/update-data` to store the fetched data in MongoDB:

```python
import requests
from fastapi import FastAPI
from pymongo import MongoClient
import os
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

    for record in data.get("results", []):
        collection.update_one(
            {"_id":
	            record["recall_number"]},
            {"$set": record},
            upsert=True
        )

    return {"message": "Data successfully updated."}
```

#### Explanation:
- **MongoDB Storage**: Each record uses `recall_number` as a unique identifier (`_id`).
- **Upsert**: Updates an existing record or inserts it if it doesn’t exist.

---

### Step 6: Automate Updates with `schedule`

Add a scheduler to automate data fetching weekly:

```python
import requests
from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import schedule
import time  

# Load environment variables from a .env file (if it exists)
load_dotenv()

app = FastAPI()

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
```

#### Explanation:
- **schedule**: Schedules tasks like `update_data` to run weekly.
- **Threading**: Runs the scheduler alongside the FastAPI server.

---

## Conclusion

This completes the first part of building the backend for a food recall tracking tool. We:
1. Created a basic FastAPI application.
2. Connected it to MongoDB.
3. Pulled and stored data from the FDA API.
4. Automated data fetching with `schedule`.

In the next part, we’ll build a frontend using Next.js to display and interact with the data. Stay tuned!

Did you enjoy reading this tutorial?
Do you have any questions or need help using it?
What would you like to learn next?

Let me know in the comments below!
Or use the chat bubble in the lower right to chat in real time.
Schedule an appointment to talk and get a free hour of consulting using the chat bubble in the lower right corner of the screen.

