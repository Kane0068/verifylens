import os
from typing import Optional, Any
import google.generativeai as genai
import time

class FileHandler:
    def __init__(self):
        self.supported_mime_types = {
            "video/mp4": [".mp4"],
            "text/plain": [".txt"],
            "audio/mpeg": [".mp3"]
        }
        self.max_file_size = 100 * 1024 * 1024  # 100MB limit
        
    def process_file(self, file_path: str, mime_type: str) -> Optional[Any]:
        """Process and validate file for analysis."""
        try:
            if not self._validate_file(file_path, mime_type):
                return None
                
            return self._upload_file_with_retry(file_path, mime_type)
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return None
    
    def _validate_file(self, file_path: str, mime_type: str) -> bool:
        """Validate file exists and matches expected type."""
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return False
            
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            print(f"Error: File too large - {file_size / 1024 / 1024:.2f}MB")
            return False
            
        extension = os.path.splitext(file_path)[1].lower()
        if extension not in self.supported_mime_types.get(mime_type, []):
            print(f"Error: Invalid file type - {extension}")
            return False
            
        return True
    
    def _upload_file_with_retry(self, file_path: str, mime_type: str, 
                              max_retries: int = 3) -> Optional[Any]:
        """Upload file with retry logic."""
        for attempt in range(max_retries):
            try:
                print(f"Upload attempt {attempt + 1}/{max_retries}")
                file = genai.upload_file(file_path, mime_type=mime_type)
                
                # Brief wait to ensure file is processed
                time.sleep(2)
                
                return file
                
            except Exception as e:
                print(f"Upload attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print("Max retries reached. Upload failed.")
                    return None
