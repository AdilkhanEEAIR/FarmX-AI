import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import io
import cv2
from typing import Dict, List, Tuple
import random
from app.utils.image_processing import ImageProcessor

class AdvancedPlantModel(nn.Module):
    def __init__(self, num_features: int = 34, num_classes: int = 5):
        super(AdvancedPlantModel, self).__init__()
        self.classifier = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        return self.classifier(x)

class PlantDiseaseClassifier:
    def __init__(self):
        self.disease_classes = {
            0: 'healthy',
            1: 'fungal_infection',
            2: 'bacterial_infection', 
            3: 'viral_infection',
            4: 'nutrient_deficiency'
        }
        
        self.disease_descriptions = {
            'healthy': "Растение здорово и находится в хорошем состоянии.",
            'fungal_infection': "Обнаружены признаки грибковой инфекции.",
            'bacterial_infection': "Выявлены симптомы бактериального заражения.",
            'viral_infection': "Найдены признаки вирусной инфекции.",
            'nutrient_deficiency': "Обнаружен дефицит питательных веществ."
        }
        
        # Имитация обученной модели
        self.model = self._create_dummy_model()
        
    def _create_dummy_model(self):
        """Создание демо-модели"""
        return AdvancedPlantModel()
    
    def extract_advanced_features(self, image_array: np.ndarray) -> np.ndarray:
        """Извлечение расширенных признаков"""
        features = []
        
        # Базовые цветовые признаки
        hsv = cv2.cvtColor((image_array * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
        
        # Признаки из HSV пространства
        features.extend(np.mean(hsv, axis=(0, 1)))
        features.extend(np.std(hsv, axis=(0, 1)))
        
        # Текстурные признаки (энергия Лапласиана)
        gray = cv2.cvtColor((image_array * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        features.append(laplacian_var)
        
        # Признаки формы и контура
        edges = ImageProcessor.detect_edges(image_array)
        features.append(np.sum(edges > 0) / edges.size)  # плотность границ
        
        return np.array(features)
    
    def predict(self, image_array: np.ndarray) -> Tuple[str, float, Dict]:
        """Предсказание состояния растения"""
        try:
            # Извлечение признаков
            features = self.extract_advanced_features(image_array)
            
            # Демо-логика предсказания (в реальном проекте здесь будет inference модели)
            color_mean = np.mean(image_array)
            color_std = np.std(image_array)
            
            # Эвристики для разных состояний
            if color_mean > 0.6 and color_std > 0.15:
                # Яркое изображение с хорошим контрастом - вероятно здоровое
                predicted_class = 'healthy'
                confidence = random.uniform(0.7, 0.95)
            elif color_mean < 0.4:
                # Темное изображение - возможен дефицит или болезнь
                predicted_class = random.choice(['nutrient_deficiency', 'fungal_infection'])
                confidence = random.uniform(0.6, 0.85)
            else:
                # Средние значения - случайный выбор
                predicted_class = random.choice(list(self.disease_classes.values())[1:])
                confidence = random.uniform(0.5, 0.8)
            
            return predicted_class, confidence, features
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

class PlantAnalysisService:
    def __init__(self):
        self.classifier = PlantDiseaseClassifier()
        self.image_processor = ImageProcessor()
        
    async def analyze_image(self, image_data: bytes) -> Dict:
        """Основной метод анализа изображения"""
        try:
            # Препроцессинг
            processed_image = self.image_processor.preprocess_image(image_data)
            
            # Предсказание
            disease_type, confidence, features = self.classifier.predict(processed_image)
            
            # Генерация результата
            is_healthy = disease_type == 'healthy'
            disease_name = None if is_healthy else disease_type
            
            recommendations = self._generate_recommendations(
                disease_type, 
                confidence, 
                features
            )
            
            return {
                "is_healthy": is_healthy,
                "disease_name": disease_name,
                "confidence": float(confidence),
                "recommendations": recommendations,
                "analysis_details": {
                    "features_extracted": len(features),
                    "disease_type": disease_type,
                    "timestamp": self._get_timestamp()
                }
            }
            
        except Exception as e:
            raise Exception(f"Plant analysis failed: {str(e)}")
    
    def _generate_recommendations(self, disease_type: str, confidence: float, features: np.ndarray) -> List[str]:
        """Генерация персонализированных рекомендаций"""
        base_recommendations = []
        
        if disease_type == 'healthy':
            base_recommendations = [
                "✅ Растение в отличном состоянии!",
                "💧 Продолжайте текущий режим полива",
                "🌞 Обеспечьте достаточное освещение",
                "📝 Регулярно проверяйте состояние листьев"
            ]
        elif disease_type == 'fungal_infection':
            base_recommendations = [
                "🍄 Обнаружены признаки грибковой инфекции",
                "💨 Улучшите вентиляцию вокруг растения",
                "💧 Избегайте переувлажнения почвы",
                "🛡️ Примените биологический фунгицид",
                "🍂 Удалите пораженные листья"
            ]
        elif disease_type == 'bacterial_infection':
            base_recommendations = [
                "🦠 Выявлены симптомы бактериального заражения",
                "🏥 Изолируйте растение от других",
                "✂️ Удалите сильно пораженные участки",
                "🧴 Используйте медьсодержащие препараты",
                "💨 Обеспечьте хорошую циркуляцию воздуха"
            ]
        elif disease_type == 'viral_infection':
            base_recommendations = [
                "🦠 Признаки вирусной инфекции",
                "🐜 Боритесь с насекомыми-переносчиками",
                "🏥 Срочно изолируйте растение",
                "💊 Используйте стимуляторы иммунитета",
                "🌱 Рассмотрите замену растения"
            ]
        elif disease_type == 'nutrient_deficiency':
            base_recommendations = [
                "🌱 Обнаружен дефицит питательных веществ",
                "🧪 Проведите анализ почвы",
                "💩 Внесите сбалансированные удобрения",
                "💧 Отрегулируйте pH поливной воды",
                "📈 Увеличьте содержание органики в почве"
            ]
        
        # Добавляем общие рекомендации
        general_advice = [
            "Регулярно осматривайте растения",
            "Ведите дневник наблюдений",
            "Консультируйтесь с агрономом при сомнениях"
        ]
        
        return base_recommendations + general_advice
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()