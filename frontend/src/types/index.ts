export interface PlantAnalysisResponse {
  is_healthy: boolean;
  disease_name?: string | null;
  confidence: number;
  recommendations: string[];
}

export interface YieldPredictionRequest {
  crop_type: string;
  soil_quality: number;
  rainfall: number;
  temperature: number;
  area: number;
  fertilizer_used: boolean;
}

export interface YieldPredictionResponse {
  predicted_yield: number;
  confidence: number;
  suggestions: string[];
}

export interface AgroGPTMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

// Добавляем интерфейс для ответа чата
export interface AgroGPTResponse {
  response: string;
  timestamp?: string;
  message_id?: string;
}