import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { checkBackendConnection } from './services/api';
import './App.css';
import Header from './components/Header';
import PlantAnalysis from './components/PlantAnalysis/PlantAnalysis';
import AgroGPT from './components/AgroGPT/AgroGPT';
import YieldPrediction from './components/YieldPrediction/YieldPrediction';

function App() {
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);

  useEffect(() => {
    const checkConnection = async () => {
      const connected = await checkBackendConnection();
      setBackendConnected(connected);
    };

    checkConnection();
  }, []);

  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          {/* Показываем статус подключения */}
          {backendConnected === false && (
            <div className="connection-warning">
              ⚠️ Внимание: Не удалось подключиться к бэкенду. Убедитесь, что сервер запущен на порту 8000.
            </div>
          )}
          
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/plant-analysis" element={<PlantAnalysis />} />
            <Route path="/agro-gpt" element={<AgroGPT />} />
            <Route path="/yield-prediction" element={<YieldPrediction />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

const HomePage: React.FC = () => {
  return (
    <div className="home-page">
      <h1>Agro AI Platform</h1>
      <p>Интеллектуальная платформа для современных агрономов</p>
      <div className="features-grid">
        <div className="feature-card">
          <h3>🔍 Анализ растений</h3>
          <p>Определите болезни растений по фотографии</p>
        </div>
        <div className="feature-card">
          <h3>🤖 AgroGPT</h3>
          <p>AI-консультант по вопросам агрономии</p>
        </div>
        <div className="feature-card">
          <h3>📈 Прогноз урожайности</h3>
          <p>Предсказание урожая на основе данных</p>
        </div>
      </div>
    </div>
  );
};

export default App;