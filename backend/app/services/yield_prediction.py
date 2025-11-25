import numpy as np
import pandas as pd
from typing import Dict, List, Any
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class AdvancedYieldModel:
    def __init__(self):
        self.crop_models = {}
        self.label_encoder = LabelEncoder()
        self.feature_importance = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Инициализация моделей для разных культур"""
        crops = ['пшеница', 'кукуруза', 'рис', 'картофель', 'ячмень', 'соя']
        
        for crop in crops:
            # Создание демо-модели Random Forest
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Обучение на синтетических данных
            X_train, y_train = self._generate_training_data(crop)
            model.fit(X_train, y_train)
            
            self.crop_models[crop] = model
            self.feature_importance[crop] = dict(zip(
                ['soil_quality', 'rainfall', 'temperature', 'area', 'fertilizer'],
                model.feature_importances_
            ))
    
    def _generate_training_data(self, crop: str, n_samples: int = 1000):
        """Генерация синтетических данных для обучения"""
        np.random.seed(42)
        
        # Базовые параметры в зависимости от культуры
        crop_params = {
            'пшеница': {'base_yield': 3.0, 'soil_impact': 0.8, 'rain_impact': 0.6},
            'кукуруза': {'base_yield': 4.0, 'soil_impact': 0.9, 'rain_impact': 0.7},
            'рис': {'base_yield': 5.0, 'soil_impact': 0.7, 'rain_impact': 0.9},
            'картофель': {'base_yield': 3.5, 'soil_impact': 0.85, 'rain_impact': 0.65},
            'ячмень': {'base_yield': 2.8, 'soil_impact': 0.75, 'rain_impact': 0.55},
            'соя': {'base_yield': 2.5, 'soil_impact': 0.8, 'rain_impact': 0.6}
        }
        
        params = crop_params.get(crop, crop_params['пшеница'])
        
        # Генерация признаков
        soil_quality = np.random.uniform(3, 10, n_samples)
        rainfall = np.random.uniform(30, 200, n_samples)
        temperature = np.random.uniform(10, 30, n_samples)
        area = np.random.uniform(0.5, 5, n_samples)
        fertilizer = np.random.choice([0, 1], n_samples)
        
        X = np.column_stack([soil_quality, rainfall, temperature, area, fertilizer])
        
        # Генерация целевой переменной
        base = params['base_yield']
        soil_effect = soil_quality * params['soil_impact'] * 0.3
        rain_effect = rainfall * params['rain_impact'] * 0.02
        temp_effect = np.where(
            (temperature >= 15) & (temperature <= 25),
            temperature * 0.1,
            temperature * 0.05
        )
        fertilizer_effect = fertilizer * 0.5
        
        y = base + soil_effect + rain_effect + temp_effect + fertilizer_effect
        
        # Добавление шума
        y += np.random.normal(0, 0.5, n_samples)
        y = np.maximum(0, y)
        
        return X, y
    
    def predict(self, crop_type: str, features: List[float]) -> float:
        """Предсказание урожайности"""
        if crop_type not in self.crop_models:
            crop_type = 'пшеница'  # fallback
        
        model = self.crop_models[crop_type]
        features_array = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_array)[0]
        
        # Добавление реалистичного шума
        prediction += random.uniform(-0.3, 0.3)
        prediction = max(0, prediction)
        
        return round(prediction, 2)

class YieldPredictionService:
    def __init__(self):
        self.model = AdvancedYieldModel()
        self.optimal_ranges = {
            'пшеница': {'temp': (15, 25), 'rain': (50, 150), 'soil': (6, 9)},
            'кукуруза': {'temp': (18, 30), 'rain': (60, 180), 'soil': (6, 8)},
            'рис': {'temp': (20, 35), 'rain': (100, 250), 'soil': (5, 7)},
            'картофель': {'temp': (15, 25), 'rain': (50, 120), 'soil': (5, 7)},
            'ячмень': {'temp': (12, 22), 'rain': (40, 120), 'soil': (6, 8)},
            'соя': {'temp': (20, 30), 'rain': (50, 150), 'soil': (6, 7)}
        }
    
    def predict_yield(self, crop_type: str, soil_quality: float, rainfall: float, 
                     temperature: float, area: float, fertilizer_used: bool) -> Dict[str, Any]:
        """Основной метод предсказания урожайности"""
        try:
            # Подготовка признаков
            features = [
                soil_quality,
                rainfall, 
                temperature,
                area,
                1 if fertilizer_used else 0
            ]
            
            # Предсказание
            predicted_yield = self.model.predict(crop_type, features)
            
            # Расчет уверенности
            confidence = self._calculate_confidence(
                crop_type, soil_quality, rainfall, temperature
            )
            
            # Генерация рекомендаций
            suggestions = self._generate_suggestions(
                crop_type, soil_quality, rainfall, temperature, 
                predicted_yield, fertilizer_used
            )
            
            # Анализ факторов влияния
            factor_analysis = self._analyze_factors(crop_type, features)
            
            return {
                "predicted_yield": predicted_yield,
                "confidence": round(confidence, 3),
                "suggestions": suggestions,
                "analysis": factor_analysis,
                "optimal_ranges": self.optimal_ranges.get(crop_type, {})
            }
            
        except Exception as e:
            raise Exception(f"Yield prediction failed: {str(e)}")
    
    def _calculate_confidence(self, crop_type: str, soil: float, rain: float, temp: float) -> float:
        """Расчет уверенности предсказания"""
        confidence = 0.7  # базовая уверенность
        
        # Проверка оптимальных диапазонов
        optimal = self.optimal_ranges.get(crop_type, {})
        
        if optimal:
            # Проверка температуры
            temp_min, temp_max = optimal.get('temp', (10, 30))
            if temp_min <= temp <= temp_max:
                confidence += 0.1
            else:
                confidence -= 0.15
            
            # Проверка осадков
            rain_min, rain_max = optimal.get('rain', (50, 150))
            if rain_min <= rain <= rain_max:
                confidence += 0.1
            else:
                confidence -= 0.1
            
            # Проверка почвы
            soil_min, soil_max = optimal.get('soil', (5, 8))
            if soil_min <= soil <= soil_max:
                confidence += 0.1
            else:
                confidence -= 0.1
        
        return max(0.3, min(0.95, confidence))
    
    def _generate_suggestions(self, crop_type: str, soil: float, rain: float, 
                            temp: float, yield_value: float, fertilizer: bool) -> List[str]:
        """Генерация персонализированных рекомендаций"""
        suggestions = []
        optimal = self.optimal_ranges.get(crop_type, {})
        
        # Рекомендации по температуре
        if optimal.get('temp'):
            temp_min, temp_max = optimal['temp']
            if temp < temp_min:
                suggestions.append(f"Температура ниже оптимальной для {crop_type}. Рассмотрите использование укрывных материалов.")
            elif temp > temp_max:
                suggestions.append(f"Температура выше оптимальной для {crop_type}. Обеспечьте затенение и дополнительный полив.")
        
        # Рекомендации по осадкам
        if optimal.get('rain'):
            rain_min, rain_max = optimal['rain']
            if rain < rain_min:
                suggestions.append(f"Осадков недостаточно для {crop_type}. Организуйте дополнительный полив.")
            elif rain > rain_max:
                suggestions.append(f"Осадков слишком много для {crop_type}. Убедитесь в хорошем дренаже почвы.")
        
        # Рекомендации по почве
        if soil < 6:
            suggestions.append("Качество почвы низкое. Добавьте органические удобрения и компост.")
        elif soil > 8:
            suggestions.append("Почва слишком щелочная. Рассмотрите внесение кислых удобрений.")
        
        # Рекомендации по удобрениям
        if not fertilizer:
            suggestions.append("Использование удобрений может увеличить урожайность на 20-30%.")
        else:
            suggestions.append("Продолжайте использовать удобрения, но следите за балансом питательных веществ.")
        
        # Общие рекомендации
        general_tips = [
            f"Регулярно мониторьте состояние {crop_type} в течение сезона",
            "Ведите учет погодных условий и применяемых агротехнических мероприятий",
            "Консультируйтесь с местными агрономами для точных рекомендаций"
        ]
        
        suggestions.extend(general_tips)
        
        return suggestions
    
    def _analyze_factors(self, crop_type: str, features: List[float]) -> Dict[str, Any]:
        """Анализ влияния факторов на урожайность"""
        soil, rain, temp, area, fertilizer = features
        
        factor_impact = {
            'soil_quality': f"Качество почвы ({soil}/10) - {'оптимальное' if 6 <= soil <= 8 else 'требует улучшения'}",
            'rainfall': f"Осадки ({rain} мм) - {'достаточно' if 50 <= rain <= 150 else 'недостаточно/избыточно'}",
            'temperature': f"Температура ({temp}°C) - {'комфортная' if 15 <= temp <= 25 else 'экстремальная'}",
            'fertilizer': f"Удобрения - {'используются' if fertilizer else 'не используются'}"
        }
        
        # Определение лимитирующего фактора
        limiting_factors = []
        if soil < 5:
            limiting_factors.append("низкое качество почвы")
        if rain < 40:
            limiting_factors.append("недостаток осадков")
        if temp < 10 or temp > 35:
            limiting_factors.append("неоптимальная температура")
        if not fertilizer:
            limiting_factors.append("отсутствие удобрений")
        
        return {
            'factor_impact': factor_impact,
            'limiting_factors': limiting_factors,
            'main_improvement': limiting_factors[0] if limiting_factors else "все факторы в норме"
        }