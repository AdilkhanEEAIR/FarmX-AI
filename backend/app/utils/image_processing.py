import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_data: bytes, target_size: tuple = (224, 224)) -> np.ndarray:
        """
        Препроцессинг изображения для ML модели
        """
        try:
            # Чтение изображения
            image = Image.open(io.BytesIO(image_data))
            
            # Конвертация в RGB если нужно
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Изменение размера
            image = image.resize(target_size)
            
            # Конвертация в numpy array
            image_array = np.array(image)
            
            # Нормализация
            image_array = image_array.astype(np.float32) / 255.0
            
            return image_array
            
        except Exception as e:
            raise Exception(f"Image processing error: {str(e)}")
    
    @staticmethod
    def extract_features(image_array: np.ndarray) -> np.ndarray:
        """
        Извлечение признаков из изображения
        """
        # Простые признаки для демонстрации
        features = []
        
        # Средние значения по каналам
        mean_rgb = np.mean(image_array, axis=(0, 1))
        features.extend(mean_rgb)
        
        # Стандартные отклонения
        std_rgb = np.std(image_array, axis=(0, 1))
        features.extend(std_rgb)
        
        # Гистограмма (упрощенная)
        hist_r = np.histogram(image_array[:,:,0], bins=8, range=(0, 1))[0]
        hist_g = np.histogram(image_array[:,:,1], bins=8, range=(0, 1))[0]
        hist_b = np.histogram(image_array[:,:,2], bins=8, range=(0, 1))[0]
        
        features.extend(hist_r / np.sum(hist_r))
        features.extend(hist_g / np.sum(hist_g))
        features.extend(hist_b / np.sum(hist_b))
        
        return np.array(features)
    
    @staticmethod
    def detect_edges(image_array: np.ndarray) -> np.ndarray:
        """
        Детекция границ для анализа текстуры листьев
        """
        gray = cv2.cvtColor((image_array * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges