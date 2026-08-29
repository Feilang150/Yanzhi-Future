#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语音处理模块
提供语音识别、语音合成等功能
"""

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class SpeechRecognitionRequest(BaseModel):
    """语音识别请求"""
    language: str = "auto"
    model: str = "large-v3"
    enable_punctuation: bool = True


class SpeechSynthesisRequest(BaseModel):
    """语音合成请求"""
    text: str
    voice: str = "default"
    speed: float = 1.0
    output_format: str = "mp3"


class PronunciationEvaluationRequest(BaseModel):
    """发音评测请求"""
    audio_path: str
    reference_text: str
    language: str = "en"


@router.post("/recognize")
async def recognize_speech(
    audio: UploadFile = File(...),
    language: str = Form("auto"),
    model: str = Form("large-v3")
):
    """
    语音识别
    """
    try:
        from services.speech_service import SpeechService
        
        speech_service = SpeechService()
        
        # 保存上传的音频文件
        audio_path = await speech_service.save_audio(audio)
        
        # 进行语音识别
        result = await speech_service.recognize(audio_path, language, model)
        
        return {
            "code": 200,
            "message": "识别成功",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Speech recognition failed: {e}")
        return {
            "code": 500,
            "message": f"识别失败: {str(e)}",
            "data": None
        }


@router.post("/synthesize")
async def synthesize_speech(request: SpeechSynthesisRequest):
    """
    语音合成
    """
    try:
        from services.speech_service import SpeechService
        
        speech_service = SpeechService()
        
        # 进行语音合成
        audio_path = await speech_service.synthesize(
            request.text,
            request.voice,
            request.speed,
            request.output_format
        )
        
        return {
            "code": 200,
            "message": "合成成功",
            "data": {
                "audio_path": audio_path,
                "duration": speech_service.get_audio_duration(audio_path)
            }
        }
        
    except Exception as e:
        logger.error(f"Speech synthesis failed: {e}")
        return {
            "code": 500,
            "message": f"合成失败: {str(e)}",
            "data": None
        }


@router.post("/evaluate-pronunciation")
async def evaluate_pronunciation(request: PronunciationEvaluationRequest):
    """
    发音评测
    """
    try:
        from services.speech_service import SpeechService
        
        speech_service = SpeechService()
        
        # 进行发音评测
        evaluation = await speech_service.evaluate_pronunciation(
            request.audio_path,
            request.reference_text,
            request.language
        )
        
        return {
            "code": 200,
            "message": "评测成功",
            "data": evaluation
        }
        
    except Exception as e:
        logger.error(f"Pronunciation evaluation failed: {e}")
        return {
            "code": 500,
            "message": f"评测失败: {str(e)}",
            "data": None
        }


@router.get("/voices")
async def get_available_voices():
    """
    获取可用的语音列表
    """
    try:
        from services.speech_service import SpeechService
        
        speech_service = SpeechService()
        voices = speech_service.get_available_voices()
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": voices
        }
        
    except Exception as e:
        logger.error(f"Failed to get voices: {e}")
        return {
            "code": 500,
            "message": f"获取失败: {str(e)}",
            "data": None
        }