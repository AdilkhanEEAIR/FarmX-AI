import React, { useState } from 'react';
import { analyzePlant } from '../../services/api';
import './PlantAnalysis.css'

const PlantAnalysis: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAnalysisResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    try {
      const result = await analyzePlant(selectedFile);
      setAnalysisResult(result);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Ошибка при анализе изображения');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="plant-analysis">
      <div className="analysis-header">
        <div className="header-icon">🔍</div>
        <h2>Анализ растений</h2>
        <p>Загрузите фото растения для диагностики заболеваний</p>
      </div>
      
      <div className="upload-section">
        <div className="upload-card">
          <div className="upload-area">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="file-input"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="upload-label">
              <div className="upload-icon">📁</div>
              <div className="upload-text">
                <span className="upload-title">Выберите изображение</span>
                <span className="upload-subtitle">PNG, JPG, JPEG до 10MB</span>
              </div>
            </label>
          </div>
          
          {previewUrl && (
            <div className="preview-container">
              <div className="preview-header">
                <span>Предпросмотр</span>
                <button 
                  onClick={() => {
                    setSelectedFile(null);
                    setPreviewUrl('');
                  }}
                  className="clear-preview"
                >
                  ✕
                </button>
              </div>
              <img src={previewUrl} alt="Preview" className="preview-image" />
            </div>
          )}
          
          <button 
            onClick={handleAnalyze} 
            disabled={!selectedFile || loading}
            className={`analyze-button ${loading ? 'loading' : ''}`}
          >
            {loading ? (
              <>
                <div className="button-spinner"></div>
                Идет анализ...
              </>
            ) : (
              <>
                <span></span>
                Проанализировать
              </>
            )}
          </button>
        </div>
      </div>

      {analysisResult && (
        <div className={`result-section ${analysisResult.is_healthy ? 'healthy' : 'diseased'}`}>
          <div className="result-header">
            <div className={`status-indicator ${analysisResult.is_healthy ? 'healthy' : 'diseased'}`}>
              {analysisResult.is_healthy ? '🌿' : '⚠️'}
            </div>
            <div className="result-title">
              <h3>Результаты анализа</h3>
              <div className="confidence-badge">
                Уверенность: {((analysisResult.confidence || 0) * 100).toFixed(1)}%
              </div>
            </div>
          </div>
          
          <div className="result-content">
            <div className="status-card">
              <span className="status-label">Состояние растения:</span>
              <span className={`status-value ${analysisResult.is_healthy ? 'healthy' : 'diseased'}`}>
                {analysisResult.is_healthy ? 'Здорово' : 'Требует внимания'}
              </span>
            </div>
            
            {analysisResult.disease_name && (
              <div className="disease-card">
                <span className="disease-label">Диагностировано:</span>
                <span className="disease-name">{analysisResult.disease_name}</span>
              </div>
            )}
            
            <div className="recommendations">
              <div className="recommendations-header">
                <div className="recommendations-icon">💡</div>
                <h4>Рекомендации по уходу</h4>
              </div>
              <div className="recommendations-list">
                {(analysisResult.recommendations || [
                  "Рекомендуется консультация с агрономом",
                  "Проведите дополнительную диагностику",
                  "Следите за развитием растения"
                ]).map((rec: string, index: number) => (
                  <div key={index} className="recommendation-item">
                    <div className="recommendation-bullet"></div>
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlantAnalysis;