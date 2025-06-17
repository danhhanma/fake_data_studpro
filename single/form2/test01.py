import requests
import random

# === Thông tin form ===
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeFJ1jC2uxepvB4FUpgFfeck5M5OeGyiAZT5hKwpJFFGGEABw/formResponse"

# ==== Tùy chọn dữ liệu ====
all_thich = [
    "Các bài học thử thách (bài thực hành)",
    "Các bài học dạng video",
    "Giọng nói người giảng hay",
    "Dịch vụ hỗ trợ làm bài tập thuê",
    "Âm thanh to rõ ràng, hình ảnh sắc nét",
    "Sự tận tâm, tâm huyết"
]

must_thich = [
    "Các bài học thử thách (bài thực hành)",
    "Các bài học dạng video",
    "Sự tận tâm, tâm huyết"
]

khong_thich_all = [
    "Bài tập hơi ít",
    "Tính năng ghi chú",
    "Các bài học thử thách (bài thực hành)"
]

mong_muon_list = [
    "Tôi mong muốn có thêm chức năng luyện nói với AI.",
    "Cần nhiều đề thi mô phỏng hơn.",
    "Muốn có phần luyện phản xạ thực tế.",
    "Thêm giáo viên chấm chữa bài tự động."
]

# ==== Chọn dữ liệu theo tỉ lệ ====
# THÍCH
def chon_thich():
    if random.random() < 0.6:
        return must_thich
    else:
        other = list(set(all_thich) - set(must_thich))
        return random.sample(other, k=random.randint(1, min(len(other), 5)))

# KHÔNG THÍCH
def chon_khong_thich():
    if random.random() < 0.7:
        return ["Bài tập hơi ít"]
    else:
        other = list(set(khong_thich_all) - {"Bài tập hơi ít"})
        return random.sample(other, k=random.randint(1, min(len(other), 3)))

# MONG MUỐN
def chon_mong_muon():
    return random.choice(mong_muon_list)

# ==== Tạo payload ====
payload = {
    "entry.1524771023": str(random.randint(4, 5)),  # Đánh giá 4–5 sao
    "entry.1594930872": chon_mong_muon(),
    "entry.366340186": chon_thich(),
    "entry.1122798691": chon_khong_thich()
}

# ==== Gửi request ====
def flatten(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            for v in value:
                result.setdefault(key, []).append(v)
        else:
            result[key] = value
    return result

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
