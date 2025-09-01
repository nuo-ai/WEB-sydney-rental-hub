#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
========== 模块说明：房产特征智能提取器 ==========

功能定位：从原始房产数据中自动识别8个核心居住特征
应用场景：悉尼租房平台的数据预处理阶段，将爬虫获取的非结构化数据转换为可查询的结构化特征

核心特征：
1. is_furnished（家具配置）- 两级判断，优先级最高
2. has_air_conditioning（空调）
3. has_laundry（洗衣设备）
4. has_dishwasher（洗碗机）
5. has_gas_cooking（燃气灶）
6. has_intercom（对讲系统）
7. has_study（书房）
8. has_balcony（阳台）

设计理念：V4方案 - 精准度优先，采用两级判断逻辑确保数据质量
"""

import re
import yaml
import logging
from typing import List, Optional, Set, Dict, Any
from pathlib import Path

# 设置模块级日志记录器（方便调试和错误追踪）
logger = logging.getLogger(__name__)

class EnhancedFeatureExtractor:
    """
    ========== 类说明：增强版特征提取器 ==========
    
    职责：智能识别房产的8个核心居住特征
    核心算法：关键词匹配 + 两级判断逻辑
    输出格式：三态值系统（yes/no/unknown）
    
    技术特点：
    1. 配置驱动 - 关键词可通过YAML文件灵活配置
    2. 性能优化 - 使用集合加速关键词查找
    3. 容错设计 - 优雅处理缺失数据和异常情况
    """
    
    def __init__(self):
        """
        ========== 构造函数：初始化特征提取器 ==========
        
        主要任务：
        1. 加载关键词配置文件
        2. 预处理关键词（转小写、构建集合）
        3. 初始化日志系统
        
        调用时机：创建提取器实例时自动执行
        失败处理：配置加载失败时记录错误但不中断，使用空配置继续
        """
        # 加载并预处理关键词（一次性加载，避免重复IO）
        self.config, self.keywords = self._load_keywords()
        logger.info("Enhanced feature extractor (V4 Logic) initialized.")

    def _load_keywords(self) -> tuple[Dict[str, Any], Dict[str, Dict[str, Set[str]]]]:
        """
        ========== 私有方法：加载关键词配置 ==========
        
        功能：从YAML文件读取特征识别关键词
        
        返回值：
        - config_data: 原始配置字典（保留用于调试）
        - processed_keywords: 处理后的关键词集合（性能优化版）
        
        数据结构示例：
        {
            'furnished': {
                'positive': {'furnished', 'fully furnished'},
                'negative': {'unfurnished', 'no furniture'},
                'optional': {'partly furnished'}
            }
        }
        """
        # 构建配置文件路径（相对路径转绝对路径，跨平台兼容）
        config_path = Path(__file__).parent / 'config' / 'property_features_keywords.yaml'
        
        # 步骤1：检查文件是否存在（防御性编程）
        if not config_path.exists():
            logger.error(f"CRITICAL: Keywords config file not found at {config_path}")
            return {}, {}  # 返回空配置而非抛异常（保证系统可用性）
        
        try:
            # 步骤2：读取YAML文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)  # safe_load防止代码注入
            
            # 步骤3：预处理关键词（性能优化关键）
            processed_keywords = {}
            for feature, types in config_data.items():
                processed_keywords[feature] = {}
                for key_type, words in types.items():
                    # 转换为小写集合：O(1)查找速度 + 不区分大小写
                    processed_keywords[feature][key_type] = {
                        str(word).lower() for word in words
                    } if words else set()
            
            return config_data, processed_keywords
            
        except Exception as e:
            # 记录详细错误但不崩溃（容错设计）
            logger.error(f"Failed to load or process keywords config: {e}")
            return {}, {}

    def _check_list_for_feature(self, feature_name: str, feature_list: List[str]) -> str:
        """
        ========== 核心方法：列表特征检查 ==========
        
        功能：在房产官方特征列表中查找指定特征
        
        参数：
        - feature_name: 特征名称（如'furnished', 'air_conditioning'）
        - feature_list: 房产网站提供的官方特征列表
        
        返回值：
        - 'yes': 确认有此特征
        - 'no': 确认无此特征
        - 'unknown': 无法判断
        
        判断逻辑：
        1. 负面关键词优先级最高（如找到"unfurnished"直接返回no）
        2. 正面关键词次之
        3. 都没找到返回unknown
        
        示例：
        feature_list = ['Furnished', 'Air Conditioning']
        result = _check_list_for_feature('furnished', feature_list)
        # 返回 'yes'
        """
        # 防御检查：确保配置存在
        if not self.keywords.get(feature_name):
            return 'unknown'

        # 获取正负关键词集合（默认空集合防止None错误）
        positive_kws = self.keywords[feature_name].get('positive', set())
        negative_kws = self.keywords[feature_name].get('negative', set())
        
        # 将列表转为小写集合（统一格式 + O(1)查找）
        feature_set = {item.lower().strip() for item in feature_list}

        # 判断优先级：negative > positive
        # 为什么负面优先：明确说"无"比暗示"有"更可靠
        if not negative_kws.isdisjoint(feature_set):  # 集合有交集
            return 'no'
        
        if not positive_kws.isdisjoint(feature_set):
            return 'yes'
            
        return 'unknown'

    def _check_text_for_feature(self, feature_name: str, text_blob: str) -> str:
        """
        ========== 核心方法：文本特征检查 ==========
        
        功能：在标题和描述文本中搜索特征关键词
        应用场景：当官方特征列表无法判断时的备选方案
        
        参数：
        - feature_name: 特征名称
        - text_blob: 合并后的文本（标题+描述）
        
        返回值：
        - 'yes': 文本明确提到有此特征
        - 'no': 文本明确提到无此特征  
        - 'optional': 部分配置（仅用于家具）
        - 'unknown': 文本中未提及
        
        三级优先级设计：
        1. negative最高 - "no pets"比"pet-friendly"更明确
        2. optional次之 - "partly furnished"的特殊状态
        3. positive最低 - 避免误判
        
        性能考虑：
        使用"in"操作符而非正则（快10倍），适合高频调用
        """
        # 前置检查：无配置或空文本直接返回
        if not self.keywords.get(feature_name) or not text_blob:
            logger.debug(f"[{feature_name}] 文本为空或配置缺失，返回 unknown")
            return 'unknown'

        # 获取三类关键词集合
        positive_kws = self.keywords[feature_name].get('positive', set())
        negative_kws = self.keywords[feature_name].get('negative', set())
        optional_kws = self.keywords[feature_name].get('optional', set())  # 仅furnished使用
        
        # 文本预处理：转小写（匹配不区分大小写）
        text_lower = text_blob.lower()
        
        # 调试日志：帮助分析匹配过程（生产环境可关闭）
        logger.debug(f"[{feature_name}] 检查文本: {text_lower[:100]}...")
        logger.debug(f"[{feature_name}] 正面关键词: {positive_kws}")
        logger.debug(f"[{feature_name}] 负面关键词: {negative_kws}")
        logger.debug(f"[{feature_name}] 可选关键词: {optional_kws}")

        # 三级判断逻辑（顺序很重要！）
        
        # 级别1：否定关键词（最高优先级）
        # 为什么：房东明确说"无"比暗示"有"更可信
        if negative_kws and any(kw in text_lower for kw in negative_kws):
            found_neg_kw = next(kw for kw in negative_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到负面关键词 '{found_neg_kw}'，返回 no")
            return 'no'
        
        # 级别2：可选关键词（仅家具特征使用）
        # 为什么："partly furnished"是特殊状态，需单独处理
        if optional_kws and any(kw in text_lower for kw in optional_kws):
            found_opt_kw = next(kw for kw in optional_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到可选关键词 '{found_opt_kw}'，返回 optional")
            return 'optional'

        # 级别3：肯定关键词
        if positive_kws and any(kw in text_lower for kw in positive_kws):
            found_pos_kw = next(kw for kw in positive_kws if kw in text_lower)
            logger.debug(f"[{feature_name}] 找到正面关键词 '{found_pos_kw}'，返回 yes")
            return 'yes'
            
        # 未找到任何关键词
        logger.debug(f"[{feature_name}] 未找到任何关键词，返回 unknown")
        return 'unknown'

    def extract_features(self, property_features_list: List[str], headline: str, description: str) -> Dict[str, Any]:
        """
        ========== 主入口：批量提取房产特征 ==========
        
        功能：从房产数据中提取8个核心居住特征
        
        参数：
        - property_features_list: 网站提供的官方特征列表
        - headline: 房源标题
        - description: 房源描述文本
        
        返回值：
        字典格式，包含8个特征的判断结果：
        {
            'is_furnished': 'yes'/'no'/'unknown',
            'has_air_conditioning': 'yes'/'no'/'unknown',
            'has_laundry': 'yes'/'no'/'unknown',
            ...
        }
        
        V4方案核心逻辑：
        - is_furnished: 两级判断（列表优先，文本备选）
        - 其他7个特征: 仅基于官方列表判断
        
        设计原因：
        1. 家具是租客最关心的特征，需要更高准确率
        2. 官方列表更可靠，文本可能有歧义
        3. 两级判断平衡了准确性和覆盖率
        
        调用示例：
        extractor = EnhancedFeatureExtractor()
        features = extractor.extract_features(
            ['Furnished', 'Air Conditioning'],
            'Modern 2BR Apartment',
            'Fully furnished with all amenities...'
        )
        """
        # 调试日志：记录输入数据（便于问题排查）
        logger.debug(f"=== 开始特征提取 ===")
        logger.debug(f"Property Features List: {property_features_list}")
        logger.debug(f"Headline: {headline[:100] if headline else 'Empty'}...")
        logger.debug(f"Description: {description[:100] if description else 'Empty'}...")
        
        # 初始化结果字典
        extracted_data = {}

        # ========== 阶段1：处理is_furnished（两级判断） ==========
        logger.debug(f"=== 处理 is_furnished ===")
        
        # 第一优先级：检查官方特征列表
        # 为什么优先：网站标注的特征最准确可靠
        furnish_status_from_list = self._check_list_for_feature('furnished', property_features_list)
        logger.debug(f"从列表检查结果: {furnish_status_from_list}")
        
        if furnish_status_from_list != 'unknown':
            # 官方列表有明确结果，直接使用
            extracted_data['is_furnished'] = furnish_status_from_list
            logger.debug(f"使用列表检查结果: {furnish_status_from_list}")
        else:
            # 第二优先级：从文本中查找
            # 为什么需要：增加覆盖率，部分房源列表不完整
            text_blob = (headline + ' ' + description)  # 合并文本增加匹配机会
            logger.debug(f"进入文本检查，合并文本长度: {len(text_blob)}")
            
            furnish_status_from_text = self._check_text_for_feature('furnished', text_blob)
            logger.debug(f"文本检查结果: {furnish_status_from_text}")
            
            # 特殊处理：'optional'（部分家具）映射为'yes'
            # 业务逻辑：对租客来说，部分家具也算有家具
            if furnish_status_from_text == 'optional':
                extracted_data['is_furnished'] = 'yes'
                logger.debug(f"将 'optional' 映射为 'yes'")
            else:
                extracted_data['is_furnished'] = furnish_status_from_text
                logger.debug(f"使用文本检查结果: {furnish_status_from_text}")

        # ========== 阶段2：处理其他7个特征（仅列表判断） ==========
        logger.debug(f"=== 处理其他特征 ===")
        
        # 定义其他7个核心特征
        # 为什么不检查文本：这些特征在列表中已足够准确，文本易误判
        other_features = [
            'air_conditioning',  # 空调
            'laundry',          # 洗衣设备
            'dishwasher',       # 洗碗机
            'gas_cooking',      # 燃气灶
            'intercom',         # 对讲系统
            'study',            # 书房
            'balcony'           # 阳台
        ]
        
        # 批量处理：统一的判断逻辑
        for feature in other_features:
            column_name = f"has_{feature}"  # 数据库字段名格式
            result = self._check_list_for_feature(feature, property_features_list)
            extracted_data[column_name] = result
            logger.debug(f"{column_name}: {result}")

        logger.debug(f"=== 特征提取完成，最终结果: {extracted_data} ===")
        return extracted_data
