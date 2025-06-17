import requests
import random

# ===== Đọc dữ liệu từ file =====
with open("../data/mongmuon.txt", "r", encoding="utf-8") as f:
    momuon_list = [line.strip() for line in f if line.strip()]

# ==== Tùy chọn dữ liệu ====
thich_all = [
    "Các bài học thử thách (bài thực hành)",
    "Các bài học dạng video",
    "Giọng nói người giảng hay",
    "Dịch vụ hỗ trợ làm bài tập thuê",
    "Âm thanh to rõ ràng, hình ảnh sắc nét",
    "Sự tận tâm, tâm huyết"
]

khong_thich_all = [
    "Bài tập hơi ít",
    "Tính năng ghi chú",
    "Các bài học thử thách (bài thực hành)"
]

# ==== Logic thich_options ====
def chon_thich_options():
    if random.random() < 0.6:
        # 60% chọn đúng 3 mục ưu tiên
        return [
            "Các bài học thử thách (bài thực hành)",
            "Các bài học dạng video",
            "Sự tận tâm, tâm huyết"
        ]
    else:
        return random.sample(thich_all, k=random.randint(1, 5))

# ==== Logic khong_thich_options ====
def chon_khong_thich():
    if random.random() < 0.7:
        other = [opt for opt in khong_thich_all if opt != "Bài tập hơi ít"]
        return ["Bài tập hơi ít"] + random.sample(other, k=random.randint(0, 2))
    else:
        return random.sample(khong_thich_all, k=random.randint(1, 3))

# ==== Chuẩn bị payload ====
payload = {
    "entry.1524771023": str(random.randint(4, 5)),  # đánh giá 4 hoặc 5 sao
    "entry.1594930872": random.choice(momuon_list),
    "entry.366340186": chon_thich_options(),
    "entry.1122798691": chon_khong_thich()
}

# ==== Hàm flatten form ====
def flatten(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            for v in value:
                result.setdefault(key, []).append(v)
        else:
            result[key] = value
    return result

# ==== Gửi request ====
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeFJ1jC2uxepvB4FUpgFfeck5M5OeGyiAZT5hKwpJFFGGEABw/formResponse"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0"
}

response = requests.post(url, data=flatten(payload), headers=headers)

# ==== Kết quả ====
if response.ok:
    print("✅ Gửi thành công.")
else:
    print("❌ Gửi lỗi:", response.status_code)
    print(response.text)
