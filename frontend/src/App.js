import logo from './logo.svg';
import './App.css';
import { LineChart } from '@mui/x-charts/LineChart';

// Fetch trend data for keyword "database"
function fetchTrendData() {
    return fetch('http://localhost:5000/api/trends?keyword=database')
      .then((response) => {
        return response.json().then((data) => {
          console.log('Fetched trend data for "database":', data);
          return data;
        }).catch(error => console.error('Error fetching data:', error));
      });
}

function App() {

  let trendData = null;
  fetchTrendData().then((data) => {
    trendData = data;
  })

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
        <ul>
          {trendData.map(item => (
            <li>{item[0]}</li>
          ))}
        </ul>
        <LineChart
          xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
          series={[
            {
              data: [2, 5.5, 2, 8.5, 1.5, 5],
            },
          ]}
          width={500}
          height={300}
        />
      </header>
    </div>
  );
}

export default App;
