import React, { useEffect, useState } from 'react';

export default function History({ tgInitData }) {
  const [txs, setTxs] = useState([]);
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/transactions`, {
      headers: { 'Authorization': `Bearer ${tgInitData}` }
    })
    .then(res => res.json())
    .then(data => setTxs(data))
    .catch(err => console.error(err));
  }, [tgInitData]);

  return (
    <div>
      <h2>История операций</h2>
      {txs.length === 0 ? (
        <p style={{ color: 'var(--tg-theme-hint-color)', textAlign: 'center', marginTop: '30px' }}>Операций пока не добавлено.</p>
      ) : (
        txs.map(tx => (
          <div key={tx.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px' }}>
            <div>
              <strong style={{ textTransform: 'capitalize' }}>{tx.category}</strong>
              <div style={{ fontSize: '12px', color: 'var(--tg-theme-hint-color)', marginTop: '2px' }}>
                {tx.description || tx.date}
              </div>
            </div>
            <div style={{ fontWeight: 'bold', fontSize: '16px', color: tx.type === 'income' ? '#4caf50' : 'var(--tg-theme-text-color)' }}>
              {tx.type === 'income' ? '+' : '-'}{tx.amount.toFixed(2)} {tx.currency}
            </div>
          </div>
        ))
      )}
    </div>
  );
}