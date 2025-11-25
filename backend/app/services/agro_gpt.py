import random
import re
from typing import List, Dict, Any
from datetime import datetime
import json

class AgroKnowledgeBase:
    def __init__(self):
        self.crop_data = {
            'пшеница': {
                'watering': "Полив 2-3 раза в неделю в зависимости от погоды",
                'fertilizer': "Азотные удобрения весной, фосфорно-калийные осенью",
                'pests': "Основные вредители: тля, клоп-черепашка, пилильщик"
            },
            'томат': {
                'watering': "Регулярный полив под корень, избегая попадания на листья",
                'fertilizer': "Калийные удобрения для улучшения плодоношения",
                'pests': "Борьба с фитофторой, белокрылкой, тлей"
            },
            'картофель': {
                'watering': "Обильный полив во время клубнеобразования",
                'fertilizer': "Калийные удобрения, зола",
                'pests': "Колорадский жук, проволочник, фитофтора"
            },
            'огурец': {
                'watering': "Частый полив теплой водой",
                'fertilizer': "Органические удобрения, азот в начале роста",
                'pests': "Паутинный клещ, тля, мучнистая роса"
            }
        }
        
        self.seasonal_advice = {
            'spring': "Весна - время посева и подготовки почвы",
            'summer': "Лето - уход за растениями и борьба с вредителями", 
            'autumn': "Осень - уборка урожая и подготовка к зиме",
            'winter': "Зима - планирование и подготовка семян"
        }

