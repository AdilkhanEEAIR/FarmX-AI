#!/usr/bin/env python3
import os
import subprocess
import sys

def setup_backend():
    """Скрипт настройки бэкенда"""
    print("🚀 Настройка Agro AI Backend...")
    
    # Создание директорий
    directories = [
        "models",
        "logs", 
        "temp_uploads"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Создана директория: {directory}")
    
    # Установка зависимостей
    print("📦 Установка зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости установлены успешно!")
    except subprocess.CalledProcessError:
        print("❌ Ошибка установки зависимостей")
        return False
    
    # Проверка установки
    print("🔍 Проверка установки...")
    try:
        import fastapi
        import torch
        import sklearn
        print("✅ Все библиотеки загружены успешно!")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    print("\n🎉 Настройка завершена! Запустите бэкенд:")
    print("   python run.py")
    print("   или")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    return True

if __name__ == "__main__":
    setup_backend()