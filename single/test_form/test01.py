import requests
import random

# Hàm chọn ngẫu nhiên có trọng số
def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]

# === Đọc dữ liệu từ file ===
with open("../data/truong.txt", "r", encoding="utf-8") as f:
    truong_list = [line.strip() for line in f if line.strip()]

with open("../data/ly_do.txt", "r", encoding="utf-8") as f:
    ly_do_list = [line.strip() for line in f if line.strip()]

# Trọng số trường học
target_truong = "Đại học Công nghệ thông tin và Truyền thông Việt Hàn"
truong_weighted = [(truong, 50 if truong == target_truong else 1) for truong in truong_list]
truong_duoc_chon = weighted_choice(truong_weighted)

# Ngành học
nganh_chon = weighted_choice([
    ("Công nghệ thông tin", 50),
    ("Kinh tế", 20),
    ("Kỹ thuật", 20),
    ("Khoa học xã hội", 10)
])

# Giờ học
gio_hoc = weighted_choice([
    ("Dưới 1 giờ", 20),
    ("2 - 3 giờ", 60),
    ("Trên 4 giờ", 20)
])

# --- Khó khăn học tập ---
def chon_kho_khan():
    roll = random.random()
    if roll < 0.7:
        # 70% ưu tiên "Không hiểu bài", + 1 trong 2
        phu = random.choice([
            "Thiếu tài liệu tham khảo",
            "Không có ai hỗ trợ, giải đáp thắc mắc"
        ])
        return ["Không hiểu bài giảng trên lớp", phu]
    else:
        # 30% chọn ngẫu nhiên 2 lý do bất kỳ
        return random.sample([
            "Không hiểu bài giảng trên lớp",
            "Thiếu tài liệu tham khảo",
            "Khó khăn trong việc quản lý thời gian",
            "Không có ai hỗ trợ, giải đáp thắc mắc"
        ], 2)

kho_khan = chon_kho_khan()

# Loại dịch vụ hỗ trợ
def chon_loai_dv():
    roll = random.random()
    if roll < 0.7:
        return [
            "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
            "Dịch vụ hỗ trợ làm bài tập thuê"
        ]
    else:
        all_dv = [
            "Gia sư trực tiếp",
            "Gia sư trực tuyến (Zoom, Google Meet, v.v.)",
            "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
            "Dịch vụ hỗ trợ làm bài tập thuê"
        ]
        return random.sample(all_dv, k=random.randint(1, 3))

loai_dv = chon_loai_dv()

# Nhược điểm dịch vụ
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
        return ["Chi phí cao", "Chất lượng không ổn định"]
    else:
        return random.sample(all_options, k=random.randint(1, 4))

nhuoc_diem = chon_nhuoc_diem()

# Lý do tự do
ly_do_chon = random.choice(ly_do_list)

# Gửi form
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfQbEigp7UPTQoiR5b_tSCeJVeo6tFojgNseV8UJTEA0S0riw/formResponse"

payload = {
    "entry.366340186": truong_duoc_chon,
    "entry.1283381215": nganh_chon,
    "entry.1732692189": gio_hoc,
    "entry.1628223057": kho_khan,
    "entry.2054599017": ly_do_chon,
    "entry.1701307417": "rồi",
    "entry.196439037": "rồi",
    "entry.507281624": loai_dv,
    "entry.2020520532": nhuoc_diem
}

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

if response.ok:
    print("✅ Gửi thành công:", truong_duoc_chon)
else:
    print("❌ Gửi lỗi:", response.status_code)
    print(response.text)