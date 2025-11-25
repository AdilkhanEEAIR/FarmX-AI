import os
import uuid
from datetime import datetime
from typing import Optional
import aiofiles

class FileManager:
    def __init__(self, upload_dir: str = "temp_uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, file_data: bytes, file_extension: str = "jpg") -> str:
        """Сохранение загруженного файла"""
        try:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{file_extension}"
            filepath = os.path.join(self.upload_dir, filename)
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(file_data)
            
            return filepath
        except Exception as e:
            raise Exception(f"File save error: {str(e)}")
    
    async def cleanup_file(self, filepath: str):
        """Удаление временного файла"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"File cleanup error: {str(e)}")
    
    def get_file_size(self, filepath: str) -> int:
        """Получение размера файла"""
        return os.path.getsize(filepath)