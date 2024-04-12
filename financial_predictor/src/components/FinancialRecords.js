import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FinancialRecords() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('/api/financial-records/');
      setRecords(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h1>Financial Records</h1>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {records.map(record => (
            <tr key={record.id}>
              <td>{record.category}</td>
              <td>{record.amount}</td>
              <td>{record.date}</td>
              <td>{record.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FinancialRecords;
