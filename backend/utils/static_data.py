"""Static dataset helpers used when the primary database is unavailable."""

from __future__ import annotations

import copy
import json
import logging
import math
import os
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _resolve_dataset_path() -> Optional[Path]:
    """Locate a static response payload shipped with the repository."""

    candidates: List[Path] = []

    env_path = os.getenv("STATIC_PROPERTIES_PATH")
    if env_path:
        path = Path(env_path).expanduser().resolve()
        if path.is_file():
            candidates.append(path)
        else:
            logger.warning(
                "STATIC_PROPERTIES_PATH=%s does not exist or is not a file", env_path
            )

    repo_root = Path(__file__).resolve().parents[2]
    for name in ("backend_test.json", "test_response.json"):
        candidate = (repo_root / name).resolve()
        if candidate.is_file():
            candidates.append(candidate)

    for path in candidates:
        if path.is_file():
            return path

    return None


def _clone_dict(item: Mapping[str, Any]) -> Dict[str, Any]:
    """Create a deep copy of a dictionary for safe mutation downstream."""

    return copy.deepcopy(dict(item))


def _normalise_postcode(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


@lru_cache(maxsize=1)
def _load_dataset() -> Optional[Dict[str, Any]]:
    """Load the JSON payload once and cache it for subsequent requests."""

    path = _resolve_dataset_path()
    if not path:
        logger.warning("No static property dataset found for fallback responses.")
        return None

    try:
        with path.open("r", encoding="utf-8") as fp:
            raw = json.load(fp)
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Failed to load static dataset from %s: %s", path, exc)
        return None

    items: List[Dict[str, Any]] = []
    for record in raw.get("data") or []:
        if not isinstance(record, Mapping):
            continue
        item = _clone_dict(record)
        # Ensure consistent primitive types for downstream filtering/sorting
        if "listing_id" in item:
            try:
                item["listing_id"] = int(item["listing_id"])
            except (TypeError, ValueError):
                item["listing_id"] = str(item["listing_id"])
        postcode = _normalise_postcode(item.get("postcode"))
        if postcode is not None:
            item["postcode"] = postcode
        images = item.get("images")
        if isinstance(images, str):
            item["images"] = [images]
        inspection_times = item.get("inspection_times")
        if isinstance(inspection_times, str):
            item["inspection_times"] = [inspection_times]
        items.append(item)

    logger.info("Loaded %d static property records from %s", len(items), path)

    return {
        "items": tuple(items),
        "pagination": raw.get("pagination") or {},
        "path": str(path),
    }


def dataset_available() -> bool:
    """Return True when a bundled dataset is available for use."""

    return _load_dataset() is not None


# ---------------------------------------------------------------------------
# Helpers for filtering and sorting
# ---------------------------------------------------------------------------

def _split_csv(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        results: List[str] = []
        for item in value:
            results.extend(_split_csv(item))
        return results
    return [part.strip() for part in str(value).split(",") if part and part.strip()]


def _normalize_str(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def _safe_int(value: Any, default: Optional[int] = 0) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default


def _parse_bool_param(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = _normalize_str(value)
    if not text:
        return None
    if text in {"true", "t", "1", "yes", "y"}:
        return True
    if text in {"false", "f", "0", "no", "n"}:
        return False
    return None


def _normalize_furnished(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    text = _normalize_str(value)
    if not text:
        return None
    if text in {"true", "t", "1", "yes", "y"}:
        return True
    if text in {"false", "f", "0", "no", "n"}:
        return False
    return None


def _parse_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    if not text:
        return None
    text = text.split("T", 1)[0]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _available_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    if not text:
        return None
    lowered = text.lower()
    if lowered in {"available now", "now", "立即入住"}:
        return None
    text = text.split("T", 1)[0]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def _listing_id_key(item: Mapping[str, Any]) -> Tuple[int, str]:
    raw = item.get("listing_id")
    numeric = _safe_int(raw, 0) or 0
    return numeric, str(raw)


def _price_sort_key(item: Mapping[str, Any]) -> Tuple[float, Tuple[int, str]]:
    rent = item.get("rent_pw")
    try:
        value = float(rent)
    except (TypeError, ValueError):
        value = float("inf")
    return value, _listing_id_key(item)


def _available_date_sort_key(item: Mapping[str, Any]) -> Tuple[int, Any, Tuple[int, str]]:
    value = _available_date(item.get("available_date"))
    if value is None:
        return 1, date.max, _listing_id_key(item)
    return 0, value, _listing_id_key(item)


def _inspection_sort_key(item: Mapping[str, Any]) -> Tuple[int, str, Tuple[int, str]]:
    times = item.get("inspection_times")
    if not times:
        return 1, "", _listing_id_key(item)
    if isinstance(times, (list, tuple, set)):
        values: List[str] = []
        for entry in times:
            if isinstance(entry, (datetime, date)):
                values.append(entry.isoformat())
            elif entry:
                values.append(str(entry))
    else:
        entry = times
        if isinstance(entry, (datetime, date)):
            values = [entry.isoformat()]
        elif entry:
            values = [str(entry)]
        else:
            values = []
    cleaned = [val.strip() for val in values if val and val.strip()]
    if not cleaned:
        return 1, "", _listing_id_key(item)
    earliest = sorted(cleaned)[0].lower()
    return 0, earliest, _listing_id_key(item)


def _match_suburb(item: Mapping[str, Any], suburbs: Sequence[str]) -> bool:
    if not suburbs:
        return True
    value = _normalize_str(item.get("suburb"))
    if not value:
        return False
    return any(token in value for token in suburbs)


def _match_property_type(item: Mapping[str, Any], target: str) -> bool:
    if not target:
        return True
    return target in _normalize_str(item.get("property_type"))


def _match_bedrooms(item: Mapping[str, Any], tokens: Sequence[str]) -> bool:
    if not tokens:
        return True
    raw = item.get("bedrooms")
    try:
        numeric = float(raw)
    except (TypeError, ValueError):
        numeric = None
    for token in tokens:
        if token.endswith("+"):
            try:
                threshold = int(token[:-1])
            except ValueError:
                continue
            if numeric is not None and numeric >= threshold:
                return True
        elif token == "studio":
            if str(raw).strip().lower() in {"0", "studio"}:
                return True
        else:
            try:
                expected = int(token)
            except ValueError:
                continue
            if numeric is not None and numeric == expected:
                return True
    return False


def _match_numeric_with_plus(value: Any, tokens: Sequence[str]) -> bool:
    if not tokens:
        return True
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return False
    for token in tokens:
        if token == "any":
            return True
        if token.endswith("+"):
            try:
                threshold = int(token[:-1])
            except ValueError:
                continue
            if numeric >= threshold:
                return True
        else:
            try:
                expected = int(token)
            except ValueError:
                continue
            if numeric == expected:
                return True
    return False


def _date_matches(
    available: Optional[date],
    date_from: Optional[date],
    date_to: Optional[date],
    today: date,
) -> bool:
    if date_from and date_to:
        if date_from <= today and available is None:
            return True
        if available is None:
            return False
        return date_from <= available <= date_to
    if date_from:
        if date_from <= today and available is None:
            return True
        if available is None:
            return False
        return available >= date_from
    if date_to:
        if available is None:
            return True
        return available <= date_to
    return True


def _to_iterable_names(values: Any) -> List[str]:
    if values is None:
        return []
    if isinstance(values, str):
        return [values]
    if isinstance(values, Iterable):
        result: List[str] = []
        for item in values:
            if item is None:
                continue
            result.append(str(item))
        return result
    return [str(values)]


@lru_cache(maxsize=1)
def _build_location_index() -> Dict[str, Any]:
    dataset = _load_dataset()
    if not dataset:
        return {"all": tuple(), "suburbs": tuple(), "lookup": {}}

    suburb_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    postcode_map: Dict[str, Dict[str, Any]] = {}

    for item in dataset["items"]:
        suburb_raw = item.get("suburb")
        postcode_raw = item.get("postcode")
        suburb = str(suburb_raw).strip()
        if not suburb:
            continue
        postcode = str(postcode_raw).strip() if postcode_raw is not None else "0"
        key = (suburb.lower(), postcode)

        suburb_entry = suburb_map.get(key)
        if not suburb_entry:
            suburb_entry = {
                "id": f"{suburb}_{postcode}",
                "type": "suburb",
                "name": suburb,
                "postcode": postcode,
                "fullName": f"{suburb}, NSW, {postcode}" if postcode and postcode != "0" else f"{suburb}, NSW",
                "count": 0,
            }
            suburb_map[key] = suburb_entry
        suburb_entry["count"] += 1

        postcode_entry = postcode_map.get(postcode)
        if not postcode_entry:
            postcode_entry = {
                "id": f"postcode_{postcode}",
                "type": "postcode",
                "name": postcode,
                "suburbs": [],
                "fullName": postcode,
                "count": 0,
            }
            postcode_map[postcode] = postcode_entry
        if suburb not in postcode_entry["suburbs"]:
            postcode_entry["suburbs"].append(suburb)
        postcode_entry["count"] += 1

    suburb_entries = sorted(
        (copy.deepcopy(entry) for entry in suburb_map.values()),
        key=lambda item: (-item["count"], item["name"].lower()),
    )

    postcode_entries: List[Dict[str, Any]] = []
    for entry in postcode_map.values():
        preview = ", ".join(entry["suburbs"][:3])
        if len(entry["suburbs"]) > 3:
            preview += f" +{len(entry['suburbs']) - 3} more"
        entry_copy = copy.deepcopy(entry)
        entry_copy["fullName"] = f"{entry_copy['name']} ({preview})" if preview else entry_copy["name"]
        postcode_entries.append(entry_copy)
    postcode_entries.sort(key=lambda item: (-item["count"], item["name"]))

    lookup = {item["name"].strip().lower(): item for item in suburb_entries}

    all_entries = tuple(suburb_entries + postcode_entries)
    return {"all": all_entries, "suburbs": tuple(suburb_entries), "lookup": lookup}


# ---------------------------------------------------------------------------
# Public APIs
# ---------------------------------------------------------------------------

def get_property(listing_id: Any) -> Optional[Dict[str, Any]]:
    """Return a single property by listing id from the static dataset."""

    dataset = _load_dataset()
    if not dataset:
        return None

    if listing_id is None:
        return None

    target = str(listing_id).strip()
    if not target:
        return None

    for item in dataset["items"]:
        if str(item.get("listing_id")) == target:
            return copy.deepcopy(item)

    return None


def list_properties(
    params: Mapping[str, Any],
    *,
    page: int,
    page_size: int,
) -> Optional[Dict[str, Any]]:
    """Return filtered properties with pagination metadata."""

    dataset = _load_dataset()
    if not dataset:
        return None

    today = datetime.now().date()

    suburb_tokens = [_normalize_str(v) for v in _split_csv(params.get("suburb")) if _normalize_str(v)]
    property_type_token = _normalize_str(params.get("property_type"))
    bedroom_tokens = [_normalize_str(v) for v in _split_csv(params.get("bedrooms")) if _normalize_str(v)]
    bathroom_tokens = [_normalize_str(v) for v in _split_csv(params.get("bathrooms")) if _normalize_str(v)]
    parking_tokens = [_normalize_str(v) for v in _split_csv(params.get("parking")) if _normalize_str(v)]
    min_price = _safe_int(params.get("minPrice"), None)
    max_price = _safe_int(params.get("maxPrice"), None)
    date_from = _parse_date(params.get("date_from"))
    date_to = _parse_date(params.get("date_to"))
    effective_furnished = _parse_bool_param(params.get("isFurnished"))
    if effective_furnished is None:
        effective_furnished = _parse_bool_param(params.get("furnished"))
    listing_id_filter = params.get("listing_id")
    listing_id_filter_str = str(listing_id_filter).strip() if listing_id_filter is not None else ""

    sort_value = _normalize_str(params.get("sort"))

    filtered: List[Dict[str, Any]] = []
    for item in dataset["items"]:
        if not _match_suburb(item, suburb_tokens):
            continue
        if not _match_property_type(item, property_type_token):
            continue
        if not _match_bedrooms(item, bedroom_tokens):
            continue
        if not _match_numeric_with_plus(item.get("bathrooms"), bathroom_tokens):
            continue
        if not _match_numeric_with_plus(item.get("parking_spaces"), parking_tokens):
            continue

        rent_value = _safe_int(item.get("rent_pw"), None)
        if min_price is not None:
            if rent_value is None or rent_value < min_price:
                continue
        if max_price is not None:
            if rent_value is None or rent_value > max_price:
                continue

        if listing_id_filter_str:
            if str(item.get("listing_id")) != listing_id_filter_str:
                continue

        available_value = _available_date(item.get("available_date"))
        if not _date_matches(available_value, date_from, date_to, today):
            continue

        if effective_furnished is not None:
            furnished_value = _normalize_furnished(item.get("is_furnished"))
            if effective_furnished and furnished_value is not True:
                continue
            if effective_furnished is False and furnished_value is not False:
                continue

        filtered.append(item)

    if sort_value == "price_asc":
        filtered.sort(key=_price_sort_key)
    elif sort_value == "available_date_asc":
        filtered.sort(key=_available_date_sort_key)
    elif sort_value == "suburb_az":
        filtered.sort(key=lambda item: (_normalize_str(item.get("suburb")), _listing_id_key(item)))
    elif sort_value == "inspection_earliest":
        filtered.sort(key=_inspection_sort_key)
    else:
        filtered.sort(key=_listing_id_key)

    total = len(filtered)
    page = max(page, 1)
    page_size = max(1, min(page_size, 100))

    if total == 0:
        pages = 0
        page = 1
    else:
        pages = math.ceil(total / page_size)
        if page > pages:
            page = pages

    start = (page - 1) * page_size if total else 0
    end = start + page_size
    page_items = filtered[start:end]

    pagination = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": end < total,
        "has_prev": start > 0 and total > 0,
        "next_cursor": None,
    }

    data_items = [copy.deepcopy(item) for item in page_items]
    return {"data": data_items, "pagination": pagination}


def list_locations() -> List[Dict[str, Any]]:
    """Return all suburb/postcode entries with property counts."""

    index = _build_location_index()
    return [copy.deepcopy(entry) for entry in index["all"]]


def suggest_locations(query: Optional[str], limit: int) -> List[Dict[str, Any]]:
    """Return location suggestions filtered by the provided query."""

    index = _build_location_index()
    entries = list(index["all"])
    if query:
        token = _normalize_str(query)
        if token:
            entries = [
                entry
                for entry in entries
                if token in _normalize_str(entry.get("name"))
                or token in _normalize_str(entry.get("fullName"))
            ]
    limit = max(limit, 0)
    return [copy.deepcopy(entry) for entry in entries[:limit]]


def nearby_suburbs(
    suburb: str,
    limit: int,
    mapping: Optional[Mapping[str, Sequence[str]]] = None,
) -> Dict[str, Any]:
    """Return a structure compatible with the /api/locations/nearby endpoint."""

    index = _build_location_index()
    limit = max(limit, 0)
    if not index["suburbs"] or not suburb:
        return {"current": suburb, "nearby": []}

    normalized_current = _normalize_str(suburb)
    normalized_mapping: Dict[str, List[str]] = {}
    if mapping:
        for key, values in mapping.items():
            normalized_mapping[_normalize_str(key)] = _to_iterable_names(values)

    requested_names = normalized_mapping.get(normalized_current, [])
    lookup = {_normalize_str(entry.get("name")): entry for entry in index["suburbs"]}

    used: set[str] = set()
    nearby: List[Dict[str, Any]] = []

    for name in requested_names:
        key = _normalize_str(name)
        entry = lookup.get(key)
        if entry and key not in used:
            nearby.append(copy.deepcopy(entry))
            used.add(key)
        if len(nearby) >= limit:
            break

    if len(nearby) < limit:
        for entry in index["suburbs"]:
            key = _normalize_str(entry.get("name"))
            if key in used or key == normalized_current:
                continue
            nearby.append(copy.deepcopy(entry))
            used.add(key)
            if len(nearby) >= limit:
                break

    return {"current": suburb, "nearby": nearby[:limit]}
