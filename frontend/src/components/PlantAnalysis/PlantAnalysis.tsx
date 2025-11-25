import React, { useState } from 'react';
import { analyzePlant } from '../../services/api';

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
      <h2>🔍 Анализ растений</h2>
      
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="file-input"
        />
        
        {previewUrl && (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="preview-image" />
          </div>
        )}
        
        <button 
          onClick={handleAnalyze} 
          disabled={!selectedFile || loading}
          className="analyze-button"
        >
          {loading ? 'Анализ...' : 'Проанализировать'}
        </button>
      </div>

      {analysisResult && (
        <div className={`result-section ${analysisResult.is_healthy ? 'healthy' : 'diseased'}`}>
          <h3>Результаты анализа:</h3>
          <p>Состояние: <strong>{analysisResult.is_healthy ? 'Здоров' : 'Болен'}</strong></p>
          <p>Уверенность: {((analysisResult.confidence || 0) * 100).toFixed(1)}%</p>
          
          {analysisResult.disease_name && (
            <p>Заболевание: {analysisResult.disease_name}</p>
          )}
          
          <div className="recommendations">
            <h4>Рекомендации:</h4>
            <ul>
              {/* ФИКС: проверяем что recommendations существует */}
              {(analysisResult.recommendations || [
                "Рекомендуется консультация с агрономом",
                "Проведите дополнительную диагностику",
                "Следите за развитием растения"
              ]).map((rec: string, index: number) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlantAnalysis;