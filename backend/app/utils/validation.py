from typing import Dict, Any, List, Optional
import re

class InputValidator:
    @staticmethod
    def validate_plant_image(file_data: bytes, filename: str) -> List[str]:
        """Валидация изображения растения"""
        errors = []
        
        # Проверка размера файла
        if len(file_data) > 10 * 1024 * 1024:  # 10MB
            errors.append("Размер файла не должен превышать 10MB")
        
        # Проверка расширения файла
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_ext = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        if file_ext not in allowed_extensions:
            errors.append(f"Неподдерживаемый формат файла. Разрешены: {', '.join(allowed_extensions)}")
        
        return errors
    
    @staticmethod
    def validate_yield_prediction_data(data: Dict[str, Any]) -> List[str]:
        """Валидация данных для прогноза урожайности"""
        errors = []
        
        # Валидация типа культуры
        allowed_crops = ['пшеница', 'кукуруза', 'рис', 'картофель', 'ячмень', 'соя']
        if data.get('crop_type') not in allowed_crops:
            errors.append(f"Неподдерживаемая культура. Разрешены: {', '.join(allowed_crops)}")
        
        # Валидация числовых параметров
        if not (1 <= data.get('soil_quality', 0) <= 10):
            errors.append("Качество почвы должно быть от 1 до 10")
        
        if data.get('rainfall', 0) < 0 or data.get('rainfall', 0) > 1000:
            errors.append("Осадки должны быть от 0 до 1000 мм")
        
        if data.get('temperature', 0) < -50 or data.get('temperature', 0) > 60:
            errors.append("Температура должна быть от -50 до 60°C")
        
        if data.get('area', 0) <= 0 or data.get('area', 0) > 100000:
            errors.append("Площадь должна быть от 0.1 до 100000 гектар")
        
        return errors
    
    @staticmethod
    def validate_chat_message(message: str) -> List[str]:
        """Валидация сообщения чата"""
        errors = []
        
        if not message or not message.strip():
            errors.append("Сообщение не может быть пустым")
        
        if len(message) > 2000:
            errors.append("Сообщение слишком длинное (максимум 2000 символов)")
        
        # Проверка на потенциально опасный контент
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'onload=',
            r'onerror='
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                errors.append("Сообщение содержит потенциально опасный контент")
                break
        
        return errors