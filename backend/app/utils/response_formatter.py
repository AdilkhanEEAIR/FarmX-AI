from typing import Dict, Any, List
from datetime import datetime
import json

class ResponseFormatter:
    @staticmethod
    def format_plant_analysis(response: Dict[str, Any]) -> Dict[str, Any]:
        """Форматирование ответа анализа растений"""
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "is_healthy": response.get("is_healthy", False),
                "disease_name": response.get("disease_name"),
                "confidence": round(response.get("confidence", 0), 3),
                "recommendations": response.get("recommendations", []),
                "analysis_details": response.get("analysis_details", {})
            }
        }
    
    @staticmethod
    def format_yield_prediction(response: Dict[str, Any]) -> Dict[str, Any]:
        """Форматирование ответа прогноза урожайности"""
        return {
            "status": "success", 
            "timestamp": datetime.now().isoformat(),
            "data": {
                "predicted_yield": response.get("predicted_yield", 0),
                "confidence": round(response.get("confidence", 0), 3),
                "suggestions": response.get("suggestions", []),
                "analysis": response.get("analysis", {}),
                "optimal_ranges": response.get("optimal_ranges", {})
            }
        }
    
    @staticmethod
    def format_chat_response(response: str) -> Dict[str, Any]:
        """Форматирование ответа чата"""
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(), 
            "data": {
                "response": response,
                "message_id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        }
    
    @staticmethod
    def format_error(message: str, error_type: str = "processing_error") -> Dict[str, Any]:
        """Форматирование ошибки"""
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": {
                "type": error_type,
                "message": message
            }
        }