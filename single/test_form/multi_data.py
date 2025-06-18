import requests
import random
import threading
import time
import json

# === Hàm chọn ngẫu nhiên có trọng số ===
def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]

# === Đọc dữ liệu từ file JSON và TXT ===
with open("../data/truong_nganh.json", "r", encoding="utf-8") as f:
    truong_theo_nganh = json.load(f)

with open("../data/ly_do.txt", "r", encoding="utf-8") as f:
    ly_do_list = [line.strip() for line in f if line.strip()]

# === Map ngành nội bộ → ngành hiển thị đúng form ===
map_nganh_hien_thi = {
    "CNTT": "Công nghệ thông tin",
    "Kinh tế": "Kinh tế",
    "KHXH": "Khoa học xã hội",
    "Kỹ thuật": "Kỹ thuật"
}

# === Hàm chọn khó khăn học tập ===
def chon_kho_khan():
    roll = random.random()
    if roll < 0.7:
        phu = random.choice([
            "Thiếu tài liệu tham khảo",
            "Không có ai hỗ trợ, giải đáp thắc mắc"
        ])
        return ["Không hiểu bài giảng trên lớp", phu]
    else:
        return random.sample([
            "Không hiểu bài giảng trên lớp",
            "Thiếu tài liệu tham khảo",
            "Khó khăn trong việc quản lý thời gian",
            "Không có ai hỗ trợ, giải đáp thắc mắc"
        ], 2)

# === Hàm chọn loại dịch vụ ===
def chon_loai_dv():
    roll = random.random()
    if roll < 0.7:
        return [
            "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
        ]
    else:
        all_dv = [
            "Gia sư trực tiếp",
            "Gia sư trực tuyến (Zoom, Google Meet, v.v.)",
            "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
            "Dịch vụ hỗ trợ làm bài tập thuê"
        ]
        return random.sample(all_dv, k=random.randint(1, 3))

# === Hàm chọn nhược điểm ===
def chon_nhuoc_diem():
    roll = random.random()
    all_options = [
        "Chi phí cao",
        "Chất lượng không ổn định",
        "Thời gian phản hồi chậm",
        "Không đúng nội dung yêu cầu",
        "Thiếu minh bạch về nguồn tài liệu"
    ]
    if roll < 0.7:
        return ["Chi phí cao"]
    else:
        return random.sample(all_options, k=random.randint(1, 4))

# === Hàm flatten checkbox ===
def flatten(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            for v in value:
                result.setdefault(key, []).append(v)
        else:
            result[key] = value
    return result

# === Hàm gửi 1 form ===
def gui_form(index):
    try:
        # Chọn ngành (dạng code nội bộ)
        nganh_code = weighted_choice([
            ("CNTT", 50),
            ("Kinh tế", 20),
            ("Kỹ thuật", 20),
            ("KHXH", 10)
        ])
        nganh_hien_thi = map_nganh_hien_thi[nganh_code]

        # Chọn trường tương ứng với ngành
        target_truong = "Đại học Công nghệ thông tin và Truyền thông Việt Hàn"
        truong_list = truong_theo_nganh[nganh_code]
        truong_weighted = [(truong, 20 if truong == target_truong else 10) for truong in truong_list]
        truong_duoc_chon = weighted_choice(truong_weighted)

        gio_hoc = weighted_choice([
            ("Dưới 1 giờ", 20),
            ("2 - 3 giờ", 60),
            ("Trên 4 giờ", 20)
        ])

        kho_khan = chon_kho_khan()
        loai_dv = chon_loai_dv()
        nhuoc_diem = chon_nhuoc_diem()
        ly_do_chon = random.choice(ly_do_list)

        url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSe38wYQkDQPlxPAq7nFgRRm12m80gA_Qt5dD0ykDy0H6WmW5w/formResponse"

        payload = {
            "entry.366340186": truong_duoc_chon,
            "entry.1283381215": nganh_hien_thi,
            "entry.1732692189": gio_hoc,
            "entry.1628223057": kho_khan,
            "entry.2054599017": ly_do_chon,
            "entry.1701307417": "chưa" if random.random() < 0.9 else "rồi",
            "entry.196439037": "rồi" if random.random() < 0.9 else "chưa",
            "entry.507281624": loai_dv,
            "entry.2020520532": nhuoc_diem
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(url, data=flatten(payload), headers=headers)
        if response.ok:
            print(f"✅ [#{index+1}] Gửi thành công: {truong_duoc_chon} - {nganh_hien_thi}")
        else:
            print(f"❌ [#{index+1}] Lỗi {response.status_code}")
    except Exception as e:
        print(f"⚠️ [#{index+1}] Lỗi: {e}")

# === Nhập số lần gửi và số luồng ===
try:
    so_lan = int(input("Nhập số lần gửi: "))
    so_luong_luong = int(input("Nhập số luồng: "))
except:
    print("❌ Bạn phải nhập số nguyên.")
    exit()

# === Tạo worker cho từng batch gửi ===
def worker(batch):
    for i in batch:
        gui_form(i)

tasks = list(range(so_lan))
batch_size = (so_lan + so_luong_luong - 1) // so_luong_luong
threads = []

for i in range(so_luong_luong):
    batch = tasks[i * batch_size : (i + 1) * batch_size]
    if not batch:
        continue
    t = threading.Thread(target=worker, args=(batch,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
