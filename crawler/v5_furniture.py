#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
房产数据爬虫脚本 - v2 (for Web UI integration)
- Reads URLs from config/temp_urls.txt if present, otherwise config/url.txt.
- Outputs to a timestamped CSV file.
- Prints the output CSV filename to stdout.
"""

import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Set, Any, Type
from dataclasses import dataclass, field, fields, make_dataclass
from functools import wraps
import threading
import re
import yaml
import random
import gc
import sys # Added for printing to stdout
import subprocess

# --- 关键修复：强制stdout使用UTF-8编码，解决Windows下print中文的UnicodeEncodeError ---
# 使用io.TextIOWrapper来确保跨平台的类型兼容性，并解决Pylance的 "reconfigure" 警告
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from lxml import etree # type: ignore

# 导入增强版特征提取器
from enhanced_feature_extractor import EnhancedFeatureExtractor

# =============================================================================
# 项目路径配置
# =============================================================================
CRAWLER_DIR = Path(__file__).parent
PROJECT_ROOT = CRAWLER_DIR.parent
LOG_DIR = PROJECT_ROOT / 'logs'
CONFIG_DIR = CRAWLER_DIR / 'config'
OUTPUT_DIR = CRAWLER_DIR / 'output'
DATA_DIR = OUTPUT_DIR / 'data'

for d_path in (LOG_DIR, CONFIG_DIR, OUTPUT_DIR, DATA_DIR):
    d_path.mkdir(exist_ok=True)

# =============================================================================
# 日志配置
# =============================================================================
def setup_logger(name: str = 'domain_crawler_v2') -> logging.Logger: # Changed logger name
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(logging.DEBUG)
    if logger_instance.handlers:
        return logger_instance
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    log_file = LOG_DIR / f"domain_crawler_v2_{datetime.now():%Y%m%d_%H%M%S}.log" # Changed log file name
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger_instance.addHandler(ch)
    logger_instance.addHandler(fh)
    return logger_instance

logger = setup_logger()

# =============================================================================
# 配置加载
# =============================================================================
def load_config() -> dict:
    config_path = CONFIG_DIR / 'crawler_config.yaml'
    if not config_path.exists():
        default_config_content = {
            'network': {'max_retries': 3, 'backoff_factor': 0.5, 'retry_statuses': [500, 502, 503, 504], 'timeout': 20},
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'},
            'performance': {'requests_per_second': 1.5, 'batch_size': 50, 'results_per_page_threshold': 10,
                            'delay_min': 0.8, 'delay_max': 2.2, 'page_delay_min': 2.0, 'page_delay_max': 3.5,
                            'inter_url_delay_min': 3.0, 'inter_url_delay_max': 7.0},
            'features': {'enable_advanced_features': True, 'enable_data_validation': True, 'enable_batch_write': True, 'from_property_features_list': True, 'preserve_description_format': True, 'translate_to_chinese': False}
        }
        try:
            with open(config_path, 'w', encoding='utf-8') as f_default_config:
                yaml.dump(default_config_content, f_default_config, default_flow_style=False)
            logger.info(f"Default configuration file created at {config_path}. Please review it.")
        except Exception as e_cfg:
            logger.error(f"Configuration file not found: {config_path} and failed to create a default: {e_cfg}")
            raise FileNotFoundError(f"配置文件不存在: {config_path} and failed to create a default: {e_cfg}")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
# FURNITURE_KEYWORDS is no longer needed here, it's handled by the extractor.

# =============================================================================
# 辅助函数 - 从URL提取区域名称
# =============================================================================
def extract_region_from_url(url: str) -> str:
    """
    从Domain搜索URL中提取区域名称
    支持多种URL格式：
    - 单个区域: /rent/sydney-nsw-2000/
    - 多个区域: /rent/sydney-nsw-2000+parramatta-nsw-2150/
    - 带其他参数的URL
    """
    try:
        # 使用正则表达式提取区域部分
        # 匹配 /rent/ 后面到 ? 或 / 之前的部分
        pattern = r'/rent/([^/?]+)'
        match = re.search(pattern, url)
        
        if match:
            region_part = match.group(1)
            
            # 处理多个区域的情况（用+连接）
            if '+' in region_part:
                # 取第一个区域作为主要区域
                regions = region_part.split('+')
                main_region = regions[0]
                # 提取区域名称（去掉州和邮编）
                region_name = main_region.split('-')[0].replace('-', ' ').title()
                return f"{region_name}_Multi" # 标记为多区域
            else:
                # 单个区域，提取区域名称
                region_name = region_part.split('-')[0].replace('-', ' ').title()
                return region_name
        else:
            # 如果无法匹配，返回默认值
            return "Unknown_Region"
            
    except Exception as e:
        logger.warning(f"Failed to extract region from URL {url}: {e}")
        return "Unknown_Region"

# =============================================================================
# 数据模型 (V4 Refactor)
# =============================================================================
@dataclass
class PropertyData:
    listing_id: str = ""
    property_url: str = ""
    address: str = ""
    suburb: str = ""
    state: str = ""
    postcode: str = ""
    property_type: str = ""
    rent_pw: float = 0.0
    bond: float = 0.0
    bedrooms: int = 0
    bathrooms: int = 0
    parking_spaces: int = 0
    bedroom_display: str = ""
    available_date: str = ""
    inspection_times: List[str] = field(default_factory=list)
    agency_name: str = ""
    agent_name: str = ""
    cover_image: str = ""
    agent_phone: str = ""
    agent_email: str = ""
    property_headline: str = ""
    property_description: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    images: str = ""
    property_features: str = "" # Storing raw feature list as JSON string
    agent_profile_url: str = ""
    agent_logo_url: str = ""
    enquiry_form_action: str = ""

    # V4 Refactor: Add specific feature columns
    is_furnished: str = "unknown"
    has_air_conditioning: str = "unknown"
    has_laundry: str = "unknown"
    has_dishwasher: str = "unknown"
    has_gas_cooking: str = "unknown"
    has_intercom: str = "unknown"
    has_study: str = "unknown"
    has_balcony: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass to a dictionary for DataFrame conversion."""
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if f.name == 'inspection_times':
                result[f.name] = '; '.join(value)
            else:
                result[f.name] = value
        return result

