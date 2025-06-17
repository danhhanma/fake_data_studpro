import requests
import random
import threading

# === Đọc dữ liệu từ file ===
with open("mongmuon.txt", "r", encoding="utf-8") as f:
    momuon_list = [line.strip() for line in f if line.strip()]

# ==== Dữ liệu mẫu ====
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

# ==== Logic thich ====
def chon_thich_options():
    if random.random() < 0.6:
        return [
            "Các bài học thử thách (bài thực hành)",
            "Các bài học dạng video",
            "Sự tận tâm, tâm huyết"
        ]
    else:
        return random.sample(thich_all, k=random.randint(1, 5))

# ==== Logic khong thich ====
def chon_khong_thich():
    if random.random() < 0.7:
        other = [opt for opt in khong_thich_all if opt != "Bài tập hơi ít"]
        return ["Bài tập hơi ít"] + random.sample(other, k=random.randint(0, 2))
    else:
        return random.sample(khong_thich_all, k=random.randint(1, 3))

# ==== Hàm gửi 1 request ====
def send_request():
    payload = {
        "entry.1524771023": str(random.randint(4, 5)),
        "entry.1594930872": random.choice(momuon_list),
        "entry.366340186": chon_thich_options(),
        "entry.1122798691": chon_khong_thich()
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSeFJ1jC2uxepvB4FUpgFfeck5M5OeGyiAZT5hKwpJFFGGEABw/formResponse"

    def flatten(data):
        result = {}
        for key, value in data.items():
            if isinstance(value, list):
                for v in value:
                    result.setdefault(key, []).append(v)
            else:
                result[key] = value
        return result

    response = requests.post(url, data=flatten(payload), headers=headers)
    if response.ok:
        print("✅ Thành công")
    else:
        print("❌ Lỗi:", response.status_code)

# ==== Hàm chạy trong từng luồng ====
def worker(n):
    for _ in range(n):
        send_request()

# ==== Nhập từ bàn phím ====
total_requests = int(input("Nhập tổng số lần gửi: "))
num_threads = int(input("Nhập số luồng: "))

requests_per_thread = total_requests // num_threads
threads = []

for i in range(num_threads):
    t = threading.Thread(target=worker, args=(requests_per_thread,))
    threads.append(t)
    t.start()

# Nếu tổng không chia hết, gửi phần còn lại
for _ in range(total_requests % num_threads):
    send_request()

# Đợi tất cả luồng kết thúc
for t in threads:
    t.join()

print("🎉 Hoàn tất gửi tất cả request.")
