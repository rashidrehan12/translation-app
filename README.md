# 🤖 RoboTranslate - AI-Powered Translation App

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=groq&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A beautiful, futuristic translation application powered by AI that translates text between multiple languages with text-to-speech capabilities.

## ✨ Features

- 🌍 **Multi-language Support**: Translate between 15+ languages
- 🤖 **AI-Powered**: Utilizes Groq's lightning-fast LLMs (Llama 3, Gemma)
- 🔊 **Text-to-Speech**: Listen to translations with natural sounding voice
- 🎨 **Beautiful UI**: Friendly robot-themed interface with chat bubbles
- 📱 **Responsive**: Works perfectly on desktop and mobile devices
- ⚡ **Real-time**: Fast translation with status indicators

## 🚀 Live Demo

- **Frontend**: [Streamlit App](https://robotranslate.streamlit.app/)
- **Backend API**: [Render API](https://translation-backend-rzn5.onrender.com)

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web application framework
- **gTTS** - Google Text-to-Speech for audio synthesis
- **Requests** - API communication

### Backend
- **FastAPI** - REST API framework
- **LangChain** - AI integration framework
- **Groq API** - LLM inference
- **Uvicorn** - ASGI server

### Deployment
- **Streamlit Community Cloud** - Frontend hosting
- **Render** - Backend hosting
- **GitHub** - Version control

## 📦 Installation

### Prerequisites
- Python 3.8+
- [Groq API account](https://console.groq.com/)
- GitHub account

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/translation-app.git
   cd translation-app
   ```

2. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend**
   ```bash
   cd ../frontend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the backend directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application locally**
   ```bash
   # Terminal 1 - Start backend
   cd backend
   python server.py
   
   # Terminal 2 - Start frontend
   cd frontend
   streamlit run app.py
   ```

## 🌐 Deployment

### Backend Deployment on Render

1. **Connect your GitHub repository** to Render
2. **Set environment variables** in Render dashboard:
   - `GROQ_API_KEY`: Your Groq API key
   - `PORT`: 8000
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn server:app --host=0.0.0.0 --port=$PORT`

### Frontend Deployment on Streamlit Cloud

1. **Ensure** `app.py` is in the root or specified directory
2. **Push** changes to GitHub repository
3. **Deploy** on [share.streamlit.io](https://share.streamlit.io/)
4. **Set environment variable**:
   - `BACKEND_URL`: Your Render backend URL (e.g., `https://translation-backend-rzn5.onrender.com`)

## 📁 Project Structure

```
translation-app/
├── backend/
│   ├── server.py          # FastAPI backend server
│   ├── requirements.txt   # Python dependencies
│   └── runtime.txt        # Python version specification
├── frontend/
│   ├── app.py            # Streamlit frontend application
│   └── requirements.txt  # Frontend dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── Procfile             # Render deployment configuration
├── render.yaml          # Render configuration (optional)
└── README.md
```

## 🎮 Usage

1. **Open the application** in your web browser
2. **Type your text** in the input box
3. **Select target language** from the dropdown menu
4. **Choose AI model** (Llama 3 8B, Llama 3 70B, or Gemma)
5. **Click "Activate Translation"** button
6. **View the translation** in the robot speech bubble
7. **Listen to translation** using the audio player

## 🌍 Supported Languages

| Language | Code | Emoji |
|----------|------|-------|
| English | en | 🇺🇸 |
| French | fr | 🇫🇷 |
| Spanish | es | 🇪🇸 |
| German | de | 🇩🇪 |
| Italian | it | 🇮🇹 |
| Portuguese | pt | 🇵🇹 |
| Chinese | zh | 🇨🇳 |
| Japanese | ja | 🇯🇵 |
| Korean | ko | 🇰🇷 |
| Hindi | hi | 🇮🇳 |
| Arabic | ar | 🇸🇦 |
| Russian | ru | 🇷🇺 |
| Dutch | nl | 🇳🇱 |
| Turkish | tr | 🇹🇷 |
| Greek | el | 🇬🇷 |

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `GET` | `/models` | List available AI models |
| `GET` | `/languages` | List supported languages |
| `GET` | `/check_groq` | Check Groq API connection status |
| `POST` | `/translate` | Translate text to target language |

### Example API Request

```bash
curl -X POST "https://translation-backend-rzn5.onrender.com/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "language": "Spanish",
    "model": "llama3-8b-8192"
  }'
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

Please follow PEP 8 guidelines for Python code and ensure proper documentation.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the AI inference API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance API framework
- [Google Text-to-Speech](https://pypi.org/project/gTTS/) for voice synthesis capabilities

## 📞 Support

If you have any questions or issues:

1. **Check existing issues** on [GitHub Issues](https://github.com/rashidrehan12/translation-app/issues)
2. **Create a new issue** with detailed description
3. **Email**: rashidrehan122000@gmail.com

## 🚀 Future Enhancements

- [ ] User authentication and translation history
- [ ] Batch translation support for multiple texts
- [ ] Additional language support (50+ languages)
- [ ] Translation memory and favorite translations
- [ ] File translation (PDF, DOCX, TXT)
- [ ] Speech-to-text input capability
- [ ] Mobile app version (iOS/Android)
- [ ] Translation quality assessment
- [ ] Custom vocabulary and terminology
- [ ] Real-time collaborative translation

## 📊 Performance Notes

- **First request**: May take 10-30 seconds (Render free tier cold start)
- **Subsequent requests**: Typically 2-5 seconds
- **Audio generation**: Additional 1-2 seconds for text-to-speech

## 🔒 Privacy & Security

- All translations are processed through secure APIs
- No data is stored permanently on the server
- Groq API calls are encrypted end-to-end
- Environment variables are used for sensitive information

---

⭐ **If you find this project helpful, please give it a star on GitHub!**

---

**Happy Translating!** 🌍🤖✨

