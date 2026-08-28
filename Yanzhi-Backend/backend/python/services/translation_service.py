#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
翻译服务
提供文本翻译、音频翻译等功能
"""

import os
import tempfile
import logging
from typing import Dict, List, Optional
import openai
from config import OPENAI_API_KEY, TRANSLATION_MODEL, TRANSLATION_TIMEOUT

logger = logging.getLogger(__name__)


class TranslationService:
    """翻译服务类"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.supported_languages = {
            "auto": "自动识别",
            "zh": "中文",
            "en": "英语",
            "ja": "日语",
            "ko": "韩语",
            "fr": "法语",
            "de": "德语",
            "es": "西班牙语",
            "ru": "俄语",
            "ar": "阿拉伯语"
        }
    
    async def save_audio(self, audio_file) -> str:
        """保存上传的音频文件"""
        try:
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, f"translate_audio_{os.urandom(8).hex()}")
            
            with open(audio_path, "wb") as f:
                content = await audio_file.read()
                f.write(content)
            
            logger.info(f"Translation audio saved to: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Failed to save translation audio: {e}")
            raise
    
    async def translate_text(self, text: str, source_language: str = "auto", 
                            target_language: str = "en", context: Optional[str] = None) -> Dict:
        """
        文本翻译
        
        Args:
            text: 要翻译的文本
            source_language: 源语言
            target_language: 目标语言
            context: 上下文信息
            
        Returns:
            翻译结果
        """
        try:
            logger.info(f"Starting text translation: {source_language} -> {target_language}")
            
            # 构建提示词
            system_prompt = self._build_translation_prompt(source_language, target_language, context)
            
            # 调用OpenAI API
            response = await self.client.chat.completions.create(
                model=TRANSLATION_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                timeout=TRANSLATION_TIMEOUT
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            logger.info(f"Text translation completed: {len(translated_text)} chars")
            
            return {
                "original_text": text,
                "translated_text": translated_text,
                "source_language": source_language,
                "target_language": target_language,
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Text translation failed: {e}")
            raise
    
    async def translate_audio(self, audio_path: str, target_language: str = "en", 
                             output_mode: str = "text") -> Dict:
        """
        音频翻译（语音识别+翻译）
        
        Args:
            audio_path: 音频文件路径
            target_language: 目标语言
            output_mode: 输出模式 (text, audio, both)
            
        Returns:
            翻译结果
        """
        try:
            logger.info(f"Starting audio translation to {target_language}")
            
            # 首先进行语音识别
            from services.speech_service import SpeechService
            speech_service = SpeechService()
            
            recognition_result = await speech_service.recognize(audio_path, language="auto")
            original_text = recognition_result["text"]
            source_language = recognition_result["language"]
            
            # 进行文本翻译
            translation_result = await self.translate_text(
                original_text,
                source_language,
                target_language
            )
            
            # 根据输出模式生成音频
            audio_url = None
            if output_mode in ["audio", "both"]:
                audio_url = await self._generate_audio(translation_result["translated_text"], target_language)
            
            result = {
                "original_text": original_text,
                "translated_text": translation_result["translated_text"],
                "source_language": source_language,
                "target_language": target_language,
                "audio_url": audio_url
            }
            
            logger.info(f"Audio translation completed")
            
            return result
            
        except Exception as e:
            logger.error(f"Audio translation failed: {e}")
            raise
    
    async def _generate_audio(self, text: str, language: str) -> str:
        """生成翻译文本的音频"""
        try:
            from services.speech_service import SpeechService
            speech_service = SpeechService()
            
            audio_path = await speech_service.synthesize(text, output_format="mp3")
            
            # 在实际应用中，这里应该上传到文件存储服务并返回URL
            return audio_path
            
        except Exception as e:
            logger.error(f"Failed to generate audio: {e}")
            return None
    
    def _build_translation_prompt(self, source_language: str, target_language: str, 
                                  context: Optional[str] = None) -> str:
        """构建翻译提示词"""
        source_name = self.supported_languages.get(source_language, source_language)
        target_name = self.supported_languages.get(target_language, target_language)
        
        prompt = f"""你是一个专业的翻译助手。请将以下文本从{source_name}翻译成{target_name}。
要求：
1. 翻译准确、自然、流畅
2. 保持原文的语气和风格
3. 注意专业术语和习惯表达
4. 确保语法正确"""
        
        if context:
            prompt += f"\n5. 结合以下上下文进行翻译：{context}"
        
        return prompt
    
    async def save_correction(self, correction: Dict) -> bool:
        """
        保存翻译纠错记录
        
        Args:
            correction: 纠错数据
            
        Returns:
            是否保存成功
        """
        try:
            # 在实际应用中，这里应该保存到数据库
            # 用于后续的模型训练和优化
            
            logger.info(f"Translation correction saved: {correction}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save correction: {e}")
            return False
    
    def get_supported_languages(self) -> List[Dict]:
        """获取支持的语言列表"""
        try:
            return [
                {"code": code, "name": name}
                for code, name in self.supported_languages.items()
            ]
        except Exception as e:
            logger.error(f"Failed to get supported languages: {e}")
            return []
    
    async def translate_with_context(self, texts: List[str], source_language: str = "auto", 
                                   target_language: str = "en") -> List[Dict]:
        """
        带上下文的批量翻译
        
        Args:
            texts: 文本列表
            source_language: 源语言
            target_language: 目标语言
            
        Returns:
            翻译结果列表
        """
        try:
            results = []
            for i, text in enumerate(texts):
                # 使用前文作为上下文
                context = " ".join(texts[max(0, i-2):i]) if i > 0 else None
                
                result = await self.translate_text(
                    text,
                    source_language,
                    target_language,
                    context
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Context-aware translation failed: {e}")
            raise
    
    async def detect_language(self, text: str) -> str:
        """
        语言检测
        
        Args:
            text: 文本内容
            
        Returns:
            检测到的语言代码
        """
        try:
            # 使用OpenAI进行语言检测
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "请识别以下文本的语言，只返回语言代码（如：zh, en, ja等）"},
                    {"role": "user", "content": text[:100]}  # 只使用前100个字符
                ],
                temperature=0.1
            )
            
            detected_language = response.choices[0].message.content.strip().lower()
            
            # 确保返回支持的语言代码
            if detected_language not in self.supported_languages:
                detected_language = "auto"
            
            return detected_language
            
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return "auto"
    
    async def cleanup(self):
        """清理资源"""
        try:
            # 清理OpenAI客户端
            if self.client:
                await self.client.close()
            
            logger.info("Translation service cleaned up")
        except Exception as e:
            logger.error(f"Failed to cleanup translation service: {e}")