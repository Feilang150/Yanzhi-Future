#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自然语言处理服务
提供文本分析、剧本生成、语法纠错等功能
"""

import os
import tempfile
import logging
import yaml
from typing import Dict, List, Optional
import openai
import spacy
import jieba
from config import OPENAI_API_KEY, SCRIPT_GENERATION_MODEL, MAX_TEXT_LENGTH

logger = logging.getLogger(__name__)


class NLPService:
    """自然语言处理服务类"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.nlp_en = None
        self.nlp_zh = None
        
    async def initialize(self):
        """初始化NLP模型"""
        try:
            logger.info("Loading NLP models...")
            
            # 加载英文NLP模型
            try:
                self.nlp_en = spacy.load("en_core_web_sm")
                logger.info("English NLP model loaded")
            except OSError:
                logger.warning("English NLP model not found, some features may be limited")
            
            # 加载中文NLP模型
            try:
                self.nlp_zh = spacy.load("zh_core_web_sm")
                logger.info("Chinese NLP model loaded")
            except OSError:
                logger.warning("Chinese NLP model not found, using jieba for Chinese text processing")
            
            logger.info("NLP service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP service: {e}")
            raise
    
    async def read_uploaded_file(self, file) -> str:
        """读取上传的文件内容"""
        try:
            content = await file.read()
            
            # 根据文件类型处理
            if file.filename.endswith('.txt'):
                text = content.decode('utf-8')
            elif file.filename.endswith('.docx'):
                from docx import Document
                import io
                doc = Document(io.BytesIO(content))
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                # 默认按文本处理
                text = content.decode('utf-8')
            
            logger.info(f"File read successfully: {len(text)} chars")
            return text
            
        except Exception as e:
            logger.error(f"Failed to read uploaded file: {e}")
            raise
    
    async def correct_grammar(self, text: str, language: str = "en", 
                             context: Optional[str] = None) -> Dict:
        """
        语法纠错
        
        Args:
            text: 要检查的文本
            language: 语言代码
            context: 上下文信息
            
        Returns:
            纠错结果
        """
        try:
            logger.info(f"Starting grammar correction: {language}")
            
            # 构建提示词
            system_prompt = f"""你是一个专业的语言纠错助手。请检查以下{language}文本的语法、用词和表达问题。
请返回JSON格式的结果，包含：
- is_correct: 是否正确
- errors: 错误列表，每个错误包含position（位置）、type（错误类型）、original（原文）、correction（修正建议）、explanation（解释）
- corrected_text: 修正后的文本
- suggestions: 改进建议"""
            
            # 调用OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            logger.info(f"Grammar correction completed: {len(result.get('errors', []))} errors found")
            
            return result
            
        except Exception as e:
            logger.error(f"Grammar correction failed: {e}")
            raise
    
    async def generate_script(self, novel_text: str, genre: str = "drama", 
                            style: str = "standard", max_scenes: int = 50) -> Dict:
        """
        剧本生成
        
        Args:
            novel_text: 小说文本
            genre: 剧本类型
            style: 风格
            max_scenes: 最大场景数
            
        Returns:
            生成的剧本（YAML格式）
        """
        try:
            logger.info(f"Starting script generation: {genre}, max {max_scenes} scenes")
            
            # 检查文本长度
            if len(novel_text) > MAX_TEXT_LENGTH:
                novel_text = novel_text[:MAX_TEXT_LENGTH]
                logger.warning(f"Text truncated to {MAX_TEXT_LENGTH} characters")
            
            # 构建提示词
            system_prompt = f"""你是一个专业的剧本创作助手。请根据提供的小说文本，创作一个符合YAML Schema规范的剧本。
剧本类型：{genre}
风格：{style}

YAML Schema格式：
```yaml
metadata:
  title: 剧本标题
  author: 作者姓名
  version: 1.0
  genre: 剧本类型
  synopsis: 剧本梗概（100-300字）

characters:
  - id: C001
    name: 人物姓名
    gender: 性别
    age: 年龄
    personality: 性格描述（50-100字）
    background: 背景简介（100-200字）
    traits:
      - 特质1
      - 特质2

scenes:
  - id: S001
    location: 场景地点
    time: 时间设定
    atmosphere: 氛围描述（50-100字）
    characters_involved:
      - C001
      - C002
    content:
      - type: description
        text: 场景描述（50-200字）
      - type: dialogue
        character_id: C001
        emotion: 情绪状态
        action: 动作提示（选填）
        line: 台词内容
```

要求：
1. 提取小说的核心情节和人物关系
2. 创建符合YAML Schema的结构化剧本
3. 场景数量不超过{max_scenes}个
4. 人物形象立体，对话自然流畅
5. 只返回YAML格式的内容，不要有其他解释"""
            
            # 调用OpenAI API
            response = await self.client.chat.completions.create(
                model=SCRIPT_GENERATION_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": novel_text}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            yaml_content = response.choices[0].message.content.strip()
            
            # 提取YAML内容（去除markdown标记）
            if yaml_content.startswith("```yaml"):
                yaml_content = yaml_content[7:]
            if yaml_content.startswith("```"):
                yaml_content = yaml_content[3:]
            if yaml_content.endswith("```"):
                yaml_content = yaml_content[:-3]
            
            yaml_content = yaml_content.strip()
            
            # 解析YAML验证格式
            try:
                script_data = yaml.safe_load(yaml_content)
                logger.info(f"Script generated successfully: {len(script_data.get('scenes', []))} scenes")
            except yaml.YAMLError as e:
                logger.error(f"Generated YAML is invalid: {e}")
                raise ValueError("生成的剧本格式不正确，请重试")
            
            return {
                "yaml_content": yaml_content,
                "script_data": script_data,
                "metadata": {
                    "character_count": len(script_data.get('characters', [])),
                    "scene_count": len(script_data.get('scenes', [])),
                    "word_count": len(yaml_content)
                }
            }
            
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            raise
    
    async def analyze_text(self, text: str, analysis_type: str = "all") -> Dict:
        """
        文本分析
        
        Args:
            text: 要分析的文本
            analysis_type: 分析类型
            
        Returns:
            分析结果
        """
        try:
            logger.info(f"Starting text analysis: {analysis_type}")
            
            results = {}
            
            if analysis_type in ["all", "sentiment"]:
                results["sentiment"] = await self._analyze_sentiment(text)
            
            if analysis_type in ["all", "keywords"]:
                results["keywords"] = await self.extract_keywords(text, top_n=10)
            
            if analysis_type in ["all", "entities"]:
                results["entities"] = await self._extract_entities(text)
            
            if analysis_type in ["all", "summary"]:
                results["summary"] = await self._summarize_text(text)
            
            logger.info(f"Text analysis completed")
            
            return results
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            raise
    
    async def _analyze_sentiment(self, text: str) -> Dict:
        """情感分析"""
        try:
            # 使用OpenAI进行情感分析
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "请分析以下文本的情感倾向，返回JSON格式，包含sentiment（positive/negative/neutral）、confidence（置信度）、details（详细分析）"},
                    {"role": "user", "content": text}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {}
    
    async def _extract_entities(self, text: str) -> List[Dict]:
        """实体提取"""
        try:
            entities = []
            
            # 使用spaCy进行英文实体提取
            if self.nlp_en:
                doc = self.nlp_en(text)
                for ent in doc.ents:
                    entities.append({
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "description": spacy.explain(ent.label_)
                    })
            
            # 如果没有提取到实体或中文文本，使用OpenAI
            if not entities:
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "请提取文本中的实体（人名、地名、机构名等），返回JSON数组，每个实体包含text、type、description"},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                
                import json
                result = json.loads(response.choices[0].message.content)
                entities = result.get("entities", [])
            
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
    
    async def _summarize_text(self, text: str) -> Dict:
        """文本摘要"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "请为以下文本生成摘要，返回JSON格式，包含summary（摘要）、key_points（关键点列表）、length（摘要字数）"},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Text summarization failed: {e}")
            return {}
    
    async def extract_keywords(self, text: str, top_n: int = 10, language: str = "en") -> List[Dict]:
        """
        关键词提取
        
        Args:
            text: 文本内容
            top_n: 返回前N个关键词
            language: 语言代码
            
        Returns:
            关键词列表
        """
        try:
            keywords = []
            
            # 中文使用jieba分词
            if language == "zh" or any('\u4e00' <= char <= '\u9fff' for char in text):
                import jieba.analyse
                jieba_words = jieba.analyse.extract_tags(text, topK=top_n, withWeight=True)
                keywords = [
                    {"word": word, "score": float(score), "language": "zh"}
                    for word, score in jieba_words
                ]
            
            # 英文使用spaCy或OpenAI
            else:
                if self.nlp_en:
                    doc = self.nlp_en(text)
                    # 提取名词和形容词作为关键词
                    for token in doc:
                        if token.pos_ in ["NOUN", "ADJ"] and not token.is_stop and len(token.text) > 2:
                            keywords.append({
                                "word": token.text,
                                "score": 1.0,  # spaCy不直接提供关键词评分
                                "language": "en"
                            })
                    
                    # 按出现频率排序
                    from collections import Counter
                    word_freq = Counter([k["word"].lower() for k in keywords])
                    keywords = [
                        {"word": word, "score": freq / len(keywords), "language": "en"}
                        for word, freq in word_freq.most_common(top_n)
                    ]
            
            # 如果没有提取到关键词，使用OpenAI
            if not keywords:
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"请提取文本中的前{top_n}个关键词，返回JSON数组，每个关键词包含word、score（重要性评分0-1）"},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                
                import json
                result = json.loads(response.choices[0].message.content)
                keywords = result.get("keywords", [])
            
            return keywords[:top_n]
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return []
    
    async def generate_dialogue(self, scenario: str, character_name: str, 
                               character_profile: Dict, previous_context: Optional[List[Dict]] = None) -> Dict:
        """
        对话生成
        
        Args:
            scenario: 场景描述
            character_name: 角色名称
            character_profile: 角色设定
            previous_context: 前文对话上下文
            
        Returns:
            生成的对话
        """
        try:
            logger.info(f"Generating dialogue for {character_name}")
            
            # 构建提示词
            context_prompt = ""
            if previous_context:
                context_lines = [f"{ctx['role']}: {ctx['content']}" for ctx in previous_context[-3:]]
                context_prompt = f"\n前文对话：\n" + "\n".join(context_lines)
            
            system_prompt = f"""你是一个专业的对话生成助手。根据以下信息生成角色的自然回应。

