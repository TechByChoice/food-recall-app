import Link from "next/link";

export default function Home() {
  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1>FDA Food Recall Tracker</h1>
      <p>Track food recalls from FDA API.</p>
      <Link href="/recalls">
        <button style={{padding: "10px 20px", cursor: "pointer"}}>
          View Recalls
        </button>
      </Link>
    </div>
  );
}
