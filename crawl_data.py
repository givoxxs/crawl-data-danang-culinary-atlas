import os
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv
import time

# 1. Load API key từ file .env
load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

if not API_KEY:
    raise ValueError("API key not found! Hãy chắc rằng bạn đã tạo file .env")

# 2. Load danh sách từ khóa từ file JSON
with open("./data/keywords_danang.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

all_results = {}

# 3. Lặp qua từng từ khóa, gọi API SerpApi
for kw in keywords:
    print(f"🔎 Đang tìm: {kw}")
    params = {
        "q": kw,
        "engine": "google_maps",         # dùng Google Maps engine
        "location": "Da Nang, Viet Nam", # địa điểm
        "hl": "vi",                      # ngôn ngữ kết quả
        "gl": "vn",                      # quốc gia
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    result = search.get_dict()

    # Lưu kết quả của keyword vào dictionary
    all_results[kw] = result

    # Nghỉ 1-2 giây để tránh rate-limit
    time.sleep(2)

# 4. Lưu dữ liệu ra file JSON
with open("./data/danang_places_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("✅ Crawl hoàn tất, dữ liệu lưu ở ./data/danang_places_results.json")
# python crawl_data.py