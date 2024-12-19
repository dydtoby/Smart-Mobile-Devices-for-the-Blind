import sqlite3
import face_recognition
import cv2
import numpy as np


def add_face_name(name):
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces
                 (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
    image = cv2.imread('add.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encoding = face_recognition.face_encodings(image)[0]
    face_encoding_np = np.array(face_encoding)
    c.execute("INSERT INTO faces (name, face_data) VALUES (?, ?)", (name, face_encoding_np))
    conn.commit()
    conn.close()
    return "添加:" + name + "成功"


print(add_face_name("hlink"))
