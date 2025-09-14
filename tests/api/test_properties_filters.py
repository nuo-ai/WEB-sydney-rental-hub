"""
QA-001 回归测试（最小可检清单）— /api/properties

目的：
- 验证“列表 total 与分页累加一致”，保障“应用（N）/确定（N）”的口径稳定（前端表现：按钮显示的 N 与实际列表一致）
- 验证排序白名单与未知键 400（BE-002）
- 验证点名过滤 listing_id 的稳定性
- 使用 /api/locations/all 获取一个真实 suburb 进行 ILIKE 测试，避免硬编码

运行方式：
- 确保后端服务运行于 http://localhost:8000（或设置环境变量 BACKEND_BASE_URL）
  export BACKEND_BASE_URL=http://localhost:8000
- 安装 pytest 和 requests 后运行：pytest -q tests/api/test_properties_filters.py
"""

import os
import math
import time
import typing as t

import pytest
import requests


BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000").rstrip("/")


def _req_get(path: str, params: dict | None = None, timeout: float = 20.0):
    """GET 请求小工具：返回 (response, json)，失败抛异常；中文注释：便于统一失败信息"""
    url = f"{BASE_URL}{path}"
    resp = requests.get(url, params=params or {}, timeout=timeout)
    try:
        data = resp.json()
    except Exception:
        data = {"_raw": resp.text}
    return resp, data


def _fetch_total(params: dict) -> int:
    """通过 page_size=1 获取 pagination.total"""
    _, data = _req_get("/api/properties", {**params, "page_size": 1})
    # 允许 error 结构返回，这种情况抛出 Assertion 让用例显式失败
    assert data and isinstance(data, dict), f"Invalid response: {data!r}"
    assert "pagination" in data, f"Missing pagination: {data!r}"
    total = data["pagination"].get("total")
    assert isinstance(total, int), f"Invalid total: {total!r}"
    return total


def _fetch_all_items(params: dict, page_size: int = 20, max_pages: int = 1000) -> list[dict]:
    """拉全量数据（用于与 total 对齐）。注意：生产数据量大时可降低 max_pages 或仅校验首页与 total 的相容性。"""
    page = 1
    acc: list[dict] = []

    for _ in range(max_pages):
        resp, data = _req_get("/api/properties", {**params, "page": page, "page_size": page_size})
        assert resp.status_code == 200, f"Unexpected status for page={page}: {resp.status_code} {data}"

        items = data.get("data", [])
        pagination = data.get("pagination", {}) or {}
        assert isinstance(items, list), f"Invalid data list: {items!r}"
        acc.extend(items)

        has_next = bool(pagination.get("has_next"))
        if not has_next:
            break
        page += 1

    return acc


def _pick_any_suburb_from_locations() -> str | None:
    """从 /api/locations/all 获取一个 suburb 名称，避免硬编码；若无数据返回 None"""
    resp, data = _req_get("/api/locations/all")
    if resp.status_code != 200:
        return None
    items = data.get("data", []) or []
    for it in items:
        if it and it.get("type") == "suburb" and it.get("name"):
            return str(it["name"]).strip()
    return None


@pytest.mark.timeout(60)
def test_smoke_properties_endpoint():
    """冒烟：接口可用，结构包含 data/pagination。前端表现：基础数据可加载，分页信息完整。"""
    resp, data = _req_get("/api/properties", {"page_size": 1})
    assert resp.status_code == 200, f"status={resp.status_code}, body={data}"
    assert "data" in data and "pagination" in data, f"Invalid structure: {data}"


@pytest.mark.timeout(120)
def test_total_matches_sum_of_pages_with_suburb_ilike_when_possible():
    """
    使用一个真实 suburb 进行 ILIKE 过滤：
    - 预期 pagination.total 与分页累加一致（保障“应用（N）/确定（N）”与列表 total 一致）
    - 若当前库没有可用 suburb，则跳过（避免在空库时误报失败）
    """
    suburb = _pick_any_suburb_from_locations()
    if not suburb:
        pytest.skip("没有可用 suburb（/api/locations/all 返回空），跳过此用例")

    q = {"suburb": suburb}

    total = _fetch_total(q)
    all_items = _fetch_all_items(q, page_size=20)
    assert len(all_items) == total, f"len(items)={len(all_items)} != total={total} for suburb={suburb!r}"


@pytest.mark.timeout(60)
def test_listing_id_point_filter_selects_single_record_when_exists():
    """
    点名过滤稳定性：
    - 从首页拿到一个 listing_id
    - 再用 listing_id 参数查询，期望只返回该记录（或 pagination.total>=1，首条匹配）
    """
    resp, data = _req_get("/api/properties", {"page_size": 1})
    assert resp.status_code == 200, f"status={resp.status_code}, body={data}"
    items = data.get("data", []) or []
    if not items:
        pytest.skip("当前库无任何房源，跳过点名过滤用例")

    first = items[0]
    lid = first.get("listing_id")
    assert lid is not None, f"首页记录缺少 listing_id: {first}"

    # 用 listing_id 点名过滤
    resp2, data2 = _req_get("/api/properties", {"page_size": 20, "listing_id": str(lid)})
    assert resp2.status_code == 200, f"status={resp2.status_code}, body={data2}"
    items2 = data2.get("data", []) or []
    # 至少包含该 listing_id
    assert any(str(it.get("listing_id")) == str(lid) for it in items2), f"点名过滤未命中 listing_id={lid}"


@pytest.mark.timeout(60)
@pytest.mark.parametrize("sort_value", ["price_asc", "available_date_asc", "suburb_az", "inspection_earliest"])
def test_sort_whitelist_valid_values(sort_value: str):
    """
    排序白名单（前端表现：选择排序后，列表顺序稳定且可复现）：
    - 允许的值应返回 200
    - 进一步可选断言：当 total>0 时，排序方向与字段近似符合预期（数据相关，保守起见此处仅验证 200）
    """
    resp, data = _req_get("/api/properties", {"page_size": 5, "sort": sort_value})
    assert resp.status_code == 200, f"sort={sort_value}, status={resp.status_code}, body={data}"


@pytest.mark.timeout(60)
def test_sort_invalid_value_returns_400():
    """
    非白名单排序值 → 400（BE-002）；
    前端表现：用户传入非法 sort（或历史 URL 中残留）时，后端明确返回错误，避免悄悄回退造成误导。
    """
    resp, data = _req_get("/api/properties", {"page_size": 5, "sort": "price"})
    assert resp.status_code == 400, f"Expected 400 for invalid sort, got {resp.status_code}, body={data}"


@pytest.mark.timeout(60)
def test_unknown_query_key_returns_400():
    """
    未知过滤键 → 400（BE-002）；
    前端表现：契约外的参数被及时拒绝，便于快速定位与修复（避免“看起来正常但口径被稀释”的隐患）。
    """
    resp, data = _req_get("/api/properties", {"page_size": 5, "foo": "bar"})
    assert resp.status_code == 400, f"Expected 400 for unknown key, got {resp.status_code}, body={data}"


@pytest.mark.timeout(120)
def test_total_matches_sum_of_pages_without_filters_smoke():
    """
    基础口径测试（无筛选）：
    - total 与分页累加一致（允许空库时 len=0,total=0）
    """
    q = {}
    total = _fetch_total(q)
    all_items = _fetch_all_items(q, page_size=20)
    assert len(all_items) == total, f"len(items)={len(all_items)} != total={total} for no-filter smoke"
