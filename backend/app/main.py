from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import logging
from datetime import datetime

from app.services.plant_analysis import PlantAnalysisService
from app.services.agro_gpt import AgroGPTService
from app.services.yield_prediction import YieldPredictionService
from app.utils.response_formatter import ResponseFormatter

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agro AI Platform API",
    description="Интеллектуальная платформа для агрономов с AI-функциями",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация сервисов
plant_service = PlantAnalysisService()
agro_gpt_service = AgroGPTService()
yield_service = YieldPredictionService()
response_formatter = ResponseFormatter()

# Модели запросов
class YieldPredictionRequest(BaseModel):
    crop_type: str
    soil_quality: float
    rainfall: float
    temperature: float
    area: float
    fertilizer_used: bool

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = None

class BatchAnalysisRequest(BaseModel):
    images: List[str]  # base64 encoded images
    analysis_type: str = "quick"

# Эндпоинты
@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "🌱 Agro AI Platform API",
        "version": "2.0.0", 
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "plant_analysis": "/api/analyze-plant",
            "yield_prediction": "/api/predict-yield", 
            "agro_chat": "/api/chat",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "plant_analysis": "available",
            "yield_prediction": "available", 
            "agro_gpt": "available"
        }
    }

@app.post("/api/analyze-plant")
async def analyze_plant(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(..., description="Изображение растения для анализа")
):
    """
    Анализ растения по изображению
    """
    try:
        logger.info(f"Starting plant analysis for file: {image.filename}")
        
        # Валидация файла
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="Файл должен быть изображением (JPEG, PNG, etc.)"
            )
        
        # Чтение файла
        image_data = await image.read()
        
        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="Размер файла не должен превышать 10MB")
        
        # Анализ растения
        result = await plant_service.analyze_image(image_data)
        
        # Форматирование ответа
        formatted_response = response_formatter.format_plant_analysis(result)
        
        logger.info(f"Plant analysis completed: {result['is_healthy']}")
        return formatted_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Plant analysis error: {str(e)}")
        error_response = response_formatter.format_error(
            f"Ошибка при анализе изображения: {str(e)}"
        )
        return JSONResponse(
            status_code=500,
            content=error_response
        )

@app.post("/api/predict-yield")
async def predict_yield(request: YieldPredictionRequest):
    """
    Прогноз урожайности на основе параметров
    """
    try:
        logger.info(f"Yield prediction request for: {request.crop_type}")
        
        # Валидация входных данных
        validation_errors = []
        
        if request.soil_quality < 1 or request.soil_quality > 10:
            validation_errors.append("Качество почвы должно быть от 1 до 10")
        
        if request.rainfall < 0 or request.rainfall > 500:
            validation_errors.append("Осадки должны быть от 0 до 500 мм")
            
        if request.temperature < -10 or request.temperature > 50:
            validation_errors.append("Температура должна быть от -10 до 50°C")
            
        if request.area <= 0 or request.area > 10000:
            validation_errors.append("Площадь должна быть от 0.1 до 10000 гектар")
        
        if validation_errors:
            raise HTTPException(status_code=400, detail="; ".join(validation_errors))
        
        # Прогнозирование
        prediction = yield_service.predict_yield(
            crop_type=request.crop_type,
            soil_quality=request.soil_quality,
            rainfall=request.rainfall,
            temperature=request.temperature,
            area=request.area,
            fertilizer_used=request.fertilizer_used
        )
        
        # Форматирование ответа
        formatted_response = response_formatter.format_yield_prediction(prediction)
        
        logger.info(f"Yield prediction completed: {prediction['predicted_yield']} т/га")
        return formatted_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Yield prediction error: {str(e)}")
        error_response = response_formatter.format_error(
            f"Ошибка при прогнозировании урожайности: {str(e)}"
        )
        return JSONResponse(
            status_code=500,
            content=error_response
        )

@app.post("/api/chat")
async def chat_with_agrogpt(request: ChatRequest):
    """
    Чат с AgroGPT - AI помощником по агрономии
    """
    try:
        logger.info(f"AgroGPT chat request: {request.message[:100]}...")
        
        # Валидация сообщения
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Сообщение не может быть пустым")
        
        if len(request.message) > 1000:
            raise HTTPException(status_code=400, detail="Сообщение слишком длинное")
        
        # Генерация ответа
        response = agro_gpt_service.generate_response(
            request.message, 
            request.conversation_history or []
        )
        
        # Форматирование ответа
        formatted_response = response_formatter.format_chat_response(response)
        
        logger.info("AgroGPT response generated successfully")
        return formatted_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AgroGPT chat error: {str(e)}")
        error_response = response_formatter.format_error(
            f"Ошибка при генерации ответа: {str(e)}"
        )
        return JSONResponse(
            status_code=500,
            content=error_response
        )

@app.post("/api/batch-analysis")
async def batch_analyze_plants(request: BatchAnalysisRequest):
    """
    Пакетный анализ нескольких изображений
    """
    try:
        if not request.images:
            raise HTTPException(status_code=400, detail="Список изображений пуст")
        
        if len(request.images) > 10:
            raise HTTPException(status_code=400, detail="Максимум 10 изображений за раз")
        
        results = []
        for i, image_data in enumerate(request.images):
            try:
                # Декодирование base64 и анализ
                # В реальном проекте здесь будет обработка base64
                result = await plant_service.analyze_image(image_data.encode())
                results.append({
                    "image_index": i,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "image_index": i, 
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "summary": {
                "total": len(request.images),
                "successful": len([r for r in results if r["status"] == "success"]),
                "failed": len([r for r in results if r["status"] == "error"])
            }
        }
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crops")
async def get_available_crops():
    """Получить список доступных культур для прогнозирования"""
    crops = [
        {"id": "пшеница", "name": "Пшеница", "category": "зерновые"},
        {"id": "кукуруза", "name": "Кукуруза", "category": "зерновые"},
        {"id": "рис", "name": "Рис", "category": "зерновые"},
        {"id": "картофель", "name": "Картофель", "category": "овощи"},
        {"id": "ячмень", "name": "Ячмень", "category": "зерновые"},
        {"id": "соя", "name": "Соя", "category": "бобовые"},
        {"id": "томат", "name": "Томат", "category": "овощи"},
        {"id": "огурец", "name": "Огурец", "category": "овощи"}
    ]
    
    return {
        "status": "success",
        "data": crops,
        "count": len(crops)
    }

# Глобальный обработчик ошибок
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=response_formatter.format_error("Внутренняя ошибка сервера")
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=response_formatter.format_error("Ресурс не найден")
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )