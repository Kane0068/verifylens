import pytest
import os
from verifylens.core.analyzer import MediaAnalyzer

def test_analyzer_initialization():
    """Test analyzer initialization with API key."""
    analyzer = MediaAnalyzer("test_api_key")
    assert analyzer is not None
    assert analyzer.api_key == "test_api_key"

def test_invalid_media_type():
    """Test handling of invalid media type."""
    analyzer = MediaAnalyzer("test_api_key")
    result = analyzer.analyze_media("test.txt", "invalid_type")
    assert "error" in result
    assert "Unsupported media type" in result["error"]

def test_missing_file():
    """Test handling of missing file."""
    analyzer = MediaAnalyzer("test_api_key")
    result = analyzer.analyze_media("nonexistent.txt", "text")
    assert "error" in result

def test_token_tracking():
    """Test token usage tracking."""
    analyzer = MediaAnalyzer("test_api_key")
    stats = analyzer.get_usage_stats()
    assert "summary" in stats
    assert "total_prompts" in stats["summary"]
