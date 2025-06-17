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

# ==== Gửi request đơn ====
def send_request(i):
    payload = {
        "entry.1524771023": str(random.randint(4, 5)),  # đánh giá sao
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

    try:
        response = requests.post(url, data=flatten(payload), headers=headers)
        if response.ok:
            print(f"✅ Thành công [{i}]")
        else:
            print(f"❌ Lỗi [{i}]: {response.status_code}")
    except Exception as e:
        print(f"❌ Ngoại lệ [{i}]: {e}")

# ==== Hàm chạy luồng ====
def worker(start_idx, count):
    for i in range(start_idx, start_idx + count):
        send_request(i)

# ==== Nhập số lượng request & luồng ====
total_requests = int(input("Nhập tổng số lần gửi: "))
num_threads = int(input("Nhập số luồng: "))

requests_per_thread = total_requests // num_threads
threads = []

# Khởi tạo các luồng chính
for i in range(num_threads):
    start_index = i * requests_per_thread
    t = threading.Thread(target=worker, args=(start_index, requests_per_thread))
    threads.append(t)
    t.start()

# Gửi phần dư (nếu không chia hết)
for i in range(total_requests % num_threads):
    send_request(num_threads * requests_per_thread + i)

# Đợi tất cả luồng kết thúc
for t in threads:
    t.join()

print("🎉 Hoàn tất gửi tất cả request.")