class AgroGPTService:
    def __init__(self):
        self.knowledge_base = AgroKnowledgeBase()
        self.conversation_context = {}
        
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Генерация интеллектуального ответа"""
        try:
            # Анализ сообщения пользователя
            user_intent = self._analyze_intent(user_message)
            user_entities = self._extract_entities(user_message)
            
            # Обновление контекста
            self._update_context(user_intent, user_entities, conversation_history)
            
            # Генерация ответа на основе интента
            if user_intent == 'plant_care':
                response = self._generate_plant_care_response(user_entities)
            elif user_intent == 'disease_help':
                response = self._generate_disease_response(user_entities)
            elif user_intent == 'soil_advice':
                response = self._generate_soil_response(user_entities)
            elif user_intent == 'watering':
                response = self._generate_watering_response(user_entities)
            elif user_intent == 'fertilizer':
                response = self._generate_fertilizer_response(user_entities)
            else:
                response = self._generate_general_advice(user_message)
            
            # Добавление персонализированных рекомендаций
            response = self._add_personal_touch(response, user_entities)
            
            return response
            
        except Exception as e:
            return f"Как агрономический помощник, я рекомендую обратиться к специалисту для точной консультации. Ошибка: {str(e)}"
    
    def _analyze_intent(self, message: str) -> str:
        """Анализ намерения пользователя"""
        message_lower = message.lower()
        
        intent_patterns = {
            'plant_care': ['уход', 'ухаживать', 'заботиться', 'ухаживаю'],
            'disease_help': ['болезн', 'заболел', 'пожелтел', 'сохнет', 'вредител'],
            'soil_advice': ['почв', 'грунт', 'земл', 'ph'],
            'watering': ['полив', 'поливать', 'вода', 'орошен'],
            'fertilizer': ['удобрен', 'подкормк', 'питание', 'npk']
        }
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return intent
                
        return 'general'
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Извлечение сущностей из сообщения"""
        entities = {
            'crops': [],
            'symptoms': [],
            'season': None
        }
        
        message_lower = message.lower()
        
        # Извлечение культур
        crops = ['пшениц', 'томат', 'картофел', 'огурец', 'морков', 'капуст', 'яблон', 'груш']
        for crop in crops:
            if crop in message_lower:
                entities['crops'].append(crop)
        
        # Извлечение симптомов
        symptoms = ['желте', 'сохнет', 'пятн', 'гнил', 'увяда', 'насеком']
        for symptom in symptoms:
            if symptom in message_lower:
                entities['symptoms'].append(symptom)
        
        # Определение сезона
        seasons = {
            'весн': 'spring',
            'лет': 'summer', 
            'осен': 'autumn',
            'зим': 'winter'
        }
        for season_ru, season_en in seasons.items():
            if season_ru in message_lower:
                entities['season'] = season_en
                break
        
        return entities
    
    def _update_context(self, intent: str, entities: Dict, history: List[Dict]):
        """Обновление контекста разговора"""
        if entities['crops']:
            self.conversation_context['current_crop'] = entities['crops'][0]
        if entities['season']:
            self.conversation_context['current_season'] = entities['season']
        if intent:
            self.conversation_context['last_intent'] = intent
    
    def _generate_plant_care_response(self, entities: Dict) -> str:
        """Генерация ответа по уходу за растениями"""
        crop = entities['crops'][0] if entities['crops'] else 'растение'
        
        responses = [
            f"Для ухода за {crop} рекомендую: регулярный полив, своевременную подкормку и защиту от вредителей.",
            f"Уход за {crop} включает: контроль влажности почвы, обеспечение достаточного освещения и профилактику заболеваний.",
            f"При уходе за {crop} важно: соблюдать севооборот, мульчировать почву и проводить регулярный осмотр."
        ]
        
        return random.choice(responses)
    
    def _generate_disease_response(self, entities: Dict) -> str:
        """Генерация ответа по болезням растений"""
        symptoms = entities['symptoms'] if entities['symptoms'] else ['проблемы']
        
        advice_map = {
            'желте': "Пожелтение листьев может указывать на недостаток азота или проблемы с поливом.",
            'сохнет': "Высыхание листьев часто связано с недостатком влаги или солнечными ожогами.",
            'пятн': "Пятна на листьях могут быть признаком грибковых заболеваний.",
            'гнил': "Гниль обычно вызвана переувлажнением или бактериальными инфекциями."
        }
        
        specific_advice = []
        for symptom in symptoms:
            if symptom in advice_map:
                specific_advice.append(advice_map[symptom])
        
        if specific_advice:
            base_response = " ".join(specific_advice)
        else:
            base_response = "При признаках заболевания растений рекомендую: изолировать пораженное растение, улучшить вентиляцию и обратиться к специалисту."
        
        return base_response + " " + self._get_general_plant_health_tips()
    
    def _generate_soil_response(self, entities: Dict) -> str:
        """Генерация ответа по почве"""
        tips = [
            "Проведите анализ почвы для определения pH и содержания питательных веществ.",
            "Добавление компоста улучшает структуру почвы и ее плодородие.",
            "Мульчирование помогает сохранить влагу и контролировать сорняки.",
            "Севооборот предотвращает истощение почвы и накопление болезней."
        ]
        
        return random.choice(tips)
    
    def _generate_watering_response(self, entities: Dict) -> str:
        """Генерация ответа по поливу"""
        crop = entities['crops'][0] if entities['crops'] else 'растения'
        
        responses = [
            f"Полив {crop} должен быть регулярным, но не чрезмерным. Проверяйте влажность почвы перед поливом.",
            f"Для {crop} рекомендую полив утром, чтобы листья успели высохнуть до вечера.",
            f"Поливайте {crop} под корень, избегая попадания воды на листья для профилактики грибковых заболеваний."
        ]
        
        return random.choice(responses)
    
    def _generate_fertilizer_response(self, entities: Dict) -> str:
        """Генерация ответа по удобрениям"""
        crop = entities['crops'][0] if entities['crops'] else 'растений'
        
        responses = [
            f"Для {crop} используйте сбалансированные удобрения с учетом фазы роста.",
            f"Органические удобрения для {crop} улучшают структуру почвы и обеспечивают медленное высвобождение питательных веществ.",
            f"При подкормке {crop} учитывайте сезон: весной - азотные, летом - комплексные, осенью - фосфорно-калийные."
        ]
        
        return random.choice(responses)
    
    def _generate_general_advice(self, message: str) -> str:
        """Генерация общего совета"""
        general_responses = [
            "Как агрономический помощник, я рекомендую: соблюдать севооборот, использовать адаптированные сорта и регулярно мониторить состояние растений.",
            "Для успешного земледелия важно: правильное планирование участка, своевременный уход и профилактика заболеваний.",
            "Советую вести агрономический дневник, где отмечать все работы и наблюдения за растениями."
        ]
        
        return random.choice(general_responses)
    
    def _add_personal_touch(self, response: str, entities: Dict) -> str:
        """Добавление персонализированных рекомендаций"""
        personal_tips = [
            "Также рекомендую учитывать климатические особенности вашего региона.",
            "Не забывайте о важности регулярного осмотра растений.",
            "Учитывайте особенности вашей почвы при планировании ухода.",
            "Рекомендую консультироваться с местными агрономами для точных рекомендаций."
        ]
        
        return response + " " + random.choice(personal_tips)
    
    def _get_general_plant_health_tips(self) -> str:
        """Общие советы по здоровью растений"""
        tips = [
            "Регулярно осматривайте растения на наличие признаков болезней и вредителей.",
            "Соблюдайте оптимальные условия освещения и полива для каждого вида растений.",
            "Используйте профилактические меры для предотвращения заболеваний."
        ]
        
        return random.choice(tips)