#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Greater Sydney 地铁（Metro, GTFS route_type=1）沿线覆盖到的 suburb 列表 (CSV)。

功能概述
- 读取 TfNSW GTFS 静态数据（routes/trips/stop_times/stops）
- 仅保留地铁（Subway/Metro, route_type=1）
- 将地铁服务的站点坐标与提供的 suburb 边界（GeoJSON）做空间相交
- 按 suburb 聚合去重并导出 CSV（默认仅一列：suburb）

使用示例
  python scripts/build_metro_served_suburbs.py \
    --suburb-geojson WEB-sydney-rental-hub/database/sydney-suburbs-name.json \
    --gtfs-dir /path/to/gtfs/dir \
    --out reports/metro_served_suburbs.csv

可选参数
  --suburb-key SUBURB_FIELD      手动指定 GeoJSON 中郊区名字段（自动识别失败时使用）
  --include-details              额外输出 stations 与 lines 两列（便于核查）
  环境变量 GTFS_DIR              若未传 --gtfs-dir，将尝试从此环境变量读取

依赖
  pip install pandas geopandas shapely fiona pyproj
"""

import argparse
import os
import sys
import json
import warnings
from typing import Optional, Tuple, List, Set

import pandas as pd

# Geo 相关库按需导入，并给出友好提示
try:
    import geopandas as gpd
    from shapely.geometry import Point, shape
    from shapely.ops import unary_union
    from shapely.validation import make_valid
except Exception as e:
    geo_import_err = e
    gpd = None


# ---------------------------
# 工具函数
# ---------------------------

SUBURB_KEY_CANDIDATES = [
    "suburb", "SUBURB", "Suburb",
    "name", "NAME", "Name",
    "locality", "LOCALITY", "LocName",
    "ssc_name", "SSC_NAME", "sscname",
    "ssc_name_2016", "SSC_NAME_2016",
    "lga_name", "LGA_NAME"
]

GTFS_REQUIRED_FILES = ["routes.txt", "trips.txt", "stop_times.txt", "stops.txt"]


def exit_with_message(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def check_geodeps():
    if gpd is None:
        exit_with_message(
            "缺少地理依赖（geopandas/shapely/fiona/pyproj）。请先安装：\n"
            "  pip install pandas geopandas shapely fiona pyproj"
        )


def detect_suburb_key(geojson_path: str, user_key: Optional[str]) -> str:
    """启发式识别 suburb 字段名。仅读取首个 Feature 的 properties 键名以降低开销。"""
    if user_key:
        return user_key

    # 尝试低开销读取：仅读第一行/首个Feature
    # 如果文件很大，这个过程依然极小
    try:
        with open(geojson_path, "r", encoding="utf-8") as f:
            # 仅读取前几万字符，寻找第一个 "properties": {...}
            head = f.read(200000)  # 200KB 头部，一般足够覆盖到第一个 feature
            # 粗略查找 properties 区段
            p_idx = head.find('"properties"')
            if p_idx == -1:
                raise RuntimeError("未在 GeoJSON 头部找到 properties 片段（启发式失败）。")

            # 从 properties 起截取，补个大括号闭合，尝试 JSON 解析
            # 这是启发式；若失败则退回完整读取（由 gpd 完整加载）
            snippet = head[p_idx:]
            # 简单定位第一个 '{' 和 随后的 '}' 进行匹配提取（不严谨但足够头部）
            lb = snippet.find("{")
            rb = snippet.find("}")
            if lb != -1 and rb != -1 and rb > lb:
                props_text = snippet[lb:rb+1]
                try:
                    props = json.loads(props_text)
                    if isinstance(props, dict):
                        keys = list(props.keys())
                        # 按优先级选择
                        for cand in SUBURB_KEY_CANDIDATES:
                            if cand in keys:
                                print(f"[info] 自动识别 suburb 字段: {cand}")
                                return cand
                        # 否则打出提示
                        print("[warn] 未从属性中匹配到常见字段，候选 keys 如下：", keys[:10])
                except Exception:
                    pass
    except Exception:
        pass

    # 回退方案：完整读取一条 feature 的 properties
    try:
        import fiona
        with fiona.open(geojson_path, "r") as src:
            for feat in src:
                props = feat.get("properties", {}) or {}
                keys = props.keys()
                for cand in SUBURB_KEY_CANDIDATES:
                    if cand in keys:
                        print(f"[info] 自动识别 suburb 字段: {cand}")
                        return cand
                print("[warn] 未从属性中匹配到常见字段，候选 keys 如下：", list(keys)[:20])
                break
    except Exception as e:
        print(f"[warn] Fiona 读取失败或无法探测属性: {e}")

    exit_with_message(
        "无法自动识别 GeoJSON 的 suburb 字段名。请使用参数 --suburb-key 手动指定。\n"
        f"文件: {geojson_path}"
    )
    return ""


def validate_gtfs_dir(gtfs_dir: Optional[str]) -> str:
    if gtfs_dir is None or gtfs_dir.strip() == "":
        gtfs_dir = os.environ.get("GTFS_DIR", "")

    if not gtfs_dir:
        exit_with_message(
            "未提供 --gtfs-dir 且未设置环境变量 GTFS_DIR。\n"
            "请提供 TfNSW GTFS 静态数据目录（包含 routes.txt, trips.txt, stop_times.txt, stops.txt）。"
        )

    missing = [fn for fn in GTFS_REQUIRED_FILES if not os.path.isfile(os.path.join(gtfs_dir, fn))]
    if missing:
        exit_with_message(
            "GTFS 目录缺少必要文件：\n  - " + "\n  - ".join(missing) +
            f"\n提供目录: {gtfs_dir}\n"
            "提示：请从 TfNSW Open Data 下载 GTFS 静态包后解压到该目录。"
        )
    return gtfs_dir


def load_gtfs_metro_stations(gtfs_dir: str) -> pd.DataFrame:
    """加载 GTFS，并返回 Metro 站点（DataFrame: station_stop_id, stop_name, lon, lat, route_names）。"""
    routes = pd.read_csv(os.path.join(gtfs_dir, "routes.txt"), dtype=str)
    trips = pd.read_csv(os.path.join(gtfs_dir, "trips.txt"), dtype=str)
    stop_times = pd.read_csv(os.path.join(gtfs_dir, "stop_times.txt"), dtype=str)
    stops = pd.read_csv(os.path.join(gtfs_dir, "stops.txt"), dtype=str)

    # 清洗列名兼容（部分 GTFS 大小写不同）
    for df in (routes, trips, stop_times, stops):
        df.columns = [c.strip() for c in df.columns]

    # 过滤 Metro（Subway）
    # 标准 GTFS: route_type = 1 -> Subway/Metro
    routes["route_type"] = routes["route_type"].astype(str)
    metro_routes = routes[routes["route_type"] == "1"].copy()
    if metro_routes.empty:
        exit_with_message("routes.txt 中未发现 route_type=1（Metro）。确认该 GTFS 是否包含地铁线路？")

    # 关联 trips → stop_times → stops
    trips_metro = trips.merge(metro_routes[["route_id", "route_short_name", "route_long_name"]], on="route_id", how="inner")
    st_metro = stop_times.merge(trips_metro[["trip_id", "route_id", "route_short_name", "route_long_name"]], on="trip_id", how="inner")
    st_metro = st_metro.merge(stops, on="stop_id", how="inner", suffixes=("", "_stop"))

    # 站点层级处理：station (location_type=1) 优先；platform(0) 回溯 parent_station
    # 缺省用自身 stop
    def compute_station_id(row):
        lt = str(row.get("location_type", "")).strip()
        ps = str(row.get("parent_station", "")).strip()
        sid = str(row.get("stop_id", "")).strip()
        if lt == "1":  # station
            return sid
        if ps and ps.lower() != "nan":
            return ps
        return sid

    st_metro["station_stop_id"] = st_metro.apply(compute_station_id, axis=1)

    # 提取站点基本信息（从 stops 表获取 station 行）
    # 确保 station 坐标
    station_info = stops.copy()
    station_info["stop_id"] = station_info["stop_id"].astype(str)
    station_info = station_info.rename(columns={"stop_id": "station_stop_id"})
    station_info = station_info[["station_stop_id", "stop_name", "stop_lon", "stop_lat", "location_type", "parent_station"]].copy()

    # 聚合每个 station 的线路名集合
    st_metro["route_label"] = st_metro.apply(
        lambda r: (r["route_short_name"] or "").strip() or (r["route_long_name"] or "").strip(),
        axis=1
    )
    routes_by_station = st_metro.groupby("station_stop_id")["route_label"].agg(lambda s: sorted(set([x for x in s if x]))).reset_index()
    routes_by_station.rename(columns={"route_label": "route_labels"}, inplace=True)

    station_df = station_info.merge(routes_by_station, on="station_stop_id", how="inner")

    # 坐标清洗
    def to_float(x):
        try:
            return float(x)
        except Exception:
            return None

    station_df["lon"] = station_df["stop_lon"].apply(to_float)
    station_df["lat"] = station_df["stop_lat"].apply(to_float)
    station_df = station_df.dropna(subset=["lon", "lat"])

    # 去重
    station_df = station_df.drop_duplicates(subset=["station_stop_id"]).reset_index(drop=True)

    return station_df[["station_stop_id", "stop_name", "lon", "lat", "route_labels"]]


def load_suburbs_gdf(geojson_path: str, suburb_key: str) -> gpd.GeoDataFrame:
    """加载 suburb 边界，并返回 GeoDataFrame（WGS84）。"""
    check_geodeps()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        gdf = gpd.read_file(geojson_path)

    if gdf.empty:
        exit_with_message(f"GeoJSON 读取为空：{geojson_path}")

    # 修复无效几何
    try:
        gdf["geometry"] = gdf["geometry"].apply(lambda geom: make_valid(geom))
    except Exception:
        # 部分 shapely 版本无 make_valid，用 buffer(0) 兜底
        gdf["geometry"] = gdf["geometry"].buffer(0)

    # CRS 统一到 EPSG:4326
    try:
        if gdf.crs is None:
            # 假定为 WGS84；如不是可在外层改 to_crs
            gdf.set_crs(epsg=4326, inplace=True)
        else:
            gdf.to_crs(epsg=4326, inplace=True)
    except Exception as e:
        print(f"[warn] 无法设置/转换 CRS，将按原 CRS 使用: {e}")

    if suburb_key not in gdf.columns:
        exit_with_message(f"指定的 suburb 字段 '{suburb_key}' 不存在于 GeoJSON 属性中。可用字段: {list(gdf.columns)}")

    # 仅保留必要字段
    gdf = gdf[[suburb_key, "geometry"]].rename(columns={suburb_key: "suburb"})
    return gdf


def build_served_suburbs(suburbs_gdf: gpd.GeoDataFrame,
                         stations_df: pd.DataFrame,
                         include_details: bool = False) -> pd.DataFrame:
    """空间相交：地铁站点落在 suburb 多边形内，聚合得到 suburb 清单（可选附加站点/线路）。"""
    check_geodeps()

    points_gdf = gpd.GeoDataFrame(
        stations_df.copy(),
        geometry=[Point(xy) for xy in zip(stations_df["lon"], stations_df["lat"])],
        crs="EPSG:4326"
    )

    # sjoin within
    joined = gpd.sjoin(points_gdf, suburbs_gdf, predicate="within", how="inner")
    if joined.empty:
        exit_with_message("空间相交结果为空。请检查坐标/范围是否匹配（EPSG:4326）。")

    if include_details:
        # 聚合每个 suburb 的站点名和线路名
        def agg_list(series: pd.Series) -> str:
            uniq = sorted(set([str(x) for x in series if pd.notna(x) and str(x).strip()]))
            return "; ".join(uniq)

        # 站点名
        stations_by_suburb = joined.groupby("suburb")["stop_name"].agg(agg_list).reset_index().rename(columns={"stop_name": "stations"})
        # 线路集合展开后再聚合
        exploded = joined[["suburb", "route_labels"]].explode("route_labels")
        lines_by_suburb = exploded.groupby("suburb")["route_labels"].agg(agg_list).reset_index().rename(columns={"route_labels": "lines"})

        out = pd.DataFrame({"suburb": sorted(joined["suburb"].unique())})
        out = out.merge(stations_by_suburb, on="suburb", how="left")
        out = out.merge(lines_by_suburb, on="suburb", how="left")
        return out

    # 仅 suburb 列
    out = pd.DataFrame({"suburb": sorted(joined["suburb"].unique())})
    return out


# ---------------------------
# 主流程
# ---------------------------

def main():
    parser = argparse.ArgumentParser(description="生成 Greater Sydney 地铁沿线覆盖的 suburb 列表 CSV")
    parser.add_argument("--suburb-geojson", required=True, help="Suburb 边界（GeoJSON/JSON）路径")
    parser.add_argument("--gtfs-dir", default=os.environ.get("GTFS_DIR", ""), help="GTFS 目录（含 routes/trips/stop_times/stops）")
    parser.add_argument("--suburb-key", default=None, help="GeoJSON 中代表郊区名的字段（不指定则自动识别）")
    parser.add_argument("--out", default="reports/metro_served_suburbs.csv", help="输出 CSV 路径（默认 reports/metro_served_suburbs.csv）")
    parser.add_argument("--include-details", action="store_true", help="输出附加列：stations, lines")
    args = parser.parse_args()

    # 校验依赖
    check_geodeps()

    # 检查 GTFS 目录与文件
    gtfs_dir = validate_gtfs_dir(args.gtfs_dir)

    # suburb 字段名识别
    suburb_key = detect_suburb_key(args.suburb_geojson, args.suburb_key)

    print(f"[info] 使用 GTFS 目录: {gtfs_dir}")
    print(f"[info] 使用 GeoJSON: {args.suburb_geojson}")
    print(f"[info] suburb 字段: {suburb_key}")

    # 加载 GTFS 与 suburb
    stations_df = load_gtfs_metro_stations(gtfs_dir)
    suburbs_gdf = load_suburbs_gdf(args.suburb_geojson, suburb_key)

    # 构建结果并导出
    out_df = build_served_suburbs(suburbs_gdf, stations_df, include_details=args.include_details)

    # 确保输出目录存在
    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)

    out_df.to_csv(args.out, index=False, encoding="utf-8-sig")
    print(f"[done] 已输出: {args.out}（共 {len(out_df)} 行）")


if __name__ == "__main__":
    main()
