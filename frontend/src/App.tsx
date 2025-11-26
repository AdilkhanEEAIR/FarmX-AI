import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
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
  const navigate = useNavigate();

  const features = [
    {
      id: 1,
      title: "🔍 Анализ растений",
      description: "Определите болезни растений по фотографии",
      path: "/plant-analysis",
      gradient: "var(--success-gradient)",
      icon: "🔍"
    },
    {
      id: 2,
      title: "🤖 AgroGPT",
      description: "AI-консультант по вопросам агрономии",
      path: "/agro-gpt",
      gradient: "var(--blue-gradient)",
      icon: "🤖"
    },
    {
      id: 3,
      title: "📈 Прогноз урожайности",
      description: "Предсказание урожая на основе данных",
      path: "/yield-prediction",
      gradient: "var(--orange-gradient)",
      icon: "📈"
    }
  ];

  const handleCardClick = (path: string) => {
    navigate(path);
  };

  return (
    <div className="home-page">
      <h1>Agro AI Platform</h1>
      <p>Интеллектуальная платформа для современных агрономов</p>
      <div className="features-grid">
        {features.map((feature) => (
          <div 
            key={feature.id}
            className="feature-card"
            onClick={() => handleCardClick(feature.path)}
            style={{ '--card-gradient': feature.gradient } as React.CSSProperties}
          >
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
            <div className="feature-arrow">→</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;