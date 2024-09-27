import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const SentimentAnalysis = () => {
  const [counts, setCounts] = useState({ negative: 0, neutral: 0, positive: 0 });

  useEffect(() => {
    const fetchSentimentCounts = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/sentiment-counts');
        setCounts(response.data);
      } catch (error) {
        console.error('Error fetching sentiment counts:', error);
      }
    };

    fetchSentimentCounts();
  }, []);

  const data = [
    { name: 'Negative', value: counts.negative },
    { name: 'Neutral', value: counts.neutral },
    { name: 'Positive', value: counts.positive },
  ];

  const COLORS = ['#EF4444', '#F59E0B', '#10B981'];

  return (
    <div className="w-full max-w-md p-4 mx-auto">
      <h2 className="mb-4 text-2xl font-bold text-center">Sentiment Analysis</h2>
      <div className="p-4 bg-white rounded-lg shadow-md">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
        <div className="grid grid-cols-3 gap-4 mt-4 text-center">
          <div className="p-2 bg-red-100 rounded">
            <p className="font-semibold">Negative</p>
            <p>{counts.negative}</p>
          </div>
          <div className="p-2 bg-yellow-100 rounded">
            <p className="font-semibold">Neutral</p>
            <p>{counts.neutral}</p>
          </div>
          <div className="p-2 bg-green-100 rounded">
            <p className="font-semibold">Positive</p>
            <p>{counts.positive}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentimentAnalysis;