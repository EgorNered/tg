import React from 'react';

export default function Layout({ children, currentTab, setCurrentTab }) {
  const tabs = [
    { id: 'home', label: 'Главная', icon: '🏠' },
    { id: 'add', label: 'Добавить', icon: '➕' },
    { id: 'history', label: 'История', icon: '📜' },
    { id: 'analytics', label: 'Аналитика', icon: '📊' }
  ];

  return (
    <div style={{ paddingBottom: '80px', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '16px', flex: 1 }}>
        {children}
      </div>
      
      <nav style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        height: '65px',
        backgroundColor: 'var(--tg-theme-secondary-bg-color, #f5f5f5)',
        borderTop: '1px solid var(--tg-theme-hint-color, #ddd)',
        display: 'flex',
        justifyContent: 'space-around',
        alignItems: 'center',
        zIndex: 1000,
        paddingBottom: 'env(safe-area-inset-bottom)' /* Фикс для айфонов с челкой снизу */
      }}>
        {tabs.map(tab => (
          <div 
            key={tab.id} 
            onClick={() => setCurrentTab(tab.id)}
            style={{
              textAlign: 'center',
              cursor: 'pointer',
              fontSize: '11px',
              color: currentTab === tab.id ? 'var(--tg-theme-button-color, #2481cc)' : 'var(--tg-theme-hint-color, #999)',
              fontWeight: currentTab === tab.id ? 'bold' : 'normal',
              flex: 1
            }}
          >
            <div style={{ fontSize: '20px', marginBottom: '2px' }}>{tab.icon}</div>
            {tab.label}
          </div>
        ))}
      </nav>
    </div>
  );
}