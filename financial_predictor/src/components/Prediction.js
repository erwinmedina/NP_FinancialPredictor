import React, { useState } from 'react';
import axios from 'axios';

function MLComponent() {
  const [predictions, setPredictions] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.post('/api/ml-endpoint/', { data: 'example' });
      setPredictions(response.data.predictions);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <button onClick={fetchData}>Run ML Script</button>
      {predictions && <p>Predictions: {predictions}</p>}
    </div>
  );
}

export default MLComponent;
