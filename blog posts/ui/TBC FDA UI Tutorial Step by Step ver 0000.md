# Building a Simple UI with Next.js and FastAPI to Track Food Recalls Part 1

What do you get an API that has everything? A simple UI. Today we’ll create a simple user interface (UI) using Next.js to display the recall data from the Food and Drug Administration (FDA) API. We built a [Python FastAPI backend in Part 0](https://i.til.show/python-fastapi-mongodb-tutorial-food-recall-step-0). We'll connect the backend to the frontend. We'll explain the code so it's easy to follow.

---

## **Overview**

The purpose of the tool is to help users track food recalls. This project was proposed by Valerie, founder of the TechByChoice community. You may read the public project brief [HERE](https://i.til.show/tbc-os-food-recall-alerts-project-brief). 

Here’s how the UI and API work together:

1. **Backend**: The FastAPI fetches data from the FDA API and stores it in a MongoDB database. The FastAPI fetches data weekly from the FDA API because the FDA API is updated once a week. The FastAPI provides an endpoint `/data` to retrieve data from the MongoDB database.
2. **Frontend**: The Next.js application calls the FastAPI `data` endpoint to display the data in a user-friendly table.

---
### Read the [Building a Food Recall Tracking App with Python, FastAPI, and MongoDB Part 0](https://i.til.show/python-fastapi-mongodb-tutorial-food-recall-step-0) to build the API that connects to this UI tutorial.
---

## **The Technologies Used to Build the UI**

### **Backend**: Python with FastAPI
- **Why did we choose FastAPI?**
  - It's fast and asynchronous. That means it can handle many requests quickly. Supporting asynchronous code is useful for handling long-running tasks.
  - It's easy to set up.
  - It's easy to use.
  - It automatically generates documentation for your API endpoints.
  - Using Python will make it easy for us to add Machine Learning and/or AI features in the future.
  - We're using Python because I want to build something with Python. I've liked the tool for a long time and most of the stuff I build is JavaScript based. I'm excited to get going with Python.

- **Alternative Tools**: Flask or Django REST Framework.
  - **Flask** is simpler but it lacks built-in async support that FastAPI includes.
  - **Django REST Framework** is a powerful tool but will feel heavy for small projects.

### **Frontend**: Next.js
- **Why did we choose Next.js?**
  - It includes Server-side rendering (SSR) for better SEO.
  - It allows easy integration with APIs.
  - It's a React-based framework. Therefore, it’s flexible and popular. That means there's a large community of developers to help with bugs and to build tools to work with it.

- **Alternative Tools**: React or Angular.
  - **React** gives us more control, but it requires more to set it up.
  - **Angular** is powerful, but can be complex for smaller projects.

### **Database**: MongoDB
- **Why did we choose MongoDB?**
  - NoSQL database that’s great for storing JSON-like data.
  - Flexible schema design. The FDA API data is inconsistent. We can't gaurantee we'll get all the values in each object. MongoDB can handle data like this easily without causing errors.

- **Alternative Tools**: PostgreSQL or MySQL.
  - These are relational databases, better for highly structured data.

---

## **Step 1: Setting Up the Backend API**

### Add a Route to Fetch Data
We updated our FastAPI backend to include a `/data` route that retrieves food recall data from MongoDB. Here’s the code:

```python
from bson import ObjectId

@app.get("/data")
def get_data():
    """
    Retrieve data from MongoDB and return as JSON.
    """
    try:
        data = list(collection.find())
        # Convert ObjectId to string for JSON serialization
        formatted_data = [{"_id": str(record["_id"], **record)} for record in data]
        return {"data": formatted_data}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
```

### Explanation
1. **`collection.find()`**: Retrieves all records from our MongoDB.
2. **`_id` Conversion**: Converts MongoDB’s unique ID to a string so it can be used in JSON.
3. **Return JSON**: Returns the data in a format almost any frontend can use easily.

---

## **Step 2: Setting Up the Frontend**

### Create a Next.js App
1. Create the frontend folder:
   ```bash
   npx create-next-app ui
   cd ui
   ```

2. Install Axios to fetch data from the backend:
   ```bash
   npm install axios
   ```

### Directory Structure
This is what the frontend (ui) folder structure looks like:

```
ui/
├── pages/
│   ├── index.js        # Home page
│   └── recalls.js      # Page to display the food recalls
├── components/
│   └── RecallTable.js  # Component to display the table containing the food recalls
└── package.json        # This file holds all the dependencies for the UI
```

---

## **Step 3: Building the Frontend Components**

### Home Page (pages/index.js)
The home page welcomes users. It provides a button (View Recalls) to navigate to the recalls page.

```jsx
import Link from "next/link";

export default function Home() {
  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1>FDA Food Recall Tracker</h1>
      <p>Track food recalls from the FDA API.</p>
      <Link href="/recalls">
        <button style={{ padding: "10px 20px", cursor: "pointer" }}>
          View Recalls
        </button>
      </Link>
    </div>
  );
}
```

### Recall Table (components/RecallTable.js)
This component displays the recall data in a table format.

```jsx
export default function RecallTable({ recalls }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px" }}>
      <thead>
        <tr>
          <th style={styles.th}>Recall Number</th>
          <th style={styles.th}>Product Description</th>
          <th style={styles.th}>Reason</th>
          <th style={styles.th}>Distribution</th>
        </tr>
      </thead>
      <tbody>
        {recalls.map((recall) => (
          <tr key={recall._id}>
            <td style={styles.td}>{recall.recall_number}</td>
            <td style={styles.td}>{recall.product_description}</td>
            <td style={styles.td}>{recall.reason_for_recall}</td>
            <td style={styles.td}>{recall.distribution_pattern}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const styles = {
  th: {
    border: "1px solid #ddd",
    padding: "8px",
    textAlign: "left",
    backgroundColor: "#f2f2f2",
  },
  td: {
    border: "1px solid #ddd",
    padding: "8px",
    textAlign: "left",
  },
};
```

### Recalls Page (pages/recalls.js)
Fetch the data from the backend. Then pass it to the `RecallTable` component.

```jsx
import { useEffect, useState } from "react";
import axios from "axios";
import RecallTable from "../components/RecallTable";

export default function Recalls() {
  const [recalls, setRecalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/data");
        setRecalls(response.data.data);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch recalls. Please try again later.");
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>FDA Food Recalls</h1>
      <RecallTable recalls={recalls} />
    </div>
  );
}
```

---

## **Step 4: Running the Application**

1. **Start the Backend**:
   ```bash
   cd api
   uvicorn main:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   cd api
   npm run dev
   ```

3. **Access the Application**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://127.0.0.1:8000](http://127.0.0.1:8000) # `localhost` is equivalent to `127.0.0.1`

---

## **Strengths and Weaknesses**

### Strengths:
- **FastAPI**: It's easy to set up. It's great for APIs. It's ready for future machine learning and AI integration.
- **Next.js**: It's SEO-friendly. It's ideal for React-based UIs.
- **MongoDB**: It uses a flexible schema that's perfect for JSON-like data.

### Weaknesses:
- **FastAPI**: It's slightly more advanced compared to Flask for beginners and those learning to code.
- **Next.js**: It can be overkill, too much, for small UIs.
- **MongoDB**: It's less structured than relational databases. This can lead to inconsistency with the data in the database. Inconsistencies in the database can create bugs in code.

---

## **What’s Next?**
The UI and API are complete. We have a fully functional MVP. What should we do next?
We can add filters and search functionality to the UI to make it more user-friendly. We can explore how to deploy this application to the cloud also.

Tell me what you would like to do next in the comments below.
Use the chat bot in the lower right corner of the screen to chat with me in real-time, schedule a consulting meeting to discuss building custom tools, or just to talk code.

#LearnWitUS
#CodeWitUS
#BuildWitUS
#GroWitUS