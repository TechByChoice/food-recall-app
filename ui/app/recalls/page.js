"use client"

import { useEffect, useState } from "react";
import RecallList from "./../../(components)/RecallList";
import axios from "axios";

export default function Recalls() {
  const [recalls, setRecalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from FastAPI
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/data");
        console.log('response.data.data :>> ', response.data.data);
        setRecalls(response.data.data || []);
        setLoading(false);
      } catch (error) {
        setError(`Failed to fetch recalls. Please try again later. Error: ${error}`);
        setLoading(false);
      }
    };
    fetchData();
  }, []);
  console.log('recalls :>> ', recalls);

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{color: "red"}}>{error}</p>;

  return (
    <div style={{padding: "2rem"}}>
      <h1>FDA Food Recalls</h1>
      <RecallList recalls={recalls} />
    </div>
  )
  
}