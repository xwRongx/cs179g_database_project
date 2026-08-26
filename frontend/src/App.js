import logo from './logo.svg';
import './App.css';
import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect, useState } from 'react';

function App() {

  const [trendData, setTrendData] = useState([]);
  // Fetch trend data for input keyword 
  useEffect(() => {
    async function fetchTrends(keyword) {
      const response = await fetch(`http://localhost:5001/api/trends?keyword=${keyword}`);
      const data = await response.json();
      console.log(`Fetched trend data for "${keyword}":`, data.data);
      setTrendData(data.data);
    }
    // User input keyword variable goes here 
    fetchTrends('radio').catch((error) => {
      console.error('Error fetching trend data:', error);
    });
  });

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <div style={{ width: '100%', height: '300px' }}>
          <LineChart 
            dataset={trendData}
            xAxis={[{ dataKey: 'year' }]}
            series={[{ dataKey: 'match_count', type: 'line' }]}
          />
        </div>
            
          
      </header>
    </div>
  );
}

export default App;