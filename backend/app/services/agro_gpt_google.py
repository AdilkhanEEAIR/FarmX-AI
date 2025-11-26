import requests
import random
from typing import List, Dict, Any

class GoogleAIPALM:
    def __init__(self):
        self.api_key = "your_google_ai_key"  # Получи на makersuite.google.com
        
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        try:
            prompt = f"""Ты AgroGPT - дружелюбный помощник по сельскому хозяйству. Отвечай на ВСЕ вопросы вежливо и интересно.

Вопрос: {user_message}

Ответ:"""
            
            data = {
                "prompt": {
                    "text": prompt
                },
                "temperature": 0.8,
                "candidate_count": 1,
                "max_output_tokens": 200
            }
            
            url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={self.api_key}"
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['output'].strip()
            
            return self._get_fallback(user_message)
            
        except:
            return self._get_fallback(user_message)
    
    def _get_fallback(self, user_message: str) -> str:
        return "Привет! Я AgroGPT - твой помощник по сельскому хозяйству! 🌱 Чем могу помочь?"

class AgroGPTService:
    def __init__(self):
        self.llm = GoogleAIPALM()
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        return self.llm.generate_response(user_message, conversation_history)