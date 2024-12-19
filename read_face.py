import sqlite3
import face_recognition
import cv2
import numpy as np


def read_face_name():
    try:
        conn = sqlite3.connect('faces.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS faces
                     (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
        image = cv2.imread('add.jpg')
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encoding_np = np.array(face_encoding)
        c.execute("SELECT name, face_data FROM faces")
        rows = c.fetchall()
        for row in rows:
            stored_face_encoding = np.frombuffer(row[1])
            if np.array_equal(face_encoding_np, stored_face_encoding):
                conn.close()
                return row[0]
        conn.close()
        return "NONE"
    except:
        return "NONE"
