import requests
import random
import time
import threading
from collections import defaultdict

# ======= LINK GOOGLE FORM =======
url = "https://docs.google.com/forms/d/e/1FAIpQLSctEUiLH2MF18-Ramw9ui6rd_7ugRTJEKjUmmECdBw6tazPiA/formResponse"

# ======= ĐỌC FILE =======
def load_emotions_from_file(filepath="../data/camxuc.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Bình thường"]

def load_schools_from_file(filepath="../data/truong.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            schools = [line.strip() for line in f if line.strip()]
            schools += ["Đại học Công nghệ thông tin và Truyền thông Việt Hàn"] * 4  # Ưu tiên 20%
            return schools
    except:
        return ["Đại học không xác định"]

def load_mongmuon_from_file(filepath="../data/mongmuon.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Có AI", "Tự động chấm điểm", "Học dễ hiểu hơn"]

# ======= HÀM CHỌN TỶ LỆ =======
def weighted_choice(choices):
    items, weights = zip(*choices)
    return random.choices(items, weights=weights, k=1)[0]

# ======= DỮ LIỆU CÁC FIELD =======
form_data_options = {
    "entry.1832209893": [
        "Làm bài dễ hơn", "Làm nhanh", "Hiểu bài hơn", "Không còn sợ môn học khó nữa",
        "Tự tin hơn khi làm bài kiểm tra", "Biết cách tự học hiệu quả hơn", "Nắm vững kiến thức nền tảng",
        "Làm bài tập về nhà nhanh hơn", "Dễ tập trung hơn khi học một mình", "Không còn mất thời gian tìm tài liệu nữa"
    ],
    "entry.1923033527": [
        "Không hiểu bài", "Thiếu tài liệu", "Không ai hướng dẫn", "Khó khăn trong việc tự học",
        "Thời gian học tập hạn chế", "Không có động lực học tập", "Môi trường học tập không phù hợp",
        "Khó khăn trong việc ghi nhớ kiến thức", "Không biết cách ôn tập hiệu quả",
        "Khó khăn trong việc làm bài tập", "Không có phương pháp học phù hợp",
        "Khó khăn trong việc tập trung", "Không có kế hoạch học tập rõ ràng"
    ],
    "entry.1582763207": ["GPT", "ChatGPT", "StudyPro", "Google"],
    "entry.308541725": load_mongmuon_from_file(),
    "entry.825945663": ["18 đến 24", "hơn 24"],
    "entry.244821263": ["Năm 1", "Năm 2", "Năm 3", "Năm 4 trở lên"],
    "entry.1471884202": [
        "Rất hiệu quả", "Khá hiệu quả", "Bình thường", "Không hiệu quả", "Hoàn toàn không hiệu quả",
        "Cực kỳ hiệu quả - Thay đổi hoàn toàn cách học của tôi", "Hiệu quả vượt trội - Kết quả học tập cải thiện rõ rệt",
        "Hiệu quả đáng kinh ngạc - Điểm số tăng vọt", "Hiệu quả tuyệt vời - Tiết kiệm được rất nhiều thời gian",
        "Hiệu quả xuất sắc - Giúp tôi đạt được mục tiêu học tập", "Hiệu quả đột phá - Thay đổi hoàn toàn cách tiếp cận môn học",
        "Hiệu quả vượt mong đợi - Kết quả vượt xa dự kiến", "Hiệu quả đáng ngạc nhiên - Không ngờ lại tốt đến thế",
        "Hiệu quả đáng kinh ngạc - Thay đổi hoàn toàn kết quả học tập", "Hiệu quả tuyệt đối - Không thể tốt hơn được nữa"
    ],
    "entry.1617008414": [
        "Không hiểu bài giảng trên lớp", "Thiếu tài liệu tham khảo",
        "Khó khăn trong việc quản lý thời gian", "Không có ai hỗ trợ giải đáp thắc mắc"
    ],
    "entry.1572115899": [
        "Gia sư trực tiếp", "Gia sư trực tuyến (Zoom, Google Meet, v.v.)",
        "Các nền tảng hỗ trợ học tập (VD: Gauth,QANDA,...)", "Dịch vụ hỗ trợ làm bài tập thuê"
    ],
    "entry.1661385998": [
        "Chi phí cao", "Chất lượng không ổn định", "Thời gian phản hồi chậm",
        "Không đúng nội dung yêu cầu", "Giao bài trễ hoặc thiếu trách nhiệm", "Thiếu minh bạch về nguồn tài liệu"
    ],
    "entry.391096228": [
        "Hỗ trợ giải bài tập theo yêu cầu", "Hỗ trợ giảng dạy trực tuyến theo lịch hẹn",
        "Cung cấp tài liệu tham khảo chất lượng cao", "Hỗ trợ lập kế hoạch học tập và quản lý thời gian",
        "Hỗ trợ ôn thi và luyện đề", "Hỗ trợ kiểm tra đạo văn và chỉnh sửa bài viết"
    ]
}

# Các trường checkbox
checkbox_fields = [
    "entry.1617008414", "entry.1572115899", "entry.1661385998", "entry.391096228"
]

# ======= TẠO DỮ LIỆU GỬI FORM =======
def build_payload():
    payload = defaultdict(list)

    # Các trường có yêu cầu đặc biệt
    payload["entry.646024672"] = random.choice(load_emotions_from_file())
    payload["entry.518848497"] = random.choice(load_schools_from_file())

    payload["entry.1039331190"] = weighted_choice([
        ("Dưới 5 triệu/1 tháng", 0.4),
        ("5 đến 10 triệu/ 1 tháng", 0.4),
        ("10 đến 15 triệu/ 1 tháng", 0.1),
        ("Hơn 15 triệu/ 1 tháng", 0.1)
    ])

    payload["entry.2695913"] = weighted_choice([
        ("Công nghệ thông tin", 0.6),
        ("Kinh tế", 0.15),
        ("Kỹ thuật", 0.15),
        ("Khoa học xã hội", 0.1)
    ])

    payload["entry.1370622741"] = weighted_choice([
        ("Có", 0.75),
        ("Không", 0.25)
    ])

    payload["entry.1582810821"] = weighted_choice([
        ("Trên 4 giờ", 0.6),
        ("3-4 giờ", 0.15),
        ("1-2 giờ", 0.15),
        ("Dưới 1 giờ", 0.1)
    ])

    payload["entry.1030001769"] = weighted_choice([
        ("Rồi", 0.8),
        ("Chưa", 0.2)
    ])

    payload["entry.1660415676"] = weighted_choice([
        ("Dưới 100.000 VNĐ", 0.4),
        ("100.000 - 300.000 VNĐ", 0.4),
        ("300.000 - 500.000 VNĐ", 0.1),
        ("Trên 500.000 VNĐ", 0.1)
    ])

    payload["entry.853215687"] = weighted_choice([
        ("Có", 0.7),
        ("Tùy vào mức giá và chất lượng dịch vụ", 0.2),
        ("Không", 0.1)
    ])

    # Trường khó khăn — tỷ lệ thấp
    options = form_data_options["entry.1617008414"]
    k = min(len(options), random.choice([0, 1, 2]))
    selected = random.sample(options, k=k)
    payload["entry.1617008414"].extend(selected)

    # Các trường còn lại
    for entry_id, options in form_data_options.items():
        if entry_id in payload:
            continue
        if entry_id in checkbox_fields:
            k = min(len(options), random.randint(1, len(options)))
            selected = random.sample(options, k=k)
            payload[entry_id].extend(selected)
        else:
            payload[entry_id] = random.choice(options)

    return payload

# ======= GỬI FORM =======
def send_form(index):
    data = build_payload()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://docs.google.com',
        'Referer': 'https://docs.google.com/forms/d/e/1FAIpQLSctEUiLH2MF18-Ramw9ui6rd_7ugRTJEKjUmmECdBw6tazPiA/viewform'
    }
    try:
        res = requests.post(url, data=data, headers=headers)
        if res.status_code == 200:
            print(f"✅ Gửi #{index} thành công")
        else:
            print(f"❌ Gửi #{index} lỗi {res.status_code} — {res.reason}")
            print("Payload lỗi:", dict(data))
    except Exception as e:
        print(f"⚠️ Lỗi khi gửi #{index}: {e}")
    time.sleep(random.uniform(0.5, 2.0))

# ======= CHẠY CHÍNH =======
if __name__ == "__main__":
    total = int(input("Nhập số lượt gửi: "))
    threads = int(input("Nhập số luồng đồng thời: "))

    thread_list = []
    for i in range(total):
        t = threading.Thread(target=send_form, args=(i + 1,))
        thread_list.append(t)
        t.start()
        while threading.active_count() > threads:
            time.sleep(0.1)
    for t in thread_list:
        t.join()

    print("🎉 Hoàn tất gửi toàn bộ.")
