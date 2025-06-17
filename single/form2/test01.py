import requests
import random
import time

# === Thông tin form ===
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeFJ1jC2uxepvB4FUpgFfeck5M5OeGyiAZT5hKwpJFFGGEABw/formResponse"

# ==== Tùy chọn dữ liệu ====
thich_options = [
    "Các bài học thử thách (bài thực hành)",
    "Các bài học dạng video",
    "Giọng nói người giảng hay",
    "Dịch vụ hỗ trợ làm bài tập thuê",
    "Âm thanh to rõ ràng, hình ảnh sắc nét",
    "Sự tận tâm, tâm huyết"
]

khong_thich_options = [
    "Bài tập hơi ít",
    "Tính năng ghi chú",
    "Các bài học thử thách (bài thực hành)"
]

mong_muon = [
    "Tôi mong muốn có thêm chức năng luyện nói với AI.",
    "Cần nhiều đề thi mô phỏng hơn.",
    "Muốn có phần luyện phản xạ thực tế.",
    "Thêm giáo viên chấm chữa bài tự động."
]

# ==== Tạo payload ====
payload = {
    "entry.1524771023": str(random.randint(4, 5)),  # Đánh giá 4 hoặc 5 sao
    "entry.1594930872": random.choice(mong_muon),
    "entry.366340186": random.sample(thich_options, k=random.randint(2, 4)),
    "entry.1122798691": random.sample(khong_thich_options, k=random.randint(1, 2))
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
