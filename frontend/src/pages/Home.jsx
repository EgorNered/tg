import React, { useEffect, useState } from 'react';

export default function Home({ currency, setCurrency, tgInitData }) {
  const [summary, setSummary] = useState({ total_income: 0, total_expense: 0, balance: 0, categories: [] });
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/analytics/summary?currency=${currency}`, {
      headers: { 'Authorization': `Bearer ${tgInitData}` }
    })
    .then(res => {
      if (!res.ok) {
        throw new Error('Ошибка авторизации или сервера');
      }
      return res.json();
    })
    .then(data => setSummary(data))
    .catch(err => {
      console.error('Ошибка получения аналитики:', err);
      // В случае ошибки сбрасываем в дефолтное безопасное состояние
      setSummary({ total_income: 0, total_expense: 0, balance: 0, categories: [] });
    });
  }, [currency, tgInitData, API_URL]);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h2 style={{ margin: 0 }}>Мой Баланс</h2>
        <select value={currency} onChange={(e) => setCurrency(e.target.value)} style={{ width: '90px', padding: '6px' }}>
          <option value="BYN">BYN</option>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="RUB">RUB</option>
        </select>
      </div>

      <div className="card" style={{ textAlign: 'center', padding: '24px 16px' }}>
        <div className="card-title">Текущий остаток</div>
        <h1 style={{ margin: 0, fontSize: '32px', color: (summary?.balance || 0) >= 0 ? '#4caf50' : '#f44336' }}>
          {(summary?.balance ?? 0).toFixed(2)} {currency}
        </h1>
      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <div className="card" style={{ flex: 1, backgroundColor: 'rgba(76, 175, 80, 0.08)', textAlign: 'center', margin: 0 }}>
          <div className="card-title" style={{ color: '#4caf50' }}>Доходы</div>
          <div style={{ fontSize: '18px', color: '#4caf50', fontWeight: 'bold' }}>
            +{(summary?.total_income ?? 0).toFixed(2)}
          </div>
        </div>
        <div className="card" style={{ flex: 1, backgroundColor: 'rgba(244, 67, 54, 0.08)', textAlign: 'center', margin: 0 }}>
          <div className="card-title" style={{ color: '#f44336' }}>Расходы</div>
          <div style={{ fontSize: '18px', color: '#f44336', fontWeight: 'bold' }}>
            -{(summary?.total_expense ?? 0).toFixed(2)}
          </div>
        </div>
      </div>

      <h3 style={{ marginBottom: '10px' }}>Бюджет и лимиты</h3>
      {(!summary?.categories || summary.categories.filter(c => c.limit > 0).length === 0) ? (
        <p style={{ color: 'var(--tg-theme-hint-color)', fontSize: '14px' }}>Лимиты пока не установлены.</p>
      ) : (
        summary.categories.filter(c => c.limit > 0).map(cat => {
          const percent = Math.min(((cat.amount || 0) / cat.limit) * 100, 100);
          return (
            <div key={cat.category} className="card" style={{ padding: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '6px' }}>
                <span style={{ textTransform: 'capitalize', fontWeight: '500' }}>{cat.category}</span>
                <span>{(cat.amount || 0).toFixed(2)} / {cat.limit} {currency}</span>
              </div>
              <div style={{ width: '100%', backgroundColor: 'rgba(0,0,0,0.1)', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${percent}%`, backgroundColor: percent >= 90 ? '#f44336' : 'var(--tg-theme-button-color, #2481cc)', height: '100%' }}></div>
              </div>
            </div>
          )
        })
      )}
    </div>
  );
}