import base64
import requests


def encode_image():
    with open("road.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


OPENAI_API_KEY = "fk197886-MLzC4JoWjKlJDFoGBaNo713b03Nwk0bu"
# OPENAI_API_KEY = "sk-proj-F5SPRKyMXHbgnoiNnQpTT3BlbkFJcHA4jBCobm491y83jjR9"
ENDPOINT = "https://openai.api2d.net/v1/chat/completions"

# ENDPOINT = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}
messages = [{"role": "system", "content": "你盲人导盲助手，请分析图片位置和信息来用最简洁的语言回答问题以及告诉盲人方位信息"}]


def chat(res_):
    # Getting the base64 string
    base64_image = encode_image()
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": res_,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.1
    }
    print("hello")
    for _ in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=data, timeout=15)
            response.raise_for_status()  # 检查响应状态码
            response_text = response.json()['choices'][0]['message']['content']
            response_text = response_text.replace("\n", "")
            print(response_text)
            return response_text
        except requests.exceptions.Timeout:
            print("请求超时，未在5秒内收到响应")
        except requests.exceptions.RequestException as e:
            print(f"请求发生异常: {e}")

    return "请求失败，已尝试三次"

