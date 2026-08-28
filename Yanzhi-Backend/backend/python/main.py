#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Yanzhi AI算法服务
提供语音识别、语音合成、翻译、NLP等AI能力
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from api import speech, translation, nlp, health
from utils.model_loader import ModelManager
from utils.cache import CacheManager

# 全局模型管理器
model_manager = None
cache_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global model_manager, cache_manager
    
    # 启动时初始化
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        # 初始化缓存管理器
        cache_manager = CacheManager(REDIS_URL)
        logger.info("Cache manager initialized")
        
        # 初始化模型管理器
        model_manager = ModelManager(MODEL_DIR, CACHE_DIR)
        await model_manager.initialize()
        logger.info("Model manager initialized")
        
        logger.info(f"{APP_NAME} started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # 关闭时清理
    logger.info("Shutting down application...")
    if model_manager:
        await model_manager.cleanup()
    if cache_manager:
        await cache_manager.close()
    logger.info("Application shut down complete")


# 创建FastAPI应用
app = FastAPI(
    title=APP_NAME,
    description="AI智能创作与语言服务算法支持",
    version=APP_VERSION,
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, prefix="/health", tags=["健康检查"])
app.include_router(speech.router, prefix="/speech", tags=["语音处理"])
app.include_router(translation.router, prefix="/translation", tags=["翻译服务"])
app.include_router(nlp.router, prefix="/nlp", tags=["自然语言处理"])

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": str(exc),
            "data": None
        }
    )


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    
    # 配置日志
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL
    )
    
    logger.add(
        LOG_FILE,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level=LOG_LEVEL
    )
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        workers=WORKERS if not DEBUG else 1,
        reload=DEBUG,
        log_level=LOG_LEVEL.lower()
    )