import { useState, useEffect } from 'react';

import { Bar } from 'react-chartjs-2';
import { 
    Chart as ChartJS, 
    CategoryScale, 
    LinearScale, 
    BarElement, 
    Title, 
    Tooltip, 
    Legend,
} from "chart.js";

ChartJS.register(
    CategoryScale, 
    LinearScale, 
    BarElement, 
    Title, 
    Tooltip, 
    Legend
);

export default function TopYear({ ranking, removeStopWords, dictionaryOnly }) {
    const[year, setYear] = useState([]);
    const[userYear, setUserYear] = useState('');
    const[yearData, setYearData] = useState([]); 

    useEffect(() => {
        async function fetchYear() {
            const response = await fetch('http://localhost:5001/api/decades'); 
            const data = await response.json();
            setYear(data.data); 
        }

        fetchYear(); 
    }, []);

    useEffect(() => {
        if (!userYear) return;

        async function fetchUserYear() {
            const response = await fetch(
                `http://localhost:5001/api/top-words-year?year=${userYear}&ranking=${ranking}&removeStopWords=${removeStopWords}&dictionaryOnly=${dictionaryOnly}`
            );

            const data = await response.json(); 
            setYearData(data.data);
        }
        
        fetchUserYear(); 
    }, [userYear, ranking, removeStopWords, dictionaryOnly]);

    function handleChange(e) {
        setUserYear(e.target.value);
    }

    const barData = {
        datasets: [
            {
                label: "Total Matches",
                data: yearData.map(t => t.total_matches),
                backgroundColor: "blue"
            }
        ]
    }

    const barOptions = {
         scales: {
            x: {
                labels: yearData.map(t => t.word)
            },
            x2: {
                labels: yearData.map(t => t.year)
            }
         }
    }

    return (
        <div>
            <div className="dropdown">
                <label>Select a starting year: </label>

                <select 
                    name="year" 
                    value={userYear} 
                    onChange={handleChange}
                >
                    {year.map(t => <option key={t}>{t}</option>)}
                </select>
            </div>

            <div className="chart">
                <Bar data={barData} options={barOptions}/>
            </div>
        </div>
    );
}