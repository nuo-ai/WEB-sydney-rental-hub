#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
增强的特征提取器 - 实现三态逻辑
支持 'yes'/'no'/'unknown' 三种状态
"""

import re
import json
import yaml
import logging
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field, fields, make_dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

def create_enhanced_property_features_class(features_config: Optional[List[Dict[str, Any]]]) -> type:
    """
    创建增强的PropertyFeatures数据类，所有特征字段都使用三态逻辑
    """
    fields_to_create = [
        # 保留现有的特殊字段，但统一为三态逻辑
        ('furnishing_status', str, field(default='unknown')),  # 'furnished'/'unfurnished'/'unknown'
        ('air_conditioning_type', str, field(default='unknown')),  # 'ducted'/'split'/'reverse_cycle'/'general'/'unknown'
        ('has_air_conditioning', str, field(default='unknown')),  # 'yes'/'no'/'unknown'
    ]
    
    if features_config:
        for config in features_config:
            field_name = config.get('column_name')
            if field_name and not any(f[0] == field_name for f in fields_to_create):
                # 所有特征字段都使用str类型，默认值为'unknown'
                fields_to_create.append((field_name, str, field(default='unknown')))

    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def merge(self, other) -> None:
        # 三态逻辑合并：unknown < no/yes，优先保留明确的状态
        for f in fields(self):
            current_value = getattr(self, f.name)
            other_value = getattr(other, f.name)
            
            if current_value == 'unknown':
                setattr(self, f.name, other_value)
            elif other_value != 'unknown' and current_value != other_value:
                # 如果有冲突，记录警告但保留当前值
                logger.warning(f"Feature conflict for {f.name}: {current_value} vs {other_value}")

    namespace = {
        'to_dict': to_dict,
        'merge': merge,
        '__annotations__': {f[0]: f[1] for f in fields_to_create}
    }

    DynamicPropertyFeatures = make_dataclass(
        'PropertyFeatures',
        fields=[(f[0], f[1], f[2]) if len(f) > 2 else (f[0], f[1]) for f in fields_to_create],
        namespace=namespace
    )
    return DynamicPropertyFeatures


class EnhancedFeatureExtractor:
    """
    增强的特征提取器，实现统一的三态逻辑
    """
    
    def __init__(self, features_config: Optional[List[Dict[str, Any]]], 
                 furniture_keywords: Optional[dict], 
                 aircon_keywords: Optional[dict]):
        self.features_config = features_config or []
        self.furniture_keywords = furniture_keywords or {}
        self.aircon_keywords = aircon_keywords or {}
        
        # 构建特征关键词映射
        self.feature_keywords = self._build_feature_keywords()
        
        # 预处理家具关键词
        self._load_furniture_keywords()
        
        # 预处理空调关键词
        self._load_aircon_keywords()
        
        logger.info(f"Enhanced feature extractor initialized with {len(self.feature_keywords)} features")

    def _build_feature_keywords(self) -> Dict[str, Dict[str, Set[str]]]:
        """
        构建特征关键词映射，支持positive和negative关键词
        """
        feature_keywords = {}
        
        for config in self.features_config:
            column_name = config.get('column_name')
            if not column_name:
                continue
                
            feature_keywords[column_name] = {
                'positive': set(),
                'negative': set()
            }
            
            # 添加正向关键词
            positive_kws = config.get('keywords', [])
            for kw in positive_kws:
                feature_keywords[column_name]['positive'].add(kw.lower())
            
            # 添加负向关键词
            negative_kws = config.get('negative_keywords', [])
            for kw in negative_kws:
                feature_keywords[column_name]['negative'].add(kw.lower())
                
        return feature_keywords

    def _load_furniture_keywords(self):
        """加载并预处理家具关键词"""
        self.furniture_positive = set()
        self.furniture_negative = set()
        self.furniture_optional = set()
        
        if self.furniture_keywords:
            # 处理正向关键词
            positive_config = self.furniture_keywords.get('positive_keywords', {})
            for category_keywords in positive_config.values():
                self.furniture_positive.update(kw.lower() for kw in category_keywords)
            
            # 处理负向关键词
            negative_config = self.furniture_keywords.get('negative_keywords', {})
            for category_keywords in negative_config.values():
                self.furniture_negative.update(kw.lower() for kw in category_keywords)
            
            # 处理可选关键词
            optional_config = self.furniture_keywords.get('optional_keywords', {})
            for category_keywords in optional_config.values():
                self.furniture_optional.update(kw.lower() for kw in category_keywords)

    def _load_aircon_keywords(self):
        """加载并预处理空调关键词"""
        self.aircon_categories = {}
        self.aircon_priority_order = [
            'negative_keywords', 'ducted_keywords', 'reverse_cycle_keywords',
            'split_system_keywords', 'general_keywords', 'other_keywords'
        ]
        
        if self.aircon_keywords:
            for category in self.aircon_priority_order:
                if category in self.aircon_keywords:
                    self.aircon_categories[category] = set()
                    config = self.aircon_keywords[category]
                    for category_keywords in config.values():
                        self.aircon_categories[category].update(kw.lower() for kw in category_keywords)

    def _extract_ternary_feature(self, text: str, positive_keywords: Set[str], 
                                negative_keywords: Set[str]) -> str:
        """
        三态特征提取的核心逻辑
        优先级：negative > positive > unknown
        """
        if not text:
            return 'unknown'
            
        text_lower = text.lower()
        
        # 优先检查负向关键词
        if negative_keywords and any(keyword in text_lower for keyword in negative_keywords):
            return 'no'
        
        # 检查正向关键词
        if positive_keywords and any(keyword in text_lower for keyword in positive_keywords):
            return 'yes'
        
        return 'unknown'

    def _get_furnishing_status(self, text: str) -> str:
        """
        改进的家具状态检测，返回标准化的三态值
        """
        if not text:
            return 'unknown'
            
        text_lower = text.lower()
        
        # 优先级：negative > optional > positive
        if any(keyword in text_lower for keyword in self.furniture_negative):
            return 'unfurnished'  # 保持现有的furnishing_status值格式
        
        if any(keyword in text_lower for keyword in self.furniture_optional):
            return 'optional'
        
        if any(keyword in text_lower for keyword in self.furniture_positive):
            return 'furnished'
        
        return 'unknown'

    def _get_air_conditioning_info(self, text: str) -> tuple[str, str]:
        """
        改进的空调检测，返回(has_air_conditioning, air_conditioning_type)
        """
        if not text or not self.aircon_categories:
            return 'unknown', 'unknown'
            
        text_lower = text.lower()
        
        # 按优先级检查
        for category in self.aircon_priority_order:
            if category in self.aircon_categories:
                keywords = self.aircon_categories[category]
                if any(keyword in text_lower for keyword in keywords):
                    if category == 'negative_keywords':
                        return 'no', 'none'
                    else:
                        ac_type = category.replace('_keywords', '')
                        return 'yes', ac_type
        
        return 'unknown', 'unknown'

    def extract(self, json_data: dict, headline: str, description: str, 
                feature_list: List[str]):
        """
        主要的特征提取方法，实现统一的三态逻辑
        """
        # 动态创建PropertyFeatures类
        PropertyFeatures = create_enhanced_property_features_class(self.features_config)
        features = PropertyFeatures()
        
        # 构建待分析的文本
        text_sources = [
            headline.lower() if headline else "",
            description.lower() if description else "",
            ' '.join(f.lower() for f in feature_list)
        ]
        
        # 添加结构化特征
        structured_features = {f.get("name", "").lower() for f in json_data.get("structuredFeatures", [])}
        text_sources.append(' '.join(structured_features))
        
        text_blob = ' '.join(text_sources)
        
        # 使用三态逻辑提取通用特征
        for feature_name, keywords_dict in self.feature_keywords.items():
            if hasattr(features, feature_name):
                positive_keywords = keywords_dict['positive']
                negative_keywords = keywords_dict['negative']
                
                feature_value = self._extract_ternary_feature(
                    text_blob, positive_keywords, negative_keywords
                )
                setattr(features, feature_name, feature_value)
        
        # 特殊处理：家具状态
        features.furnishing_status = self._get_furnishing_status(text_blob)
        
        # 特殊处理：空调
        has_ac, ac_type = self._get_air_conditioning_info(text_blob)
        features.has_air_conditioning = has_ac
        features.air_conditioning_type = ac_type
        
        # 特殊优化：某些特征的额外逻辑
        self._apply_special_rules(features, text_blob)
        
        return features

    def _apply_special_rules(self, features, text_blob: str):
        """
        应用特殊规则来提高准确性
        """
        # 燃气灶的精确检测
        if hasattr(features, 'has_gas_cooking') and features.has_gas_cooking == 'unknown':
            gas_cooking_patterns = [
                r'gas\s+cook', r'gas\s+stove', r'gas\s+cooktop', 
                r'gas\s+range', r'gas\s+burner', r'gas\s+hob'
            ]
            gas_exclusion_patterns = [
                r'gas\s+heat', r'gas\s+hot\s+water', r'gas\s+fireplace'
            ]
            
            has_cooking = any(re.search(pattern, text_blob) for pattern in gas_cooking_patterns)
            has_exclusion = any(re.search(pattern, text_blob) for pattern in gas_exclusion_patterns)
            
            if has_cooking and not has_exclusion:
                features.has_gas_cooking = 'yes'
            elif has_exclusion and not has_cooking:
                features.has_gas_cooking = 'no'
        
        # 泳池检测增强
        if hasattr(features, 'has_pool') and features.has_pool == 'unknown':
            pool_keywords = ['spa', 'swimming pool', 'pool area', 'resort pool']
            if any(keyword in text_blob for keyword in pool_keywords):
                features.has_pool = 'yes'
        
        # 书房检测增强
        if hasattr(features, 'has_study') and features.has_study == 'unknown':
            study_keywords = ['study', 'office', 'den', 'home office', 'work space', 'workspace']
            if any(keyword in text_blob for keyword in study_keywords):
                features.has_study = 'yes'


# 使用示例和测试
if __name__ == "__main__":
    # 模拟配置数据
    sample_features_config = [
        {
            'column_name': 'has_pool',
            'keywords': ['pool', 'swimming'],
            'negative_keywords': ['no pool', 'pool not available']
        },
        {
            'column_name': 'allows_pets',
            'keywords': ['pet friendly', 'pets allowed'],
            'negative_keywords': ['no pets', 'pets not allowed']
        }
    ]
    
    # 创建提取器实例
    extractor = EnhancedFeatureExtractor(
        features_config=sample_features_config,
        furniture_keywords={},
        aircon_keywords={}
    )
    
    # 测试用例
    test_cases = [
        {
            'description': 'Beautiful apartment with swimming pool and pet friendly policy',
            'expected': {'has_pool': 'yes', 'allows_pets': 'yes'}
        },
        {
            'description': 'Modern unit, no pets allowed, pool facilities available',
            'expected': {'has_pool': 'yes', 'allows_pets': 'no'}
        },
        {
            'description': 'Quiet location, great for professionals',
            'expected': {'has_pool': 'unknown', 'allows_pets': 'unknown'}
        }
    ]
    
    print("Testing Enhanced Feature Extractor:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        features = extractor.extract({}, '', test_case['description'], [])
        result = features.to_dict()
        
        print(f"\nTest Case {i}:")
        print(f"Description: {test_case['description']}")
        print(f"Results: {result}")
        print(f"Expected: {test_case['expected']}")
        
        # 验证结果
        all_correct = True
        for feature, expected_value in test_case['expected'].items():
            if result.get(feature) != expected_value:
                all_correct = False
                print(f"❌ {feature}: got {result.get(feature)}, expected {expected_value}")
        
        if all_correct:
            print("✅ All assertions passed!")
        else:
            print("❌ Some assertions failed!")
