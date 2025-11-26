import React, { useState } from 'react';
import { predictYield } from '../../services/api';
import './YieldPrediction.css';
import type { YieldPredictionRequest, YieldPredictionResponse } from '../../types';

const YieldPrediction: React.FC = () => {
  const [formData, setFormData] = useState<YieldPredictionRequest>({
    crop_type: 'пшеница',
    soil_quality: 7,
    rainfall: 100,
    temperature: 20,
    area: 1,
    fertilizer_used: true
  });
  
  const [prediction, setPrediction] = useState<YieldPredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const cropOptions = [
    { value: 'пшеница', label: '🌾 Пшеница', icon: '🌾' },
    { value: 'кукуруза', label: '🌽 Кукуруза', icon: '🌽' },
    { value: 'рис', label: '🍚 Рис', icon: '🍚' },
    { value: 'картофель', label: '🥔 Картофель', icon: '🥔' },
    { value: 'ячмень', label: '🌾 Ячмень', icon: '🌾' },
    { value: 'соя', label: '🫘 Соя', icon: '🫘' }
  ];

  const handleInputChange = (field: keyof YieldPredictionRequest, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await predictYield(formData);
      setPrediction(result);
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Ошибка при прогнозировании урожайности');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="yield-prediction">
      <div className="prediction-header">
        <div className="header-icon"></div>
        <div className="header-content">
          <h2>Прогноз урожайности</h2>
          <p>Рассчитайте потенциальный урожай на основе агрономических данных</p>
        </div>
      </div>
      
      <div className="prediction-main">
        <div className="form-section">
          <div className="form-card">
            <div className="form-header">
              <h3>Параметры расчета</h3>
              <div className="form-subtitle">Заполните данные для точного прогноза</div>
            </div>

            <form onSubmit={handleSubmit} className="prediction-form">
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">
                    <span className="label-icon">🌱</span>
                    Культура
                  </label>
                  <div className="select-wrapper">
                    <select
                      value={formData.crop_type}
                      onChange={(e) => handleInputChange('crop_type', e.target.value)}
                      className="form-select"
                    >
                      {cropOptions.map(option => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                    <div className="select-arrow">▼</div>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <span className="label-icon">🪴</span>
                    Качество почвы
                  </label>
                  <div className="range-container">
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={formData.soil_quality}
                      onChange={(e) => handleInputChange('soil_quality', parseFloat(e.target.value))}
                      className="form-range"
                    />
                    <div className="range-labels">
                      <span>1</span>
                      <span className="range-value">{formData.soil_quality}</span>
                      <span>10</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">
                    <span className="label-icon">💧</span>
                    Осадки (мм/месяц)
                  </label>
                  <div className="input-with-unit">
                    <input
                      type="number"
                      value={formData.rainfall}
                      onChange={(e) => handleInputChange('rainfall', parseFloat(e.target.value))}
                      className="form-input"
                      min="0"
                      max="500"
                    />
                    <span className="input-unit">мм</span>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">
                    <span className="label-icon">🌡️</span>
                    Температура (°C)
                  </label>
                  <div className="input-with-unit">
                    <input
                      type="number"
                      value={formData.temperature}
                      onChange={(e) => handleInputChange('temperature', parseFloat(e.target.value))}
                      className="form-input"
                      min="-10"
                      max="40"
                    />
                    <span className="input-unit">°C</span>
                  </div>
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">
                    <span className="label-icon">📏</span>
                    Площадь участка
                  </label>
                  <div className="input-with-unit">
                    <input
                      type="number"
                      value={formData.area}
                      onChange={(e) => handleInputChange('area', parseFloat(e.target.value))}
                      className="form-input"
                      min="0.1"
                      max="1000"
                      step="0.1"
                    />
                    <span className="input-unit">га</span>
                  </div>
                </div>

                <div className="form-group checkbox-container">
                  <label className="checkbox-label">
                    <div className="checkbox-wrapper">
                      <input
                        type="checkbox"
                        checked={formData.fertilizer_used}
                        onChange={(e) => handleInputChange('fertilizer_used', e.target.checked)}
                        className="form-checkbox"
                      />
                      <div className="checkbox-custom">
                        <div className="checkbox-checkmark">✓</div>
                      </div>
                    </div>
                    <div className="checkbox-text">
                      <span className="checkbox-title">Используются удобрения</span>
                      <span className="checkbox-subtitle">Повышает урожайность</span>
                    </div>
                  </label>
                </div>
              </div>

              <button 
                type="submit" 
                disabled={loading} 
                className={`predict-button ${loading ? 'loading' : ''}`}
              >
                {loading ? (
                  <>
                    <div className="button-spinner"></div>
                    Расчет...
                  </>
                ) : (
                  <>
                    <span className="button-icon">📊</span>
                    Рассчитать урожай
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {prediction && (
          <div className="result-section">
            <div className="result-card">
              <div className="result-header">
                <div className="result-icon">🎯</div>
                <div className="result-title">
                  <h3>Результаты прогноза</h3>
                  <div className="confidence-badge">
                    Точность: {((prediction.confidence || 0) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              <div className="yield-display">
                <div className="yield-value">
                  {prediction.predicted_yield}
                  <span className="yield-unit">т/га</span>
                </div>
                <div className="yield-label">Прогнозируемый урожай</div>
              </div>

              <div className="suggestions">
                <div className="suggestions-header">
                  <div className="suggestions-icon">💡</div>
                  <h4>Рекомендации для повышения урожайности</h4>
                </div>
                <div className="suggestions-list">
                  {(prediction.suggestions || [
                    "Рекомендуется консультация с агрономом",
                    "Проведите дополнительную диагностику почвы",
                    "Следите за развитием растений"
                  ]).map((suggestion: string, index: number) => (
                    <div key={index} className="suggestion-item">
                      <div className="suggestion-bullet">{index + 1}</div>
                      <span>{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default YieldPrediction;