import requests

API_KEY = "AIzaSyDSsNrspI5UsLi5ia6TIekdF79NARn9rIg"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# Khởi tạo hội thoại
conversation = []

while True:
    user_input = input("Bạn: ")
    if user_input.lower() == "exit":
        break

    # Thêm câu hỏi người dùng
    conversation.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    # Gửi API
    response = requests.post(url, headers=headers, json={"contents": conversation})
    res_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    print("Gemini:", res_text)

    # Thêm phản hồi vào lịch sử
    conversation.append({
        "role": "model",
        "parts": [{"text": res_text}]
    })
