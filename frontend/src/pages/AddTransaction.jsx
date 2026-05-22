import React, { useState } from 'react';

export default function AddTransaction({ currency, tgInitData, onSave }) {
  const [isLimitMode, setIsLimitMode] = useState(false);
  const [type, setType] = useState('expense');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('еда');
  const [description, setDescription] = useState('');
  
  const categories = ['еда', 'транспорт', 'жильё', 'развлечения', 'здоровье', 'одежда', 'другое'];
  const API_URL = import.meta.env.VITE_API_URL;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!amount || isNaN(amount)) return;

    const endpoint = isLimitMode ? '/api/transactions/limits' : '/api/transactions';
    const payload = isLimitMode 
      ? { category, limit_amount: parseFloat(amount), currency }
      : { type, amount: parseFloat(amount), currency, category, date: new Date().toISOString().split('T')[0], description };

    fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tgInitData}`
      },
      body: JSON.stringify(payload)
    })
    .then(res => {
      if (res.ok) {
        // Вызываем вибрацию смартфона (Haptic Feedback) через SDK Telegram
        if (window.Telegram?.WebApp?.HapticFeedback) {
          window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
        }
        onSave();
      }
    });
  };

  return (
    <div>
      <div style={{ display: 'flex', marginBottom: '20px', gap: '8px' }}>
        <button type="button" onClick={() => setIsLimitMode(false)} style={{ backgroundColor: !isLimitMode ? 'var(--tg-theme-button-color)' : 'rgba(0,0,0,0.05)', color: !isLimitMode ? '#fff' : 'var(--tg-theme-text-color)', flex: 1, margin: 0, borderRadius: '8px' }}>Операция</button>
        <button type="button" onClick={() => setIsLimitMode(true)} style={{ backgroundColor: isLimitMode ? 'var(--tg-theme-button-color)' : 'rgba(0,0,0,0.05)', color: isLimitMode ? '#fff' : 'var(--tg-theme-text-color)', flex: 1, margin: 0, borderRadius: '8px' }}>Лимит</button>
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {!isLimitMode && (
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="expense">Расход</option>
            <option value="income">Доход</option>
          </select>
        )}

        <input 
          type="number" 
          step="0.01" 
          inputMode="decimal"
          placeholder={isLimitMode ? "Сумма лимита" : "Сумма"} 
          value={amount} 
          onChange={(e) => setAmount(e.target.value)} 
          required 
        />

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map(cat => <option key={cat} value={cat} style={{textTransform: 'capitalize'}}>{cat}</option>)}
        </select>

        {!isLimitMode && (
          <input 
            type="text" 
            placeholder="Комментарий (необязательно)" 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
          />
        )}

        <button type="submit" style={{ padding: '14px', marginTop: '10px' }}>Сохранить</button>
      </form>
    </div>
  );
}