import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect, useState } from 'react';

function WordTrend({ searchWord }) {

  const [trendData, setTrendData] = useState([]);

  // Fetch trend data for input keyword
  useEffect(() => {

    if (!searchWord) return;

    async function fetchTrends(keyword) {

      const response = await fetch(
        `http://localhost:5001/api/trends?keyword=${encodeURIComponent(keyword)}`
      );

      const data = await response.json();

      console.log(
        `Fetched trend data for "${keyword}":`,
        data.data
      );

      setTrendData(data.data);
    }

    fetchTrends(searchWord).catch((error) => {
      console.error(
        'Error fetching trend data:',
        error
      );
    });

  }, [searchWord]);


  return (
    <div style={{ width: '100%', height: '400px' }}>

      <LineChart
        dataset={trendData}

        xAxis={[
          {
            dataKey: 'year',
            label: 'Year'
          }
        ]}

        series={[
          {
            dataKey: 'match_count',
            label: searchWord,
            type: 'line'
          }
        ]}
      />

    </div>
  );
}

export default WordTrend;