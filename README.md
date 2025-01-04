
# VerifyLens

AI-powered media verification platform that detects deception in video, audio, and text content.

## Features

- **Video Analysis**: Analyze facial expressions, body language, and speech patterns
- **Text Verification**: Detect factual inaccuracies and logical inconsistencies
- **Audio Analysis**: Examine voice patterns and transcribe content
- **Real-time Processing**: Quick and efficient analysis
- **Comprehensive Reports**: Detailed analysis with confidence scores
- **API Integration**: Easy integration with existing systems

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
GEMINI_API_KEY=your_api_key_here
```

3. Run the API:
```bash
uvicorn verifylens.api.routes:app --reload
```

4. Visit API documentation:
```
http://localhost:8000/docs
```

## API Usage

### Analyze Media

```python
import requests

# Analyze video
files = {'file': open('video.mp4', 'rb')}
response = requests.post('http://localhost:8000/analyze/video', files=files)

# Analyze text
files = {'file': open('document.txt', 'rb')}
response = requests.post('http://localhost:8000/analyze/text', files=files)

# Analyze audio
files = {'file': open('recording.mp3', 'rb')}
response = requests.post('http://localhost:8000/analyze/audio', files=files)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- Website: [verifylens.com](https://verifylens.com)
- Email: support@verifylens.com
- Twitter: [@VerifyLens](https://twitter.com/VerifyLens)
