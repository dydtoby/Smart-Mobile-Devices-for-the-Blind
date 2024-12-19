import base64

import requests


def encode_image():
    with open("thing.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



OPENAI_API_KEY = "fk197886-MLzC4JoWjKlJDFoGBaNo713b03Nwk0bu"

ENDPOINT = "https://oa.api2d.net/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}
messages = [{"role": "system", "content": "你盲人导盲助手，分析图片告知物品信息"}]


def thing_chat(res_):
    # Getting the base64 string
    base64_image = encode_image()
    data = {
        "model": "gpt-4-vision-preview",
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
    for _ in range(5):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=data, timeout=10)
            response.raise_for_status()  # 检查响应状态码
            response_text = response.json()['choices'][0]['message']['content']
            response_text = response_text.replace("\n", "")
            return response_text
        except requests.exceptions.Timeout:
            print("请求超时，未在5秒内收到响应")
        except requests.exceptions.RequestException as e:
            print(f"请求发生异常: {e}")

    return "请求失败，已尝试三次"
