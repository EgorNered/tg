import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Analytics({ currency, tgInitData }) {
  const [summary, setSummary] = useState(null);
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/analytics/summary?currency=${currency}`, {
      headers: { 'Authorization': `Bearer ${tgInitData}` }
    })
    .then(res => res.json())
    .then(data => setSummary(data));
  }, [currency, tgInitData]);

  if (!summary || summary.categories.length === 0) {
    return (
      <div>
        <h2>Аналитика трат</h2>
        <p style={{ color: 'var(--tg-theme-hint-color)', textAlign: 'center', marginTop: '40px' }}>
          Добавьте расходы в валюте {currency}, чтобы увидеть диаграмму.
        </p>
      </div>
    );
  }

  const chartData = {
    labels: summary.categories.map(c => c.category),
    datasets: [{
      data: summary.categories.map(c => c.amount),
      backgroundColor: ['#f44336', '#2481cc', '#ffeb3b', '#e91e63', '#4caf50', '#9c27b0', '#ff9800'],
      borderWidth: 0
    }]
  };

  return (
    <div>
      <h2>Распределение трат ({currency})</h2>
      <div style={{ maxWidth: '280px', margin: '30px auto' }}>
        <Doughnut data={chartData} options={{ plugins: { legend: { position: 'bottom' } } }} />
      </div>
    </div>
  );
}