def get_expected_columns() -> List[str]:
    """Returns a static list of expected columns for the output file."""
    return [f.name for f in fields(PropertyData)] + ['image_1', 'image_2', 'image_3', 'image_4']

EXPECTED_COLUMNS = get_expected_columns()

# =============================================================================
# 数据清洗 & 验证
# =============================================================================
class DataCleaner:
    @staticmethod
    def clean_price(price: str) -> float:
        if not price: return 0.0
        try: return float(re.sub(r'[^\d.]', '', price))
        except (ValueError, TypeError): return 0.0
    
    @staticmethod
    def clean_available_date(date_str: str) -> str:
        """
        专门处理入住日期的智能清理
        将过期日期转换为 'Available Now'，保留未来日期
        """
        if not date_str: 
            return "Available Now"
        
        try:
            if 'T' in date_str: 
                date_str = date_str.split('T')[0]
            
            if any(keyword in date_str.upper() for keyword in ['NOW', 'AVAILABLE', 'IMMEDIATE']):
                return "Available Now"
            
            parsed_date = None
            patterns = ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%Y-%m-%d %H:%M:%S']
            
            for pattern in patterns:
                try:
                    parsed_date = datetime.strptime(date_str, pattern)
                    break
                except ValueError:
                    continue
            
            if parsed_date:
                today = datetime.now().date()
                available_date = parsed_date.date()
                
                if available_date <= today:
                    logger.debug(f"过期入住日期 {date_str} 转换为 'Available Now'")
                    return "Available Now"
                else:
                    return available_date.strftime('%Y-%m-%d')
            else:
                date_lower = date_str.lower().strip()
                if any(word in date_lower for word in ['now', 'immediate', 'available', 'asap']):
                    return "Available Now"
                else:
                    logger.debug(f"无法解析日期格式 '{date_str}'，默认为 'Available Now'")
                    return "Available Now"
                    
        except Exception as e:
            logger.debug(f"处理入住日期 '{date_str}' 时出错: {e}，默认为 'Available Now'")
            return "Available Now"

    @staticmethod
    def clean_text(text: str) -> str:
        if not text: return ""
        text = re.sub(r'<[^>]+>', '', text); text = ' '.join(text.split())
        return text.strip()
    
    @staticmethod
    def clean_description(text: str, preserve_format: bool = True) -> str:
        """
        专门用于清理房源描述的方法
        可以选择保留格式或进行传统的文本清理
        """
        if not text: return ""
        
        if preserve_format:
            text = re.sub(r'<br\s*/?>', '\n', text)
            text = re.sub(r'</p>\s*<p[^>]*>', '\n\n', text)
            text = re.sub(r'<p[^>]*>', '', text)
            text = re.sub(r'</p>', '\n', text)
            text = re.sub(r'<li[^>]*>', '• ', text)
            text = re.sub(r'</li>', '\n', text)
            text = re.sub(r'</?[uo]l[^>]*>', '\n', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'[ \t]+', ' ', text)
            text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
            text = re.sub(r'^\s+|\s+$', '', text)
            return text.strip()
        else:
            return DataCleaner.clean_text(text)

