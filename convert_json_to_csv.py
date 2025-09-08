import os
import json
import argparse
from typing import Any, Dict, List, Tuple
import pandas as pd


def safe_get(d: Dict[str, Any], path: List[str], default: Any = None) -> Any:
    node: Any = d
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def normalize_local_result(keyword: str, item: Dict[str, Any]) -> Dict[str, Any]:
    gps = item.get("gps_coordinates") or {}
    operating_hours = item.get("operating_hours") or {}
    service_options = item.get("service_options") or {}

    # Convert list fields to comma-joined strings for CSV friendliness
    types = ", ".join(item.get("types") or []) if isinstance(item.get("types"), list) else item.get("types")
    type_ids = ", ".join(item.get("type_ids") or []) if isinstance(item.get("type_ids"), list) else item.get("type_ids")

    row: Dict[str, Any] = {
        "keyword": keyword,
        "position": item.get("position"),
        "title": item.get("title"),
        "place_id": item.get("place_id"),
        "data_id": item.get("data_id"),
        "data_cid": item.get("data_cid"),
        "provider_id": item.get("provider_id"),
        "rating": item.get("rating"),
        "reviews": item.get("reviews"),
        "price": item.get("price"),
        "type": item.get("type"),
        "types": types,
        "type_id": item.get("type_id"),
        "type_ids": type_ids,
        "address": item.get("address"),
        "open_state": item.get("open_state") or item.get("hours"),
        "phone": item.get("phone"),
        "website": item.get("website"),
        "latitude": gps.get("latitude"),
        "longitude": gps.get("longitude"),
        "user_review": item.get("user_review"),
        "thumbnail": item.get("thumbnail"),
        "serpapi_thumbnail": item.get("serpapi_thumbnail"),
        "reviews_link": item.get("reviews_link"),
        "photos_link": item.get("photos_link"),
        "place_id_search": item.get("place_id_search"),
        # Keep JSON-encoded for structured fields
        "operating_hours_json": json.dumps(operating_hours, ensure_ascii=False) if operating_hours else None,
        "service_options_json": json.dumps(service_options, ensure_ascii=False) if service_options else None,
    }
    return row


def load_and_flatten(input_path: str) -> pd.DataFrame:
    with open(input_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)

    rows: List[Dict[str, Any]] = []
    for keyword, payload in data.items():
        local_results = payload.get("local_results") or []
        if not isinstance(local_results, list):
            continue
        for item in local_results:
            rows.append(normalize_local_result(keyword, item))

    df = pd.DataFrame(rows)
    return df


def deduplicate(df: pd.DataFrame, coord_round: int = 6) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # Prepare coordinate key rounded to tolerance
    df = df.copy()
    df["lat_rounded"] = df["latitude"].round(coord_round)
    df["lon_rounded"] = df["longitude"].round(coord_round)

    # Primary dedup by (lat, lon); keep first occurrence (stable)
    before_count = len(df)
    deduped = df.drop_duplicates(subset=["lat_rounded", "lon_rounded"], keep="first")

    # For reporting which rows were removed
    removed_idx = df.index.difference(deduped.index)
    removed = df.loc[removed_idx].copy()

    # Drop helper columns
    for col in ["lat_rounded", "lon_rounded"]:
        if col in deduped.columns:
            deduped = deduped.drop(columns=[col])
        if col in removed.columns:
            removed = removed.drop(columns=[col])

    print(f"Tổng bản ghi trước khi loại trùng: {before_count}")
    print(f"Số bản ghi bị loại do trùng toạ độ: {len(removed)}")
    print(f"Tổng bản ghi sau khi loại trùng: {len(deduped)}")
    return deduped, removed


def main():
    parser = argparse.ArgumentParser(description="Chuyển dữ liệu SerpApi Google Maps từ JSON sang CSV và loại trùng theo toạ độ.")
    parser.add_argument("--input", default="./data/danang_places_results.json", help="Đường dẫn file JSON đầu vào")
    parser.add_argument("--out-raw", default="./data/danang_places_results_raw.csv", help="Đường dẫn CSV thô (chưa loại trùng)")
    parser.add_argument("--out-dedup", default="./data/danang_places_results_dedup.csv", help="Đường dẫn CSV sau loại trùng")
    parser.add_argument("--coord-round", type=int, default=6, help="Số chữ số làm tròn khi so sánh toạ độ")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out_raw), exist_ok=True)

    print("Đang đọc và làm phẳng dữ liệu...")
    df = load_and_flatten(args.input)
    print(f"Số dòng sau khi làm phẳng: {len(df)}")

    print(f"Lưu CSV thô: {args.out_raw}")
    df.to_csv(args.out_raw, index=False)

    print("Đang loại trùng theo toạ độ...")
    deduped, removed = deduplicate(df, coord_round=args.coord_round)

    print(f"Lưu CSV sau loại trùng: {args.out_dedup}")
    deduped.to_csv(args.out_dedup, index=False)

    # Cũng lưu danh sách các bản ghi bị loại (tham khảo)
    removed_path = args.out_dedup.replace(".csv", "_removed_dupes.csv")
    print(f"Lưu danh sách bản ghi bị loại: {removed_path}")
    removed.to_csv(removed_path, index=False)

    print("Hoàn tất.")


if __name__ == "__main__":
    main()


# python convert_json_to_csv.py