import requests
import time

# Endpoint gốc của Google Form
url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfQbEigp7UPTQoiR5b_tSCeJVeo6tFojgNseV8UJTEA0S0riw/formResponse"

# Thời gian timestamp thực tế
timestamp = int(time.time() * 1000)
fbzx = "3633689863012893725"  # giữ nguyên nếu không thay đổi form
partial = f"[null,null,\"{fbzx}\"]"

# Payload đầy đủ
payload = {
    "entry.366340186": "Đại học Công nghệ - ĐHQG Hà Nội",
    "entry.2054599017": "Thiếu ngủ",
    "entry.507281624": [
        "Gia sư trực tiếp",
        "Gia sư trực tuyến (Zoom, Google Meet, v.v.)",
        "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)",
        "Dịch vụ hỗ trợ làm bài tập thuê"
    ],
    "entry.1283381215": "Công nghệ thông tin",
    "entry.1732692189": "Trên 4 giờ",
    "entry.1628223057": [
        "Không hiểu bài giảng trên lớp",
        "Thiếu tài liệu tham khảo",
        "Khó khăn trong việc quản lý thời gian",
        "Không có ai hỗ trợ, giải đáp thắc mắc"
    ],
    "entry.1701307417": "rồi",
    "entry.196439037": "rồi",
    "entry.2020520532": [
        "Chi phí cao",
        "Chất lượng không ổn định",
        "Thời gian phản hồi chậm",
        "Không đúng nội dung yêu cầu",
        "Thiếu minh bạch về nguồn tài liệu"
    ],

}

# Hàm flatten form cho checkbox
def flatten(data):
    result = {}
    for k, v in data.items():
        if isinstance(v, list):
            for item in v:
                result.setdefault(k, []).append(item)
        else:
            result[k] = v
    return result

# Headers mô phỏng form
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0"
}

# Gửi POST request
response = requests.post(url, data=flatten(payload), headers=headers)

# Kết quả
if response.status_code == 200:
    print("✅ Gửi thành công.")
else:
    print("❌ Gửi lỗi:", response.status_code)
    print(response.text)
