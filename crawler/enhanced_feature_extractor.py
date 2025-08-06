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
        self.keywords = self._load_keywords()
        logger.info("Enhanced feature extractor (V4 Logic) initialized.")

    def _load_keywords(self) -> Dict[str, Dict[str, Set[str]]]:
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
            return processed_keywords
        except Exception as e:
            logger.error(f"Failed to load or process keywords config: {e}")
            return {}

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
            return 'unknown'

        positive_kws = self.keywords[feature_name].get('positive', set())
        negative_kws = self.keywords[feature_name].get('negative', set())
        optional_kws = self.keywords[feature_name].get('optional', set())
        
        text_lower = text_blob.lower()

        # 优先级: negative > optional > positive
        if negative_kws and any(kw in text_lower for kw in negative_kws):
            return 'no'
        
        if optional_kws and any(kw in text_lower for kw in optional_kws):
            return 'optional' # 'optional' 仅用于家具状态

        if positive_kws and any(kw in text_lower for kw in positive_kws):
            return 'yes'
            
        return 'unknown'

    def extract_features(self, property_features_list: List[str], headline: str, description: str) -> Dict[str, Any]:
        """
        主要的特征提取方法，实现V4方案。
        """
        extracted_data = {}

        # 1. 处理 is_furnished (两级判断逻辑)
        # 第一优先级: 检查官方列表
        furnish_status_from_list = self._check_list_for_feature('furnished', property_features_list)
        
        if furnish_status_from_list != 'unknown':
            extracted_data['is_furnished'] = furnish_status_from_list
        else:
            # 第二优先级: 检查文本
            text_blob = (headline + ' ' + description).lower()
            furnish_status_from_text = self._check_text_for_feature('furnished', text_blob)
            # 将 'optional' 映射为 'yes' 或其他定义，这里暂时也归为 'yes'
            if furnish_status_from_text == 'optional':
                 extracted_data['is_furnished'] = 'yes'
            else:
                 extracted_data['is_furnished'] = furnish_status_from_text

        # 2. 处理其他7个核心特征 (仅检查官方列表)
        other_features = [
            'air_conditioning', 'laundry', 'dishwasher', 
            'gas_cooking', 'intercom', 'study', 'balcony'
        ]
        for feature in other_features:
            column_name = f"has_{feature}"
            extracted_data[column_name] = self._check_list_for_feature(feature, property_features_list)

        return extracted_data
