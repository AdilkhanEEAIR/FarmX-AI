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
    { value: 'пшеница', label: 'Пшеница' },
    { value: 'кукуруза', label: 'Кукуруза' },
    { value: 'рис', label: 'Рис' },
    { value: 'картофель', label: 'Картофель' },
    { value: 'ячмень', label: 'Ячмень' },
    { value: 'соя', label: 'Соя' }
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
      <h2>📈 Прогноз урожайности</h2>
      
      <div className="prediction-container">
        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-group">
            <label>Культура:</label>
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
          </div>

          <div className="form-group">
            <label>Качество почвы (1-10):</label>
            <input
              type="range"
              min="1"
              max="10"
              value={formData.soil_quality}
              onChange={(e) => handleInputChange('soil_quality', parseFloat(e.target.value))}
              className="form-range"
            />
            <span className="range-value">{formData.soil_quality}</span>
          </div>

          <div className="form-group">
            <label>Осадки (мм/месяц):</label>
            <input
              type="number"
              value={formData.rainfall}
              onChange={(e) => handleInputChange('rainfall', parseFloat(e.target.value))}
              className="form-input"
              min="0"
              max="500"
            />
          </div>

          <div className="form-group">
            <label>Температура (°C):</label>
            <input
              type="number"
              value={formData.temperature}
              onChange={(e) => handleInputChange('temperature', parseFloat(e.target.value))}
              className="form-input"
              min="-10"
              max="40"
            />
          </div>

          <div className="form-group">
            <label>Площадь (гектары):</label>
            <input
              type="number"
              value={formData.area}
              onChange={(e) => handleInputChange('area', parseFloat(e.target.value))}
              className="form-input"
              min="0.1"
              max="1000"
              step="0.1"
            />
          </div>

          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.fertilizer_used}
                onChange={(e) => handleInputChange('fertilizer_used', e.target.checked)}
                className="form-checkbox"
              />
              Используются удобрения
            </label>
          </div>

          <button type="submit" disabled={loading} className="predict-button">
            {loading ? 'Прогнозирование...' : 'Спрогнозировать урожай'}
          </button>
        </form>

        {prediction && (
          <div className="prediction-result">
            <h3>Результаты прогноза:</h3>
            <div className="yield-value">
              {prediction.predicted_yield} т/га
            </div>
            <div className="confidence">
              Уверенность прогноза: {((prediction.confidence || 0) * 100).toFixed(1)}%
            </div>
            
            <div className="suggestions">
              <h4>Рекомендации:</h4>
              <ul>
                {/* ФИКС: проверяем что suggestions существует */}
                {(prediction.suggestions || []).map((suggestion: string, index: number) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default YieldPrediction;