场景：{scenario}
角色：{character_name}
角色设定：
- 性格：{character_profile.get('personality', '')}
- 背景：{character_profile.get('background', '')}
- 特质：{', '.join(character_profile.get('traits', []))}
{context_prompt}

要求：
1. 回应要符合角色性格和场景设定
2. 语言自然流畅，避免机械感
3. 适当体现情感和语气
4. 长度控制在50字以内
5. 只返回对话内容，不要有其他解释"""
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请生成{character_name}的回应"}
                ],
                temperature=0.8,
                max_tokens=200
            )
            
            dialogue = response.choices[0].message.content.strip()
            
            logger.info(f"Dialogue generated for {character_name}: {len(dialogue)} chars")
            
            return {
                "character": character_name,
                "dialogue": dialogue,
                "emotion": "neutral",  # 可以进一步分析情感
                "action": ""  # 可以生成动作提示
            }
            
        except Exception as e:
            logger.error(f"Dialogue generation failed: {e}")
            raise
    
    async def validate_yaml_schema(self, content: str) -> Dict:
        """
        验证YAML剧本格式
        
        Args:
            content: YAML内容
            
        Returns:
            验证结果
        """
        try:
            logger.info("Validating YAML schema")
            
            # 解析YAML
            try:
                data = yaml.safe_load(content)
            except yaml.YAMLError as e:
                return {
                    "valid": False,
                    "errors": [f"YAML解析错误: {str(e)}"]
                }
            
            # 验证必需字段
            errors = []
            warnings = []
            
            # 验证metadata
            if 'metadata' not in data:
                errors.append("缺少metadata字段")
            else:
                metadata = data['metadata']
                required_fields = ['title', 'author', 'version', 'genre', 'synopsis']
                for field in required_fields:
                    if field not in metadata:
                        errors.append(f"metadata缺少必需字段: {field}")
                    elif not metadata[field]:
                        warnings.append(f"metadata字段{field}为空")
                
                # 验证字数限制
                if 'synopsis' in metadata:
                    synopsis_len = len(metadata['synopsis'])
                    if synopsis_len < 100 or synopsis_len > 300:
                        warnings.append(f"梗概长度应为100-300字，当前为{synopsis_len}字")
            
            # 验证characters
            if 'characters' not in data:
                errors.append("缺少characters字段")
            elif not isinstance(data['characters'], list):
                errors.append("characters应为数组")
            else:
                for i, char in enumerate(data['characters']):
                    if 'id' not in char:
                        errors.append(f"人物{i+1}缺少id字段")
                    if 'name' not in char:
                        errors.append(f"人物{i+1}缺少name字段")
            
            # 验证scenes
            if 'scenes' not in data:
                errors.append("缺少scenes字段")
            elif not isinstance(data['scenes'], list):
                errors.append("scenes应为数组")
            else:
                for i, scene in enumerate(data['scenes']):
                    if 'id' not in scene:
                        errors.append(f"场景{i+1}缺少id字段")
                    if 'location' not in scene:
                        errors.append(f"场景{i+1}缺少location字段")
                    if 'content' not in scene:
                        errors.append(f"场景{i+1}缺少content字段")
            
            result = {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
            
            logger.info(f"YAML validation completed: valid={result['valid']}")
            
            return result
            
        except Exception as e:
            logger.error(f"YAML validation failed: {e}")
            return {
                "valid": False,
                "errors": [f"验证过程出错: {str(e)}"]
            }
    
    async def cleanup(self):
        """清理资源"""
        try:
            # 清理OpenAI客户端
            if self.client:
                await self.client.close()
            
            logger.info("NLP service cleaned up")
        except Exception as e:
            logger.error(f"Failed to cleanup NLP service: {e}")