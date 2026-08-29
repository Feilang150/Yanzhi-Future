# 应用配置
APP_NAME = "Yanzhi AI Service"
APP_VERSION = "1.0.0"
DEBUG = True

# 服务器配置
HOST = "0.0.0.0"
PORT = 5000
WORKERS = 4

# 数据库配置
MONGODB_URL = "mongodb://localhost:27017/"
MONGODB_DATABASE = "yanzhi_future"

REDIS_URL = "redis://localhost:6379/0"

# 模型配置
MODEL_DIR = "./models"
CACHE_DIR = "./cache"

# OpenAI配置（如果使用OpenAI API）
OPENAI_API_KEY = "your-openai-api-key"
OPENAI_MODEL = "gpt-4"

# 语音识别配置
WHISPER_MODEL = "large-v3"  # tiny, base, small, medium, large-v3
WHISPER_LANGUAGE = "auto"  # auto, en, zh, etc.

# 语音合成配置
TTS_MODEL = "tts_models/en/ljspeech/vits"
TTS_VOICE_SPEED = 1.0

# 翻译配置
TRANSLATION_MODEL = "gpt-4"  # 或使用其他翻译模型
TRANSLATION_TIMEOUT = 30

# 文本处理配置
MAX_TEXT_LENGTH = 100000  # 最大文本长度
CHUNK_SIZE = 1000  # 文本分块大小

# 剧本生成配置
SCRIPT_GENERATION_MODEL = "gpt-4"
MAX_SCENES = 50
MAX_CHARACTERS = 20

# 文件上传配置
MAX_UPLOAD_SIZE = 104857600  # 100MB
ALLOWED_EXTENSIONS = [".txt", ".docx", ".pdf", ".mp3", ".wav"]

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "logs/yanzhi_ai.log"
LOG_ROTATION = "10 MB"
LOG_RETENTION = "7 days"

# 缓存配置
CACHE_TTL = 3600  # 1小时

# 限流配置
RATE_LIMIT = "100/minute"