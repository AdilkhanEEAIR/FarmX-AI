import axios from 'axios';
import type { PlantAnalysisResponse, YieldPredictionRequest, YieldPredictionResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Обработчик для правильного парсинга ответов
api.interceptors.response.use(
  (response) => {
    // Если ответ содержит data.data (вложенная структура), извлекаем данные
    if (response.data && response.data.data) {
      return { ...response, data: response.data.data };
    }
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    if (error.code === 'ERR_NETWORK') {
      throw new Error('Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на порту 8000.');
    }
    throw error;
  }
);

export const analyzePlant = async (imageFile: File): Promise<PlantAnalysisResponse> => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await api.post('/api/analyze-plant', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  // ФИКС: гарантируем что все поля существуют
  const result = response.data;
  return {
    is_healthy: result?.is_healthy ?? false,
    disease_name: result?.disease_name || null,
    confidence: result?.confidence ?? 0,
    recommendations: result?.recommendations || []
  };
};

export const predictYield = async (data: YieldPredictionRequest): Promise<YieldPredictionResponse> => {
  const response = await api.post('/api/predict-yield', data);
  
  // ФИКС: гарантируем что все поля существуют
  const result = response.data;
  return {
    predicted_yield: result?.predicted_yield ?? 0,
    confidence: result?.confidence ?? 0,
    suggestions: result?.suggestions || []
  };
};

export const chatWithAgroGPT = async (message: string, conversationHistory: any[] = []) => {
  const response = await api.post('/api/chat', {
    message,
    conversation_history: conversationHistory,
  });
  
  // ФИКС: проверяем структуру ответа
  if (response.data && typeof response.data === 'object') {
    return response.data;
  }
  
  return { response: "Извините, не удалось обработать ответ" };
};

export const checkBackendConnection = async (): Promise<boolean> => {
  try {
    await api.get('/');
    return true;
  } catch (error) {
    console.error('Backend connection failed:', error);
    return false;
  }
};