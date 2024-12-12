# -*- coding:utf-8 -*-
"""
Created on  # 19:28  19:28
@author: hlink
"""
import subprocess
import wave
import requests
import pyaudio
import paho.mqtt.client as mqtt
from Text2Voice import text2voice
from aip import AipSpeech
import threading
import cv2
import time
from distance_py import ultrasonic_distance
API_KEY = "rqRB*****WbGjXw"
SECRET_KEY = "Sq*******7X6JK"
from face import add_face_name, read_face_name, delete_all_faces
from road_detect import chat
from thing_detect import thing_chat
from qr_read import insert_item, read_item, read_qr_code

import RPi.GPIO as GPIO
import time

TRIG=23
ECHO=24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

CHUNK = 1024  # 每次读取的音频数据大小
FORMAT = pyaudio.paInt16  # 音频数据格式为16位整数
CHANNELS = 1  # 单声道
RATE = 48000  # 采样率（每秒采样点数）
TARGET_RATE = 16000
RECORD_SECONDS = 5  # 录制时长
WAVE_OUTPUT_FILENAME = "recording.wav"  # 保存音频的文件名
FINAL_OUTPUT_FILENAME = "recording_16000.wav"
MAX_CONVERSATION = 3  #对话轮数
""" 你的 BAIDU APPID AK SK """
BD_APP_ID = '6******7'
BD_API_KEY = '*****'
BD_SECRET_KEY = 'rXz**********1kBdvZHn'

interrupted = False


def send_mqtt_message(topic, message):
    client = mqtt.Client()
    client.connect("hli****ce", 1883, 60)
    client.publish(topic, message)
    client.disconnect()


def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    if payload == "#1":  # 人脸识别
        play("snowboy/resources/ding.wav")
        read_face_()
    elif payload == "#2":
        play("snowboy/resources/ding.wav")
        around_read_()  #环境识别
    elif payload == "#3":
        play("snowboy/resources/ding.wav")
        chat_bot_main(conversation_list)


def mqtt_connect():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("hl****ace", 1*3)
    client.subscribe("4b_road")
    client.loop_forever()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))



def mic(record_seconds):
    p = pyaudio.PyAudio()
    # 打开麦克风输入流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    stream.volume = 1
    print("开始录制音频...")

    frames = []  # 用于存储音频帧数据

    # 读取音频数据并保存
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录制完成！")

    # 停止录制并关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存音频文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("音频保存为：" + WAVE_OUTPUT_FILENAME)
    #播放音频
    #os.system("aplay recording.wav")


def changeRate():
    # 使用FFmpeg降低采样频率
    command = [
        "ffmpeg",
        "-i", WAVE_OUTPUT_FILENAME,
        "-ar", str(TARGET_RATE),
        FINAL_OUTPUT_FILENAME,
        "-y"
    ]

    # 运行命令行
    subprocess.run(command, check=True)

    print("音频采样频率已降低为", TARGET_RATE)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def voice2Text():
    #根据语音调用百度的API获取文字
    client = AipSpeech(BD_APP_ID, BD_API_KEY, BD_SECRET_KEY)
    response = client.asr(get_file_content(FINAL_OUTPUT_FILENAME), 'pcm', 16000, {'dev_pid': ***, })
    print(response)

    result = response['result'][0]
    print(result)
    return result


def chatbaidu(conversation_list):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "messages": conversation_list
    }
    res = requests.request("POST", url, headers=headers, json=data).json()
    print(res)
    answer = res['result']
    print(answer)
    return answer


def play(save_file):
    command = [
        "aplay",
        save_file
    ]

    # 运行命令行
    subprocess.run(command, check=True)


def deleteAudio(save_file):
    command = [
        "rm",
        WAVE_OUTPUT_FILENAME,
        FINAL_OUTPUT_FILENAME,
        save_file
    ]
    subprocess.run(command, check=True)


def show_conversation(conversation_list):
    for msg in conversation_list:
        if msg['role'] == 'user':
            print(f"\U0001f47b: {msg['content']}\n")
        else:
            print(f"\U0001f47D: {msg['content']}\n")


# print(add_face_name("hlink"))
# print(read_face_name())
# print(chat("是否有盲道，以及盲道是否有障碍物"))
# print(thing_chat("桌面上有什么物品啊"))
# print(insert_item(read_qr_code("001.png"),"布洛芬缓释胶囊，一日一次一次三颗"))
# print(read_item(read_qr_code("001.png")))
# print(get_objects_by_position())
def take_photo(filename):
    # 打开相机
    cap = cv2.VideoCapture(0)
    # 检查相机是否成功打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    frame_count = 0
    while True:
        ret, frame = cap.read()
        # cv2.imshow('frame', frame)
        frame_count += 1
        if frame_count == 10:
            break
    # 保存照片到本地文件
    cv2.imwrite(filename, frame)
    # 释放相机资源
    cap.release()
    cv2.destroyAllWindows()


def add_face_():
    take_photo('add.jpg')
    save_file = text2voice("请在叮声后说出人脸名称")
    play(save_file)
    play("snowboy/resources/ding.wav")
    mic(3)
    changeRate()
    question = voice2Text()
    res = text2voice(add_face_name(question))
    play(res)


def read_face_():
    take_photo('add.jpg')
    play("snowboy/resources/ding.wav")
    res = text2voice("面前人脸是" + read_face_name())
    play(res)


def around_read_():
    take_photo('road.jpg')
    question = "最简短的语句描述人物或物体的方位"
    print(question)
    res = text2voice(chat(str(question)))
    play(res)


def chat_bot_main(conversation_list=[]):
    record_seconds = 3
    mic(record_seconds)
    changeRate()
    question = voice2Text()
    if "read" in question:
        read_face_()

    elif "add" in question:
        add_face_()

    elif "read around" in question:
        around_read_()
    elif "open light" in question:
        print("openlight")
        send_mqtt_message("#6")
    elif "close light" in question:
        print("closelight")
        send_mqtt_message("#7") 
    elif "open fan" in question:
        print("openfan")
        send_mqtt_message("#8")
    elif "close the fan" in question:
        print("closefan")
        send_mqtt_message("#9")
    else:
        conversation_list.append({"role": "user", "content": question})
        answer = chatbaidu(conversation_list)
        # print(answer)
        conversation_list.append({"role": "assistant", "content": answer})
        show_conversation(conversation_list)
        save_file = text2voice(answer)
        play(save_file)
        deleteAudio(save_file)
        if len(conversation_list) > 2 * MAX_CONVERSATION:
            # 删除前两个元素
            del conversation_list[:2]
            # 添加两个新元素

def send_mqtt_message(message):
    client = mqtt.Client()
    client.connect("hlin***ce", 1**3, **)
    client.publish("4b_road", message)
    client.disconnect()
    

def voice_detection():
    while True:
        time.sleep(1)
        try:
            dist = distance()
            if dist <=50:
                send_mqtt_message("#10")
            else:
                send_mqtt_message("#11")
            print(dist)
        except:
            print("error")


if __name__ == "__main__":
    conversation_list=[]
    voice_thread = threading.Thread(target=voice_detection)
    mqtt_thread = threading.Thread(target=mqtt_connect)

    voice_thread.start()
    mqtt_thread.start()
