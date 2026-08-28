#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语音处理服务
提供语音识别、语音合成、发音评测等功能
"""

import os
import tempfile
import logging
from typing import Dict, List, Optional
import torch
import whisper
import numpy as np
from TTS.api import TTS

from config import WHISPER_MODEL, TTS_MODEL, TTS_VOICE_SPEED

logger = logging.getLogger(__name__)


class SpeechService:
    """语音处理服务类"""
    
    def __init__(self):
        self.whisper_model = None
        self.tts_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def initialize(self):
        """初始化模型"""
        try:
            logger.info("Loading speech recognition model...")
            self.whisper_model = whisper.load_model(WHISPER_MODEL, device=self.device)
            
            logger.info("Loading text-to-speech model...")
            self.tts_model = TTS(model_name=TTS_MODEL).to(self.device)
            
            logger.info("Speech service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize speech service: {e}")
            raise
    
    async def save_audio(self, audio_file) -> str:
        """保存上传的音频文件"""
        try:
            # 创建临时文件
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, f"audio_{os.urandom(8).hex()}")
            
            # 保存文件
            with open(audio_path, "wb") as f:
                content = await audio_file.read()
                f.write(content)
            
            logger.info(f"Audio saved to: {audio_path}")
            return audio_path
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
            raise
    
    async def recognize(self, audio_path: str, language: str = "auto", model: str = "large-v3") -> Dict:
        """
        语音识别
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码 (auto, en, zh, etc.)
            model: Whisper模型名称
            
        Returns:
            识别结果字典
        """
        try:
            logger.info(f"Starting speech recognition: {audio_path}")
            
            # 加载音频
            audio = whisper.load_audio(audio_path)
            
            # 设置识别参数
            options = {
                "language": None if language == "auto" else language,
                "task": "transcribe",
                "fp16": torch.cuda.is_available()
            }
            
            # 进行识别
            result = self.whisper_model.transcribe(audio, **options)
            
            # 提取结果
            recognized_text = result["text"].strip()
            segments = [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                }
                for seg in result["segments"]
            ]
            
            logger.info(f"Speech recognition completed: {len(recognized_text)} chars")
            
            return {
                "text": recognized_text,
                "segments": segments,
                "language": result.get("language", language)
            }
            
        except Exception as e:
            logger.error(f"Speech recognition failed: {e}")
            raise
    
    async def synthesize(self, text: str, voice: str = "default", 
                        speed: float = 1.0, output_format: str = "mp3") -> str:
        """
        语音合成
        
        Args:
            text: 要合成的文本
            voice: 语音类型
            speed: 语速
            output_format: 输出格式
            
        Returns:
            生成的音频文件路径
        """
        try:
            logger.info(f"Starting speech synthesis: {len(text)} chars")
            
            # 创建输出文件路径
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"tts_{os.urandom(8).hex()}.{output_format}")
            
            # 进行语音合成
            self.tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                speed=speed
            )
            
            logger.info(f"Speech synthesis completed: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            raise
    
    async def evaluate_pronunciation(self, audio_path: str, reference_text: str, 
                                    language: str = "en") -> Dict:
        """
        发音评测
        
        Args:
            audio_path: 用户录音文件路径
            reference_text: 参考文本
            language: 语言代码
            
        Returns:
            评测结果
        """
        try:
            logger.info(f"Starting pronunciation evaluation")
            
            # 首先进行语音识别
            recognition_result = await self.recognize(audio_path, language)
            user_text = recognition_result["text"]
            
            # 计算相似度和错误率
            similarity = self._calculate_similarity(user_text, reference_text)
            error_rate = self._calculate_error_rate(user_text, reference_text)
            
            # 生成详细评测
            evaluation = {
                "user_text": user_text,
                "reference_text": reference_text,
                "overall_score": min(100, int(similarity * 100)),
                "similarity": round(similarity, 4),
                "error_rate": round(error_rate, 4),
                "details": {
                    "pronunciation": self._evaluate_pronunciation_details(user_text, reference_text),
                    "fluency": self._evaluate_fluency(user_text),
                    "accuracy": self._evaluate_accuracy(user_text, reference_text)
                }
            }
            
            logger.info(f"Pronunciation evaluation completed: {evaluation['overall_score']}")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Pronunciation evaluation failed: {e}")
            raise
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        try:
            from difflib import SequenceMatcher
            return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    def _calculate_error_rate(self, user_text: str, reference_text: str) -> float:
        """计算错误率"""
        try:
            similarity = self._calculate_similarity(user_text, reference_text)
            return 1.0 - similarity
        except Exception as e:
            logger.error(f"Failed to calculate error rate: {e}")
            return 1.0
    
    def _evaluate_pronunciation_details(self, user_text: str, reference_text: str) -> Dict:
        """评估发音细节"""
        try:
            # 这里可以集成更专业的发音评测模型
            return {
                "phonemes": [],
                "stress": [],
                "intonation": [],
                "overall": "good"
            }
        except Exception as e:
            logger.error(f"Failed to evaluate pronunciation details: {e}")
            return {}
    
    def _evaluate_fluency(self, text: str) -> Dict:
        """评估流利度"""
        try:
            words = text.split()
            if not words:
                return {"score": 0, "feedback": "无内容"}
            
            # 基于文本长度和复杂度的简单评估
            score = min(100, len(words) * 5)
            feedback = "流利" if score > 80 else "需要练习"
            
            return {"score": score, "feedback": feedback}
        except Exception as e:
            logger.error(f"Failed to evaluate fluency: {e}")
            return {"score": 0, "feedback": "评估失败"}
    
    def _evaluate_accuracy(self, user_text: str, reference_text: str) -> Dict:
        """评估准确性"""
        try:
            similarity = self._calculate_similarity(user_text, reference_text)
            score = int(similarity * 100)
            
            if score > 90:
                feedback = "优秀"
            elif score > 80:
                feedback = "良好"
            elif score > 60:
                feedback = "一般"
            else:
                feedback = "需要改进"
            
            return {"score": score, "feedback": feedback}
        except Exception as e:
            logger.error(f"Failed to evaluate accuracy: {e}")
            return {"score": 0, "feedback": "评估失败"}
    
    def get_audio_duration(self, audio_path: str) -> float:
        """获取音频时长"""
        try:
            import librosa
            duration = librosa.get_duration(filename=audio_path)
            return duration
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            return 0.0
    
    def get_available_voices(self) -> List[Dict]:
        """获取可用的语音列表"""
        try:
            # 这里返回TTS模型支持的语音列表
            return [
                {"id": "default", "name": "默认语音", "language": "en"},
                {"id": "male", "name": "男声", "language": "en"},
                {"id": "female", "name": "女声", "language": "en"}
            ]
        except Exception as e:
            logger.error(f"Failed to get available voices: {e}")
            return []
    
    async def cleanup(self):
        """清理资源"""
        try:
            if self.whisper_model:
                del self.whisper_model
            if self.tts_model:
                del self.tts_model
            
            # 清理GPU缓存
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("Speech service cleaned up")
        except Exception as e:
            logger.error(f"Failed to cleanup speech service: {e}")