export default function RecallList({recalls}) {

  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px"}}>
      <thead>
        <tr>
          <th style={styles.th}>Recall Number</th>
          <th style={styles.th}>Product Description</th>
          <th style={styles.th}>Reason for Recall</th>
          <th style={styles.th}>Distribution Pattern</th>
        </tr>
      </thead>
      <tbody>
        {recalls.map((recall) => (
          <tr key={recall.recall_number}>
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
    },
    td: {
      border: "1px solid #ddd",
      padding: "8px",
      textAlign: "left",
    }
  }
