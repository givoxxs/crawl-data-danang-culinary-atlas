# Tạo danh sách từ khóa đầy đủ cho việc crawl quán ăn/đồ uống ở Đà Nẵng
keywords = [
    # Nhóm 1: Tổng quát
    "Quán ăn Đà Nẵng",
    "Nhà hàng Đà Nẵng",
    "Quán nhậu Đà Nẵng",
    "Quán ăn ngon Đà Nẵng",
    "Địa điểm ăn uống Đà Nẵng",
    "Food Đà Nẵng",

    # Nhóm 2: Đồ uống – cafe, trà
    "Quán cà phê Đà Nẵng",
    "Coffee shop Đà Nẵng",
    "Quán cafe view đẹp Đà Nẵng",
    "Trà sữa Đà Nẵng",
    "Quán sinh tố Đà Nẵng",
    "Quán nước ép Đà Nẵng",
    "Quán pub Đà Nẵng",
    "Quán bar Đà Nẵng",

    # Nhóm 3: Món đặc sản
    "Mì Quảng Đà Nẵng",
    "Bún chả cá Đà Nẵng",
    "Bún bò Đà Nẵng",
    "Bánh xèo Đà Nẵng",
    "Bánh tráng cuốn thịt heo Đà Nẵng",
    "Cao lầu Đà Nẵng",
    "Hải sản Đà Nẵng",
    "Quán ốc Đà Nẵng",

    # Nhóm 4: Món phổ biến & fastfood
    "Phở Đà Nẵng",
    "Cơm gà Đà Nẵng",
    "Pizza Đà Nẵng",
    "Sushi Đà Nẵng",
    "BBQ Đà Nẵng",
    "Buffet Đà Nẵng",
    "Lẩu Đà Nẵng",
    "Quán ăn chay Đà Nẵng",
    "Vegan restaurant Da Nang",
    "Fast food Đà Nẵng",
    "KFC Đà Nẵng",
    "Lotteria Đà Nẵng",
    "McDonald's Đà Nẵng",
    "Burger King Đà Nẵng",

    # Nhóm 5: Cho khách du lịch (tiếng Anh)
    "Restaurants in Da Nang",
    "Best food Da Nang",
    "Street food Da Nang",
    "Seafood Da Nang",
    "Vegan Da Nang",
    "Coffee Da Nang",
    "Bars in Da Nang",
    "Nightlife Da Nang",
]

# Xuất ra file txt và json để tiện dùng
import json
import os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
output_dir = os.path.join(base_dir, "data")
os.makedirs(output_dir, exist_ok=True)


with open(os.path.join(output_dir, "keywords_danang.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(keywords))

with open(os.path.join(output_dir, "keywords_danang.json"), "w", encoding="utf-8") as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

# "/data/keywords_danang.txt", "/data/keywords_danang.json"
# python3 init_keyword.py