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

export default function TopDecade({ ranking, removeStopWords, dictionaryOnly }) {
    const[decade, setDecade] = useState([]);
    const[userDecade, setUserDecade] = useState('');
    const[decadeData, setDecadeData] = useState([]); 

    useEffect(() => {
        async function fetchDecades() {
            const response = await fetch('http://localhost:5001/api/decades'); 
            const data = await response.json();
            setDecade(data.data); 
        }

        fetchDecades(); 
    }, []);

    useEffect(() => {
        if (!userDecade) return;

        async function fetchUserDecade() {
            const response = await fetch(
                `http://localhost:5001/api/top-words?decade=${userDecade}&limit=10&ranking=${ranking}&removeStopWords=${removeStopWords}&dictionaryOnly=${dictionaryOnly}`
            );

            const data = await response.json(); 
            setDecadeData(data.data);
        }
        
        fetchUserDecade(); 
    }, [userDecade, ranking, removeStopWords, dictionaryOnly]);

    function handleChange(e) {
        setUserDecade(e.target.value);
    }

    const barData = {
        labels: decadeData.map(t => t.word),
        datasets: [
            {
                label: "Total Matches",
                data: decadeData.map(t => t.total_matches),
                backgroundColor: "blue"
            }
        ]
    }

    return (
        <div>
            <div className="dropdown">
                <label>Select a decade: </label>

                <select 
                    name="decade" 
                    value={userDecade} 
                    onChange={handleChange}
                >
                    {decade.map(t => <option key={t}>{t}</option>)}
                </select>
            </div>

            <div className="chart">
                <Bar data={barData} />
            </div>
        </div>
    );
}