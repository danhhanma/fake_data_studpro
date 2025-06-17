import requests
import random

# Hàm chọn ngẫu nhiên có trọng số
def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]

# === Đọc dữ liệu từ file ===
with open("data/truong.txt", "r", encoding="utf-8") as f:
    truong_list = [line.strip() for line in f if line.strip()]

with open("data/lydo.txt", "r", encoding="utf-8") as f:
    ly_do_list = [line.strip() for line in f if line.strip()]

# === Trọng số trường học ===
target_truong = "Đại học Công nghệ thông tin và Truyền thông Việt Hàn"
truong_weighted = [(truong, 50 if truong == target_truong else 1) for truong in truong_list]
truong_duoc_chon = weighted_choice(truong_weighted)

# === Trọng số ngành học ===
nganh_chon = weighted_choice([
    ("Công nghệ thông tin", 50),
    ("Kinh tế", 20),
    ("Kỹ thuật", 20),
    ("Khoa học xã hội", 10)
])

# === Giờ học trung bình ===
gio_hoc = weighted_choice([
    ("Dưới 1 giờ", 20),
    ("2 - 3 giờ", 60),
    ("Trên 4 giờ", 20)
])

# === Khó khăn học tập (chọn 2) ===
kho_khan = random.sample([
    "Không hiểu bài giảng trên lớp",
    "Thiếu tài liệu tham khảo",
    "Khó khăn trong việc quản lý thời gian",
    "Không có ai hỗ trợ, giải đáp thắc mắc"
], k=2)

# === Dịch vụ hỗ trợ (chọn 1–3) ===
loai_dv = random.sample([
    "Gia sư trực tiếp",
    "Gia sư trực tuyến (Zoom, Google Meet, v.v.)",
    "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
    "Dịch vụ hỗ trợ làm bài tập thuê"
], k=random.randint(1, 3))

# === Nhược điểm của dịch vụ (chọn 1–3) ===
nhuoc_diem = random.sample([
    "Chi phí cao",
    "Chất lượng không ổn định",
    "Thời gian phản hồi chậm",
    "Không đúng nội dung yêu cầu",
    "Thiếu minh bạch về nguồn tài liệu"
], k=random.randint(1, 3))

# === Lý do cá nhân (1 dòng từ file) ===
ly_do_chon = random.choice(ly_do_list)

# === Google Form URL ===
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfQbEigp7UPTQoiR5b_tSCeJVeo6tFojgNseV8UJTEA0S0riw/formResponse"

# === Payload gửi đi ===
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

# === Hàm flatten để xử lý list (checkbox) ===
def flatten(data):
    result = {}
    for k, v in data.items():
        if isinstance(v, list):
            for item in v:
                result.setdefault(k, []).append(item)
        else:
            result[k] = v
    return result

# === Gửi request ===
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0"
}

response = requests.post(url, data=flatten(payload), headers=headers)

# === Phản hồi ===
if response.ok:
    print("✅ Gửi thành công:", truong_duoc_chon)
else:
    print("❌ Gửi lỗi:", response.status_code)
    print(response.text)
