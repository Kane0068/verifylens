import os
import time
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from ..utils.token_tracker import TokenTracker
from ..utils.file_handler import FileHandler

class MediaAnalyzer:
    def __init__(self, api_key: str):
        """Initialize the analyzer with API credentials."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        self.generation_config = {
            "temperature": 0.1,
            "top_p": 1.0,
            "top_k": 32,
            "max_output_tokens": 4096,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
        )
        
        self.token_tracker = TokenTracker()
        self.file_handler = FileHandler()
        
    def analyze_media(self, file_path: str, media_type: str) -> Dict[str, Any]:
        """Unified media analysis method with proper error handling."""
        mime_types = {
            "video": "video/mp4",
            "text": "text/plain",
            "audio": "audio/mpeg"
        }
        
        if media_type not in mime_types:
            return {"error": f"Unsupported media type: {media_type}"}
            
        try:
            # Validate and process file
            processed_file = self.file_handler.process_file(
                file_path, 
                mime_types[media_type]
            )
            
            if not processed_file:
                return {"error": "File processing failed"}
                
            # Choose appropriate analysis method
            if media_type == "video":
                result = self._analyze_video(processed_file)
            elif media_type == "text":
                result = self._analyze_text(processed_file)
            elif media_type == "audio":
                result = self._analyze_audio(processed_file)
                
            # Track token usage
            self.token_tracker.track_usage(result)
            
            return result
            
        except Exception as e:
            return {
                "error": f"Analysis error: {str(e)}",
                "file_path": file_path,
                "media_type": media_type
            }

    def _analyze_video(self, video_file: Any) -> Dict[str, Any]:
        """Analyze video for potential deception indicators."""
        chat = self.model.start_chat()
        analysis_prompts = {
            "Transcription": """
                Analyze this video and provide:
                1. Exact transcription of all spoken words with timestamps
                2. Speaker identification (name or description)
                3. Basic scene description
            """,
            "Behavioral Analysis": """
                Based on the video, analyze these specific behavioral indicators:
                1. Eye Movement Patterns
                2. Facial Expressions
                3. Body Language
            """,
            "Statement Analysis": """
                Analyze the truthfulness of statements in the video:
                1. Note exact statements and timestamps
                2. Analyze internal consistency
                3. Verify claims
            """
        }
        
        results = {}
        for name, prompt in analysis_prompts.items():
            if name == "Transcription":
                response = chat.send_message([prompt, video_file])
            else:
                response = chat.send_message(prompt)
                
            results[name] = self._parse_response(response)
            
        return results

    def _analyze_text(self, text_file: Any) -> Dict[str, Any]:
        """Analyze text file for incorrect statements."""
        chat = self.model.start_chat()
        analysis_prompts = {
            "Content Analysis": """
                Please analyze this text document and identify:
                1. Factually incorrect statements
                2. Grammatical errors
                3. Logical inconsistencies
            """,
            "Verification": """
                For each correction suggested:
                1. Rate confidence (0-100%)
                2. Provide reasoning
                3. Note alternative interpretations
            """
        }
        
        results = {}
        for name, prompt in analysis_prompts.items():
            if name == "Content Analysis":
                response = chat.send_message([prompt, text_file])
            else:
                response = chat.send_message(prompt)
                
            results[name] = self._parse_response(response)
            
        return results

    def _analyze_audio(self, audio_file: Any) -> Dict[str, Any]:
        """Analyze audio file for verification."""
        chat = self.model.start_chat()
        analysis_prompts = {
            "Transcription": """
                Please analyze this audio file and provide:
                1. Complete transcription with timestamps
                2. Identify incorrect statements
                3. Note unclear passages
            """,
            "Voice Analysis": """
                Analyze:
                1. Voice patterns
                2. Emotional indicators
                3. Potential deception markers
            """
        }
        
        results = {}
        for name, prompt in analysis_prompts.items():
            if name == "Transcription":
                response = chat.send_message([prompt, audio_file])
            else:
                response = chat.send_message(prompt)
                
            results[name] = self._parse_response(response)
            
        return results

    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """Parse model response into structured format."""
        if not hasattr(response, 'text'):
            return {"error": "Invalid response format"}
            
        return {
            "content": response.text,
            "metadata": {
                "token_count": getattr(response, 'token_count', 0),
                "response_time": getattr(response, 'response_time', 0)
            }
        }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get token usage statistics."""
        return self.token_tracker.get_stats()