class DataValidator:
    @staticmethod
    def validate_property(data: PropertyData) -> Tuple[bool, List[str]]:
        errors = []
        if not data.listing_id: errors.append("缺少listing_id")
        if not data.property_url: errors.append("缺少property_url")
        if data.rent_pw < 0: errors.append("rent_pw不能为负数")
        if data.bedrooms < 0: errors.append("bedrooms不能为负数")
        if data.bathrooms < 0: errors.append("bathrooms不能为负数")
        if data.latitude and not (-90 <= data.latitude <= 90): errors.append("latitude超出有效范围")
        if data.longitude and not (-180 <= data.longitude <= 180): errors.append("longitude超出有效范围")
        return not errors, errors

# =============================================================================
# 请求管理
# =============================================================================
def safe_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = CONFIG['network']['max_retries']
        backoff_factor = CONFIG['network']['backoff_factor']
        last_exception = None
        for i_retry in range(retries):
            try: return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                last_exception = e
                if i_retry < retries - 1:
                    wait_time = (2 ** i_retry) * backoff_factor
                    logger.warning(f"请求失败 ({i_retry+1}/{retries})，{wait_time:.1f}s后重试: {e}"); time.sleep(wait_time)
        logger.error(f"请求失败，已达到最大重试次数: {last_exception if last_exception else 'Unknown Error'}");
        if last_exception: raise last_exception
        raise RuntimeError("Request failed after max retries, no exception stored.")
    return wrapper

class RequestManager:
    def __init__(self):
        self.session = self._create_session(); self.last_request_time = 0; self._lock = threading.Lock()
    def _create_session(self) -> requests.Session:
        s = requests.Session()
        rs = Retry(total=CONFIG['network']['max_retries'], backoff_factor=CONFIG['network']['backoff_factor'], status_forcelist=CONFIG['network']['retry_statuses'])
        a = HTTPAdapter(max_retries=rs); s.mount("http://", a); s.mount("https://", a)
        s.headers.update(CONFIG['headers']); return s
    def _wait_for_rate_limit(self):
        with self._lock:
            current_time = time.time(); elapsed = current_time - self.last_request_time
            base_delay = 1.0 / CONFIG['performance']['requests_per_second']
            random_delay_factor = CONFIG['performance'].get('random_delay_factor', 0.5)
            random_delay = random.uniform(0, base_delay * random_delay_factor)
            wait_time = base_delay + random_delay - elapsed
            if wait_time > 0: time.sleep(wait_time)
            self.last_request_time = time.time()
    @safe_request
    def get(self, url: str, **kwargs) -> requests.Response:
        try:
            self._wait_for_rate_limit()
            resp = self.session.get(url, timeout=CONFIG['network']['timeout'], **kwargs)
            resp.raise_for_status()
            if not resp.content: raise requests.exceptions.RequestException("空响应内容")
            ct = resp.headers.get('content-type', '')
            if not ('text/html' in ct or 'application/json' in ct):
                raise requests.exceptions.RequestException(f"意外的响应类型: {ct}")
            return resp
        except requests.Timeout as e_timeout: logger.error(f"请求超时: {url}"); raise e_timeout
        except requests.HTTPError as e_http: logger.error(f"HTTP错误: {url}, 状态码: {e_http.response.status_code}"); raise e_http
        except requests.exceptions.RequestException as e_req: logger.error(f"请求异常: {url}, 错误: {e_req}"); raise e_req
        except Exception as e_generic: logger.error(f"未预期的错误 during GET: {url}, 错误: {e_generic}"); raise e_generic

# =============================================================================
# 批量写入管理
# =============================================================================
class BatchWriter:
    def __init__(self):
        self.buffer: List[PropertyData] = []; self._lock = threading.Lock()
    def add(self, item: PropertyData) -> None:
        with self._lock: self.buffer.append(item)
    def flush(self, region: str = "Unknown", total_count: int = 0, output_format: str = 'xlsx') -> Optional[str]:
        if not self.buffer:
            logger.info(f"缓冲区中无数据可刷新至 {output_format.upper()}。")
            return None
        with self._lock:
            try:
                data_dicts = [item.to_dict() for item in self.buffer]
                temp_df = pd.DataFrame(data_dicts)
                df_final = pd.DataFrame(columns=EXPECTED_COLUMNS)
                for col in EXPECTED_COLUMNS:
                    if col in temp_df.columns:
                        df_final[col] = temp_df[col]
                    else:
                        df_final[col] = "" 
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                clean_region = re.sub(r'[^\w\s-]', '', region).replace(' ', '_')

                if output_format.lower() == 'csv':
                    output_filename = f"{timestamp}_{clean_region}_{total_count}properties.csv"
                    output_file_path = OUTPUT_DIR / output_filename
                    df_final.to_csv(output_file_path, index=False, encoding='utf-8-sig')
                else:
                    output_filename = f"{timestamp}_{clean_region}_{total_count}properties.xlsx"
                    output_file_path = OUTPUT_DIR / output_filename
                    df_final.to_excel(output_file_path, index=False, engine='openpyxl')

                logger.info(f"已成功保存 {len(df_final)} 条记录到: {output_file_path} (区域: {region}, 总房源数: {total_count})")
                self.buffer = []
                return str(output_file_path)
            except Exception as e:
                logger.error(f"写入 {output_format.upper()} 文件 ({output_filename if 'output_filename' in locals() else 'unknown'}) 失败: {e}", exc_info=True)
                return None

