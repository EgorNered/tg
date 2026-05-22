import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import Home from './pages/Home';
import AddTransaction from './pages/AddTransaction';
import History from './pages/History';
import Analytics from './pages/Analytics';

export default function App() {
  const [currentTab, setCurrentTab] = useState('home');
  const [currency, setCurrency] = useState('BYN');
  const [tgInitData, setTgInitData] = useState('');

  useEffect(() => {
    // Проверяем, запущено ли приложение внутри Telegram
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand(); // Разворачиваем окно на максимум вверх
      
      // Передаем реальную строку инициализации для бэкенда
      setTgInitData(tg.initData);
    } else {
      // Заглушка для разработки в обычном браузере
      // Хэш ванильный, бэкенд пропустит только если отключить проверку (для тестов в браузере)
      const mockInitData = "user=%7B%22id%22%3A123456%2C%22first_name%22%3A%22Egor%22%7D&hash=mock";
      setTgInitData(mockInitData);
    }
  }, []);

  const renderContent = () => {
    switch (currentTab) {
      case 'home': return <Home currency={currency} setCurrency={setCurrency} tgInitData={tgInitData} />;
      case 'add': return <AddTransaction currency={currency} tgInitData={tgInitData} onSave={() => setCurrentTab('home')} />;
      case 'history': return <History tgInitData={tgInitData} />;
      case 'analytics': return <Analytics currency={currency} tgInitData={tgInitData} />;
      default: return <Home currency={currency} setCurrency={setCurrency} tgInitData={tgInitData} />;
    }
  };

  return (
    <Layout currentTab={currentTab} setCurrentTab={setCurrentTab}>
      {renderContent()}
    </Layout>
  );
}