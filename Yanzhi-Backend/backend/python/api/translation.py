#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
翻译服务模块
提供实时翻译、文本翻译等功能
"""

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class TranslationRequest(BaseModel):
    """翻译请求"""
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    context: Optional[str] = None


class AudioTranslationRequest(BaseModel):
    """音频翻译请求"""
    target_language: str = "en"
    output_mode: str = "text"  # text, audio, both


class TranslationCorrection(BaseModel):
    """翻译纠错"""
    original_text: str
    translated_text: str
    correct_text: str
    error_type: str = "translation"


@router.post("/text")
async def translate_text(request: TranslationRequest):
    """
    文本翻译
    """
    try:
        from services.translation_service import TranslationService
        
        translation_service = TranslationService()
        
        # 进行翻译
        result = await translation_service.translate_text(
            request.text,
            request.source_language,
            request.target_language,
            request.context
        )
        
        return {
            "code": 200,
            "message": "翻译成功",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Text translation failed: {e}")
        return {
            "code": 500,
            "message": f"翻译失败: {str(e)}",
            "data": None
        }


@router.post("/audio")
async def translate_audio(
    audio: UploadFile = File(...),
    target_language: str = Form("en"),
    output_mode: str = Form("text")
):
    """
    音频翻译（语音识别+翻译）
    """
    try:
        from services.translation_service import TranslationService
        
        translation_service = TranslationService()
        
        # 保存音频文件
        audio_path = await translation_service.save_audio(audio)
        
        # 进行音频翻译
        result = await translation_service.translate_audio(
            audio_path,
            target_language,
            output_mode
        )
        
        return {
            "code": 200,
            "message": "翻译成功",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Audio translation failed: {e}")
        return {
            "code": 500,
            "message": f"翻译失败: {str(e)}",
            "data": None
        }


@router.post("/batch")
async def batch_translate(requests: List[TranslationRequest]):
    """
    批量翻译
    """
    try:
        from services.translation_service import TranslationService
        
        translation_service = TranslationService()
        
        # 批量翻译
        results = []
        for request in requests:
            result = await translation_service.translate_text(
                request.text,
                request.source_language,
                request.target_language,
                request.context
            )
            results.append(result)
        
        return {
            "code": 200,
            "message": "批量翻译成功",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Batch translation failed: {e}")
        return {
            "code": 500,
            "message": f"批量翻译失败: {str(e)}",
            "data": None
        }


@router.post("/correct")
async def submit_correction(correction: TranslationCorrection):
    """
    提交翻译纠错
    """
    try:
        from services.translation_service import TranslationService
        
        translation_service = TranslationService()
        
        # 保存纠错记录用于模型优化
        await translation_service.save_correction(correction)
        
        return {
            "code": 200,
            "message": "纠错提交成功",
            "data": None
        }
        
    except Exception as e:
        logger.error(f"Failed to submit correction: {e}")
        return {
            "code": 500,
            "message": f"提交失败: {str(e)}",
            "data": None
        }


@router.get("/languages")
async def get_supported_languages():
    """
    获取支持的语言列表
    """
    try:
        from services.translation_service import TranslationService
        
        translation_service = TranslationService()
        languages = translation_service.get_supported_languages()
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": languages
        }
        
    except Exception as e:
        logger.error(f"Failed to get languages: {e}")
        return {
            "code": 500,
            "message": f"获取失败: {str(e)}",
            "data": None
        }