# =============================================================================
# 爬虫核心
# =============================================================================
class DomainCrawler:
    def __init__(self):
        self.request_manager = RequestManager()
        self.feature_extractor = EnhancedFeatureExtractor()
        self.data_cleaner = DataCleaner()
        self.data_validator = DataValidator()
        self.batch_writer = BatchWriter()
        self._lock = threading.Lock()
    
    def _extract_inspection_times(self, document: etree._Element) -> List[str]:
        times = []
        for b in document.xpath('//div[@data-testid="listing-details__inspections-block"]'):
            try:
                d_el = b.xpath('.//span[@data-testid="listing-details__inspections-block-day"]/text()')
                t_el = b.xpath('.//span[@data-testid="listing-details__inspections-block-time"]/text()')
                if d_el and t_el: times.append(f"{d_el[0].strip()}, {t_el[0].strip()}")
            except Exception as e: logger.debug(f"_extract_inspection_times method 1 error: {e}")
        if not times:
            try:
                js_txt = "".join(document.xpath(".//script[@id='__NEXT_DATA__']/text()"))
                if js_txt:
                    js_data = json.loads(js_txt)
                    props = js_data.get("props", {}).get("pageProps", {}).get("componentProps", {})
                    for i_item in props.get("inspectionDetails", {}).get("inspections", []):
                        st, et = i_item.get("startTime", ""), i_item.get("endTime", "")
                        if st and et: times.append(f"{st} - {et}")
            except Exception as e: logger.debug(f"_extract_inspection_times method 2 error: {e}")
        return times
    
    def _generate_bedroom_display(self, bedrooms: int, property_type: str, 
                                  property_features: List[str], headline: str, 
                                  description: str) -> str:
        if bedrooms > 0:
            return str(bedrooms)
        
        text_sources = [
            property_type.lower() if property_type else "",
            headline.lower() if headline else "",
            description.lower() if description else "",
            " ".join(property_features).lower() if property_features else ""
        ]
        
        studio_keywords = ["studio", "studios", "studio apartment", "studio unit", "open plan", "efficiency apartment"]
        
        for text in text_sources:
            if text and any(keyword in text for keyword in studio_keywords):
                logger.debug(f"检测到Studio关键词在: {text[:50]}...")
                return "Studio"
        
        logger.debug(f"卧室数为0但未找到Studio关键词，默认返回Studio")
        return "Studio"
    
    def crawl_detail(self, house_href: str) -> Optional[PropertyData]:
        try:
            logger.info(f"正在抓取详情页: {house_href}")
            response = self.request_manager.get(house_href)
            if not response: return None
            house_document = etree.HTML(response.text)
            
            try:
                json_script = "".join(house_document.xpath(".//script[@id='__NEXT_DATA__']/text()"))
                if not json_script: logger.error(f"__NEXT_DATA__ script tag not found: {house_href}"); return None
                base_json = json.loads(json_script)
            except Exception as e: logger.error(f"解析详情页JSON失败 for {house_href}: {e}", exc_info=True); return None
            
            comp_props = base_json.get("props", {}).get("pageProps", {}).get("componentProps", {})
            root_q = comp_props.get("rootGraphQuery", {}).get("listingByIdV2", {}) or {}
            list_sum = comp_props.get("listingSummary", {}) or {}
            agents_list = root_q.get("agents", []); agent_p = agents_list[0] if agents_list else {}
            addr_info = root_q.get("displayableAddress", {}) or {}; geo_info = addr_info.get("geolocation", {}) or {}
            
            prop_feat_els = house_document.xpath("//div[@id='property-features']//li")
            prop_feat_list = [li.xpath("string(.)").strip() for li in prop_feat_els if li.xpath("string(.)")]
            
            # V4 Refactor: Call the new feature extractor
            headline_text = root_q.get("headline", "")
            description_text = root_q.get("description", "")
            extracted_features = self.feature_extractor.extract_features(prop_feat_list, headline_text, description_text)
            
            img_urls_raw = [img.get("url", "") for img in root_q.get("largeMedia", []) if img.get("url")]
            images_json = json.dumps(img_urls_raw)
            
            cover_image_val = img_urls_raw[0] if img_urls_raw else ""
            property_features_json = json.dumps(prop_feat_list) # Store the raw list

            enquiry_form_action = ""
            apply_link_el = house_document.xpath('//div[@data-testid="listing-details__agent-details-cta-box"]//a[contains(@href, "snug.com") or contains(@href, "2apply.com.au")]/@href')
            if apply_link_el:
                enquiry_form_action = apply_link_el[0].strip()
            
            if not enquiry_form_action:
                oneform_action_el = house_document.xpath('//div[@data-testid="listing-details__agent-details-cta-box"]//form[@data-testid="listing-details__oneform-button-form"]/@action')
                if not oneform_action_el:
                    oneform_action_el = house_document.xpath('//div[@data-testid="listing-details__agent-details-cta-box"]//form[contains(@class, "css-")]/@action')
                if oneform_action_el:
                    enquiry_form_action = oneform_action_el[0].strip()
            
            if not enquiry_form_action:
                original_enquiry_el = house_document.xpath("//form[@id='enquiry-form']/@action")
                if original_enquiry_el:
                    enquiry_form_action = original_enquiry_el[0].strip()

            property_type_val = root_q.get("propertyType", "")
            if not property_type_val:
                property_type_elements = house_document.xpath('//span[@class="css-1efi8gv"]/text()')
                if property_type_elements:
                    property_type_val = property_type_elements[0].strip()

            agent_phone_val = agent_p.get("phoneNumber", "")
            if not agent_phone_val or agent_phone_val.strip().lower() == "call" or not agent_phone_val.strip():
                agent_phone_href_el = house_document.xpath('//a[@data-testid="listing-details__phone-cta-button"]/@href')
                if agent_phone_href_el and agent_phone_href_el[0].startswith("tel:"):
                    agent_phone_val = agent_phone_href_el[0].replace("tel:", "").strip()
                else:
                    agent_phone_el_text = house_document.xpath('//a[@data-testid="listing-details__phone-cta-button"]/span[@class="css-1s26z8e"]/span/text()')
                    if agent_phone_el_text:
                         agent_phone_val = agent_phone_el_text[0].strip()

            agent_logo_url_val = (agent_p.get("agency", {}) or {}).get("logoUrl", "") 
            if not agent_logo_url_val:
                agent_logo_el = house_document.xpath('//a[@class="css-wrjy08"]/img[@data-testid="listing-details__agent-details-branding-lazy"]/@src')
                if agent_logo_el:
                    agent_logo_url_val = agent_logo_el[0].strip()

            bedrooms_raw = list_sum.get("beds", 0)
            bedroom_display_val = self._generate_bedroom_display(
                bedrooms_raw, property_type_val, prop_feat_list, headline_text, description_text
            )

            data_item = PropertyData(
                listing_id=root_q.get("listingId", ""), property_url=house_href,
                address=self.data_cleaner.clean_text(list_sum.get("address", "")),
                suburb=addr_info.get("suburbName", ""), state=addr_info.get("state", ""),
                postcode=addr_info.get("postcode", ""),
                property_type=property_type_val,
                rent_pw=self.data_cleaner.clean_price(list_sum.get("title", "")),
                bond=self.data_cleaner.clean_price(str((root_q.get("priceDetails", {}) or {}).get("bond", 0))),
                bedrooms=bedrooms_raw, bathrooms=list_sum.get("baths", 0),
                parking_spaces=list_sum.get("parking", 0),
                bedroom_display=bedroom_display_val,
                available_date=self.data_cleaner.clean_available_date((root_q.get("dateAvailableV2", {}) or {}).get("isoDate", "")),
                inspection_times=self._extract_inspection_times(house_document),
                agency_name=(root_q.get("agency", {}) or {}).get("name", ""),
                agent_name=agent_p.get("fullName", ""), 
                cover_image=cover_image_val,
                agent_phone=agent_phone_val, 
                agent_email=agent_p.get("email", ""),
                agent_profile_url=agent_p.get("profileUrl", ""),
                agent_logo_url=agent_logo_url_val, 
                property_headline=headline_text,
                property_description=self.data_cleaner.clean_description(
                    description_text, 
                    preserve_format=CONFIG['features'].get('preserve_description_format', True)
                ),
                latitude=float(geo_info.get("latitude", 0.0) or 0.0),
                longitude=float(geo_info.get("longitude", 0.0) or 0.0),
                images=images_json, 
                property_features=property_features_json,
                enquiry_form_action=enquiry_form_action,
                # V4 Refactor: Add extracted features directly
                **extracted_features
            )
            
            if CONFIG['features'].get('enable_data_validation', False):
                is_valid, errors = self.data_validator.validate_property(data_item)
                if not is_valid: logger.warning(f"数据验证失败 for {house_href}: {errors}")
            
            logger.info(f"成功提取房源信息: ID={data_item.listing_id or 'N/A'} for URL: {house_href}")
            if CONFIG['features']['enable_batch_write']: self.batch_writer.add(data_item)
            return data_item
        except Exception as e:
            logger.error(f"抓取详情页失败: {house_href}", exc_info=True); return None
    
    def process_search_page(self, url: str) -> List[str]:
        try:
            resp = self.request_manager.get(url)
            if not resp: return []
            doc = etree.HTML(resp.text)
            links = []
            common_link_pattern = doc.xpath(".//ul[@data-testid='results']/li//a[contains(@href, 'www.domain.com.au') and string-length(@href) > 40]/@href")

            if common_link_pattern:
                links = [link for link in common_link_pattern if link.startswith("https://www.domain.com.au/")]
            
            if not links:
                listing_items_xpath = ".//ul[@data-testid='results']/li"
                link_xpath_inside_item = ".//a[contains(@class, 'address') or @data-testid='listing-card-link' or contains(@href,'/1')]/@href"
                for item_element in doc.xpath(listing_items_xpath):
                    href_list = item_element.xpath(link_xpath_inside_item)
                    if not href_list: href_list = item_element.xpath(".//div[@class='css-qrqvvg']/a/@href")
                    if not href_list: href_list = item_element.xpath("(.//a[contains(@href,'www.domain.com.au')])[1]/@href")

                    if href_list:
                        link_candidate = href_list[0]
                        if link_candidate.startswith("/"): link_candidate = "https://www.domain.com.au" + link_candidate
                        if link_candidate.startswith("https://www.domain.com.au/"): links.append(link_candidate)
            
            if not links: logger.warning(f"在页面 {url} 上未找到房源链接，请检查XPath选择器。")
            return list(set(links))
        except Exception as e: logger.error(f"处理搜索页面失败: {url}", exc_info=True); return []
    
    def save_progress(self, url: str, page: int, progress_file_name: str) -> None:
        try:
            prog = {"url": url, "page": page, "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            with open(PROJECT_ROOT / progress_file_name, 'w', encoding='utf-8') as f: json.dump(prog, f, indent=2)
            logger.debug(f"保存进度到 {progress_file_name}: URL={url}, 页码={page}")
        except Exception as e: logger.error(f"保存进度到 {progress_file_name} 失败: {e}")
    
    def load_progress(self, progress_file_name: str) -> Optional[dict]:
        try:
            p_file = PROJECT_ROOT / progress_file_name
            if p_file.exists():
                with open(p_file, 'r', encoding='utf-8') as f: prog = json.load(f)
                logger.info(f"从 {progress_file_name} 加载到上次进度: {prog.get('url','N/A')}, 页码 {prog.get('page','N/A')}"); return prog
        except Exception as e: logger.error(f"从 {progress_file_name} 加载进度失败: {e}"); return None
    
    def search(self, input_url: str, using_temp_urls: bool) -> int:
        page = 1
        total_links_processed = 0
        progress_file_name = "progress_temp.json" if using_temp_urls else "progress.json"
        
        res_thresh = CONFIG.get('performance', {}).get('results_per_page_threshold', 10)
        delay_min = CONFIG.get('performance', {}).get('delay_min', 0.8)
        delay_max = CONFIG.get('performance', {}).get('delay_max', 2.2)
        page_delay_min = CONFIG.get('performance', {}).get('page_delay_min',2.0)
        page_delay_max = CONFIG.get('performance', {}).get('page_delay_max',3.5)

        while True:
            # 修正 3: 正确地构造分页 URL
            if '?' in input_url:
                s_url = f"{input_url}&page={page}"
            else:
                if not input_url.endswith('/'):
                    input_url += '/'
                s_url = f"{input_url}?page={page}"

            logger.info(f"正在抓取第{page}页: {s_url}")
            links = self.process_search_page(s_url)
            if not links: 
                logger.info(f"第 {page} 页无房源链接或已达末页, 结束对 {input_url} 搜索.")
                break
            
            logger.info(f"第{page}页找到{len(links)}个房源"); succ_count = 0
            total_links_processed += len(links)
            for i_idx, detail_url in enumerate(links):
                try:
                    logger.info(f"处理第{i_idx+1}/{len(links)}个房源: {detail_url}")
                    if self.crawl_detail(detail_url): succ_count += 1
                    time.sleep(random.uniform(delay_min, delay_max))
                except Exception as e: logger.error(f"处理房源 {detail_url} 失败: {e}", exc_info=True); time.sleep(5.0)
            
            logger.info(f"本页成功处理{succ_count}/{len(links)}个房源")
            
            if not using_temp_urls:
                self.save_progress(input_url, page + 1, progress_file_name)

            if page % 5 == 0: gc.collect(); logger.info("执行内存回收")
            
            if len(links) < res_thresh : 
                logger.info(f"当前页房源数 ({len(links)}) < 阈值 ({res_thresh})，判断为最后一页.")
                break
            
            logger.info(f"完成第{page}页处理"); page += 1
            time.sleep(random.uniform(page_delay_min, page_delay_max))
        
        logger.info(f"搜索完成，总共找到 {len(links)} 个房源链接")
        return total_links_processed
    
    def run(self) -> List[str]:
        output_files = []
        all_properties_buffer = []
        output_mode = CONFIG.get('output', {}).get('mode', 'per_url')
        combined_prefix = CONFIG.get('output', {}).get('single_file_prefix', 'Combined')

        try:
            logger.info("开始运行房源信息采集程序 (v2)...")
            
            temp_url_file = CONFIG_DIR / 'temp_urls.txt'
            default_url_file = CONFIG_DIR / 'url.txt'
            using_temp_urls = False

            if temp_url_file.exists() and temp_url_file.stat().st_size > 0:
                url_cfg_path = temp_url_file
                using_temp_urls = True
                logger.info(f"检测到临时URL文件: {url_cfg_path}")
                temp_progress_file = PROJECT_ROOT / "progress_temp.json"
                if temp_progress_file.exists():
                    try: temp_progress_file.unlink()
                    except OSError as e: logger.warning(f"无法删除临时进度文件 {temp_progress_file}: {e}")

            elif default_url_file.exists():
                url_cfg_path = default_url_file
                logger.info(f"未找到或临时URL文件为空，将使用默认URL文件: {url_cfg_path}")
                progress_file = PROJECT_ROOT / 'progress.json'
                if progress_file.exists():
                    try:
                        progress_file.unlink(); logger.info(f"已删除旧的进度文件: {progress_file} (针对默认URL)。")
                    except OSError as e: logger.error(f"删除进度文件 {progress_file} 失败: {e}。")
            else:
                logger.error(f"默认配置文件不存在: {default_url_file}")
                with open(default_url_file, "w", encoding="utf-8") as f:
                    f.write("# URL list, one per line\nhttps://www.domain.com.au/rent/?suburb=sydney-nsw-2000\n")
                logger.info(f"示例配置文件已创建: {default_url_file}. 请填充后运行."); return []

            with open(url_cfg_path, "r", encoding="utf-8") as f:
                urls = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
            
            if not urls: logger.error(f"配置文件 {url_cfg_path} 中无有效URL."); return []
            
            logger.info(f"找到{len(urls)}个URL待处理 (来源: {'temp_urls.txt' if using_temp_urls else 'url.txt'}): {urls}")
            inter_url_delay_min = CONFIG['performance'].get('inter_url_delay_min', 3.0)
            inter_url_delay_max = CONFIG['performance'].get('inter_url_delay_max', 7.0)

            for i_url, url in enumerate(urls, 1):
                try:
                    logger.info(f"开始处理 ({i_url}/{len(urls)}): {url}")
                    total_count = self.search(url, using_temp_urls)
                    
                    region_name = extract_region_from_url(url)
                    logger.info(f"完成处理URL: {url}，开始保存数据 (区域: {region_name}, 房源数: {len(self.batch_writer.buffer)})")
                    
                    if CONFIG['features']['enable_batch_write']:
                        if output_mode in ['single_file', 'hybrid']:
                            all_properties_buffer.extend(self.batch_writer.buffer)
                        
                        if output_mode in ['per_url', 'hybrid']:
                            output_file = self.batch_writer.flush(region=region_name, total_count=len(self.batch_writer.buffer))
                            if output_file:
                                output_files.append(output_file)
                        
                        elif output_mode == 'single_file':
                            self.batch_writer.buffer = []
                    
                    if i_url < len(urls):
                        inter_url_delay = random.uniform(inter_url_delay_min, inter_url_delay_max)
                        logger.info(f"下一个URL前延迟 {inter_url_delay:.1f} 秒...")
                        time.sleep(inter_url_delay)
                except Exception as e: 
                    logger.error(f"处理URL {url} 严重错误，跳过.", exc_info=True)

            if CONFIG['features']['enable_batch_write'] and output_mode in ['single_file', 'hybrid'] and all_properties_buffer:
                logger.info(f"开始保存所有URL的合并数据...")
                self.batch_writer.buffer = all_properties_buffer
                combined_file = self.batch_writer.flush(region=combined_prefix, total_count=len(all_properties_buffer), output_format='csv')
                if combined_file:
                    output_files.append(combined_file)

            unique_files = list(set(output_files))
            logger.info(f"所有URL处理完毕，共生成 {len(unique_files)} 个输出文件")
            for output_file in unique_files:
                logger.info(f"生成的文件: {output_file}")
            
            logger.info("爬虫任务完成。")
            return unique_files

        except Exception as e:
            logger.critical(f"程序运行期间发生严重错误: {e}", exc_info=True)
            if CONFIG['features']['enable_batch_write']:
                logger.info("尝试在程序异常退出前保存已收集的数据...")
                try:
                    output_csv_path_on_exc = self.batch_writer.flush(region="Error_Recovery", total_count=0)
                    if output_csv_path_on_exc:
                        output_files.append(output_csv_path_on_exc)
                except Exception as save_exc:
                    logger.error(f"异常处理中保存数据失败: {save_exc}")
            return list(set(output_files))
        finally:
            logger.info("房源信息采集程序 (v2) 结束。")


def trigger_etl_job():
    """
    Triggers the new, notification-enabled ETL job script after the crawler successfully finishes.
    """
    logger.info("爬取完成，正在触发带通知的ETL数据更新任务...")
    try:
        # 更改为调用新的主控脚本
        project_root = Path(__file__).parent.parent
        etl_script_path = project_root / 'scripts' / 'automated_data_update_with_notifications.py'
        
        if not etl_script_path.exists():
            logger.error(f"新的ETL主控脚本未找到: {etl_script_path}")
            return

        python_executable = sys.executable
        
        # 附带 --run-once 参数
        command = [python_executable, str(etl_script_path), '--run-once']
        logger.info(f"正在执行: {' '.join(command)}")
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        logger.info("ETL任务触发完成。")
        if process.stdout:
            logger.info("ETL输出:\n" + process.stdout)
        if process.stderr:
            logger.warning("ETL 错误输出:\n" + process.stderr)
        
        if process.returncode != 0:
             logger.error(f"被触发的ETL任务执行失败，返回码: {process.returncode}")

    except FileNotFoundError:
        logger.error(f"无法找到Python解释器 '{sys.executable}' 或ETL脚本 '{etl_script_path}'")
    except Exception as e:
        logger.error(f"触发ETL任务时发生未知错误: {e}", exc_info=True)


if __name__ == "__main__":
    crawler = DomainCrawler()
    output_files = crawler.run()
    
    if output_files:
        print(f"生成了 {len(output_files)} 个输出文件:")
        for output_file in output_files:
            print(output_file)
        
        # 恢复链式调用
        trigger_etl_job()
        
        sys.exit(0)
    else:
        print("没有生成任何输出文件")
        sys.exit(1)
def trigger_etl_job():
    """
    Triggers the new, notification-enabled ETL job script after the crawler successfully finishes.
    """
    logger.info("爬取完成，正在触发带通知的ETL数据更新任务...")
    try:
        # 更改为调用新的主控脚本
        project_root = Path(__file__).parent.parent
        etl_script_path = project_root / 'scripts' / 'automated_data_update_with_notifications.py'
        
        if not etl_script_path.exists():
            logger.error(f"新的ETL主控脚本未找到: {etl_script_path}")
            return

        python_executable = sys.executable
        
        # 附带 --run-once 参数
        command = [python_executable, str(etl_script_path), '--run-once']
        logger.info(f"正在执行: {' '.join(command)}")
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        logger.info("ETL任务触发完成。")
        if process.stdout:
            logger.info("ETL输出:\n" + process.stdout)
        if process.stderr:
            logger.warning("ETL 错误输出:\n" + process.stderr)
        
        if process.returncode != 0:
             logger.error(f"被触发的ETL任务执行失败，返回码: {process.returncode}")

    except FileNotFoundError:
        logger.error(f"无法找到Python解释器 '{sys.executable}' 或ETL脚本 '{etl_script_path}'")
    except Exception as e:
        logger.error(f"触发ETL任务时发生未知错误: {e}", exc_info=True)
