# Python AI服务 Dockerfile

# 基础镜像
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/models /app/cache /app/uploads

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 下载必要的NLP模型（可选，避免启动时下载）
RUN python -m spacy download en_core_web_sm || true

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 创建非root用户
RUN groupadd -r yanzhi && useradd -r -g yanzhi yanzhi
RUN chown -R yanzhi:yanzhi /app

# 切换到非root用户
USER yanzhi

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]