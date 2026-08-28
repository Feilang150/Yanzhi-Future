#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自然语言处理模块
提供文本分析、剧本生成、语法纠错等功能
"""

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class GrammarCorrectionRequest(BaseModel):
    """语法纠错请求"""
    text: str
    language: str = "en"
    context: Optional[str] = None


class ScriptGenerationRequest(BaseModel):
    """剧本生成请求"""
    novel_text: str
    genre: Optional[str] = "drama"
    style: Optional[str] = "standard"
    max_scenes: int = 50


class TextAnalysisRequest(BaseModel):
    """文本分析请求"""
    text: str
    analysis_type: str = "all"  # all, sentiment, keywords, entities


class DialogueGenerationRequest(BaseModel):
    """对话生成请求"""
    scenario: str
    character_name: str
    character_profile: dict
    previous_context: Optional[List[dict]] = None


@router.post("/correct-grammar")
async def correct_grammar(request: GrammarCorrectionRequest):
    """
    语法纠错
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 进行语法纠错
        corrections = await nlp_service.correct_grammar(
            request.text,
            request.language,
            request.context
        )
        
        return {
            "code": 200,
            "message": "纠错完成",
            "data": corrections
        }
        
    except Exception as e:
        logger.error(f"Grammar correction failed: {e}")
        return {
            "code": 500,
            "message": f"纠错失败: {str(e)}",
            "data": None
        }


@router.post("/generate-script")
async def generate_script(
    file: UploadFile = File(...),
    genre: str = Form("drama"),
    style: str = Form("standard"),
    max_scenes: int = Form(50)
):
    """
    剧本生成
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 读取文件内容
        novel_text = await nlp_service.read_uploaded_file(file)
        
        # 生成剧本
        script = await nlp_service.generate_script(
            novel_text,
            genre,
            style,
            max_scenes
        )
        
        return {
            "code": 200,
            "message": "剧本生成成功",
            "data": script
        }
        
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        return {
            "code": 500,
            "message": f"生成失败: {str(e)}",
            "data": None
        }


@router.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """
    文本分析
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 进行文本分析
        analysis = await nlp_service.analyze_text(
            request.text,
            request.analysis_type
        )
        
        return {
            "code": 200,
            "message": "分析完成",
            "data": analysis
        }
        
    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        return {
            "code": 500,
            "message": f"分析失败: {str(e)}",
            "data": None
        }


@router.post("/generate-dialogue")
async def generate_dialogue(request: DialogueGenerationRequest):
    """
    对话生成
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 生成对话
        dialogue = await nlp_service.generate_dialogue(
            request.scenario,
            request.character_name,
            request.character_profile,
            request.previous_context
        )
        
        return {
            "code": 200,
            "message": "对话生成成功",
            "data": dialogue
        }
        
    except Exception as e:
        logger.error(f"Dialogue generation failed: {e}")
        return {
            "code": 500,
            "message": f"生成失败: {str(e)}",
            "data": None
        }


@router.post("/extract-keywords")
async def extract_keywords(
    text: str = Form(...),
    top_n: int = Form(10),
    language: str = Form("en")
):
    """
    关键词提取
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 提取关键词
        keywords = await nlp_service.extract_keywords(text, top_n, language)
        
        return {
            "code": 200,
            "message": "关键词提取成功",
            "data": keywords
        }
        
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}")
        return {
            "code": 500,
            "message": f"提取失败: {str(e)}",
            "data": None
        }


@router.post("/validate-yaml")
async def validate_yaml_schema(content: str = Form(...)):
    """
    验证YAML剧本格式
    """
    try:
        from services.nlp_service import NLPService
        
        nlp_service = NLPService()
        
        # 验证YAML格式
        validation_result = await nlp_service.validate_yaml_schema(content)
        
        return {
            "code": 200,
            "message": "验证完成",
            "data": validation_result
        }
        
    except Exception as e:
        logger.error(f"YAML validation failed: {e}")
        return {
            "code": 500,
            "message": f"验证失败: {str(e)}",
            "data": None
        }