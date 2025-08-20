#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
特征提取器 V2 - 遵循V4重构计划
- 为 is_furnished 实现两级判断逻辑
- 为其他7个核心特征实现基于 property_features 的一级判断
- 简化整体逻辑，移除动态类创建
"""

import re
import yaml
import logging
from typing import List, Optional, Set, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedFeatureExtractor:
    """
    重构后的特征提取器，实现V4方案的精准逻辑。
    """
    
    def __init__(self):
        """
        初始化提取器，加载唯一的关键词配置文件。
        """
        self.config, self.keywords = self._load_keywords()
        logger.info("Enhanced feature extractor (V4 Logic) initialized.")

    def _load_keywords(self) -> tuple[Dict[str, Any], Dict[str, Dict[str, Set[str]]]]:
        """
        加载并预处理 property_features_keywords.yaml 文件。
        """
        config_path = Path(__file__).parent / 'config' / 'property_features_keywords.yaml'
        if not config_path.exists():
            logger.error(f"CRITICAL: Keywords config file not found at {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # 将所有关键词转换为小写set以便快速、不区分大小写地查找
            processed_keywords = {}
            for feature, types in config_data.items():
                processed_keywords[feature] = {}
                for key_type, words in types.items():
                    processed_keywords[feature][key_type] = {str(word).lower() for word in words} if words else set()
            return config_data, processed_keywords
        except Exception as e:
            logger.error(f"Failed to load or process keywords config: {e}")
            return {}, {}

    def _check_list_for_feature(self, feature_name: str, feature_list: List[str]) -> str:
        """
        在官方特征列表中检查单个特征。
        """
        if not self.keywords.get(feature_name):
            return 'unknown'

        positive_kws = self.keywords[feature_name].get('positive', set())
        negative_kws = self.keywords[feature_name].get('negative', set())
        
        feature_set = {item.lower().strip() for item in feature_list}

        # 优先检查否定关键词
        if not negative_kws.isdisjoint(feature_set):
            return 'no'
        
        # 检查肯定关键词
        if not positive_kws.isdisjoint(feature_set):
            return 'yes'
            
        return 'unknown'

    def _check_text_for_feature(self, feature_name: str, text_blob: str) -> str:
        """
        在文本块中检查单个特征。
        """
        if not self.keywords.get(feature_name) or not text_blob:
            logger.debug(f"[{feature_name}] 文本为空或配置缺失，返回 unknown")
            return 'unknown'

        positive_kws = self.keywords[feature_name].get('positive', set())
        negative_kws = self.keywords[feature_name].get('negative', set())
        optional_kws = self.keywords[feature_name].get('optional', set())
        
        text_lower = text_blob.lower()
        
        # 调试日志：显示正在检查的文本和关键词
        logger.debug(f"[{feature_name}] 检查文本: {text_lower[:100]}...")
        logger.debug(f"[{feature_name}] 正面关键词: {positive_kws}")
        logger.debug(f"[{feature_name}] 负面关键词: {negative_kws}")
        logger.debug(f"[{feature_name}] 可选关键词: {optional_kws}")

        # 优先级: negative > optional > positive
        if negative_kws and any(kw in text_lower for kw in negative_kws):
            found_neg_kw = next(kw for kw in negative_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到负面关键词 '{found_neg_kw}'，返回 no")
            return 'no'
        
        if optional_kws and any(kw in text_lower for kw in optional_kws):
            found_opt_kw = next(kw for kw in optional_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到可选关键词 '{found_opt_kw}'，返回 optional")
            return 'optional' # 'optional' 仅用于家具状态

        if positive_kws and any(kw in text_lower for kw in positive_kws):
            found_pos_kw = next(kw for kw in positive_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到正面关键词 '{found_pos_kw}'，返回 yes")
            return 'yes'
            
        logger.debug(f"[{feature_name}] 未找到任何关键词，返回 unknown")
        return 'unknown'

    def extract_features(self, property_features_list: List[str], headline: str, description: str) -> Dict[str, Any]:
        """
        主要的特征提取方法，实现V4方案。
        """
        # 调试日志：显示传入的原始数据
        logger.debug(f"=== 开始特征提取 ===")
        logger.debug(f"Property Features List: {property_features_list}")
        logger.debug(f"Headline: {headline[:100] if headline else 'Empty'}...")
        logger.debug(f"Description: {description[:100] if description else 'Empty'}...")
        
        extracted_data = {}

        # 1. 处理 is_furnished (两级判断逻辑)
        logger.debug(f"=== 处理 is_furnished ===")
        # 第一优先级: 检查官方列表
        furnish_status_from_list = self._check_list_for_feature('furnished', property_features_list)
        logger.debug(f"从列表检查结果: {furnish_status_from_list}")
        
        if furnish_status_from_list != 'unknown':
            extracted_data['is_furnished'] = furnish_status_from_list
            logger.debug(f"使用列表检查结果: {furnish_status_from_list}")
        else:
            # 第二优先级: 检查文本
            text_blob = (headline + ' ' + description)
            logger.debug(f"进入文本检查，合并文本长度: {len(text_blob)}")
            furnish_status_from_text = self._check_text_for_feature('furnished', text_blob)
            logger.debug(f"文本检查结果: {furnish_status_from_text}")
            # 将 'optional' 映射为 'yes' 或其他定义，这里暂时也归为 'yes'
            if furnish_status_from_text == 'optional':
                 extracted_data['is_furnished'] = 'yes'
                 logger.debug(f"将 'optional' 映射为 'yes'")
            else:
                 extracted_data['is_furnished'] = furnish_status_from_text
                 logger.debug(f"使用文本检查结果: {furnish_status_from_text}")

        # 2. 处理其他7个核心特征 (仅检查官方列表)
        logger.debug(f"=== 处理其他特征 ===")
        other_features = [
            'air_conditioning', 'laundry', 'dishwasher', 
            'gas_cooking', 'intercom', 'study', 'balcony'
        ]
        for feature in other_features:
            column_name = f"has_{feature}"
            result = self._check_list_for_feature(feature, property_features_list)
            extracted_data[column_name] = result
            logger.debug(f"{column_name}: {result}")

        logger.debug(f"=== 特征提取完成，最终结果: {extracted_data} ===")
        return extracted_data
