import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/connection_logs', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setLogs(data);
      }
    };

    fetchLogs();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      <h2 className="text-2xl font-bold mb-4">Connection Logs</h2>
      <div className="bg-gray-800 p-4 rounded-lg">
        <pre>{JSON.stringify(logs, null, 2)}</pre>
      </div>
    </div>
  );
}

export default Dashboard;
