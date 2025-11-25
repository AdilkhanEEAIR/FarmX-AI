import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  const location = useLocation();

  return (
    <header className="header">
      <div className="header-content">
        <h1 className="logo">
          🌱 AgroAI
        </h1>
        <nav className="nav">
          <Link 
            to="/plant-analysis" 
            className={`nav-link ${location.pathname === '/plant-analysis' ? 'active' : ''}`}
          >
            Анализ растений
          </Link>
          <Link 
            to="/agro-gpt" 
            className={`nav-link ${location.pathname === '/agro-gpt' ? 'active' : ''}`}
          >
            AgroGPT
          </Link>
          <Link 
            to="/yield-prediction" 
            className={`nav-link ${location.pathname === '/yield-prediction' ? 'active' : ''}`}
          >
            Прогноз урожая
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;