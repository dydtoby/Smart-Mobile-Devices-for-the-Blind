import sqlite3
import face_recognition
import cv2
import numpy as np
from pyzbar.pyzbar import decode


# def add_face_name(name):
#     try:
#         conn = sqlite3.connect('faces.db')
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS faces
#                      (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
#         image = cv2.imread('add.jpg')
#         face_encoding = face_recognition.face_encodings(image)[0]
#         face_encoding_np = np.array(face_encoding)
#         c.execute("INSERT INTO faces (name, face_data) VALUES (?, ?)", (name, face_encoding_np))
#         conn.commit()
#         conn.close()
#         return "添加:" + name + "成功"
#     except:
#         return "添加:" + name + "失败"


def add_face_name(name):
    try:
        conn = sqlite3.connect('faces.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS faces
                     (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
        cap = cv2.VideoCapture(0)
        frame_count = 0

        while frame_count < 100:
            ret, frame = cap.read()
            face_encoding = face_recognition.face_encodings(frame)
            if len(face_encoding) > 0 and frame_count > 10:
                face_encoding_np = np.array(face_encoding)
                c.execute("INSERT INTO faces (name, face_data) VALUES (?, ?)", (name, face_encoding_np.tobytes()))
                conn.commit()
                conn.close()
                cap.release()
                cv2.destroyAllWindows()
                return "添加:" + name + "成功"

            frame_count += 1
            cv2.imshow('Barcodes', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        conn.close()
        cap.release()
        cv2.destroyAllWindows()
        return "添加:" + name + "失败"

    except Exception as e:
        print(e)
        return "添加11:" + name + "失败"


# def read_face_name():
#     try:
#         conn = sqlite3.connect('faces.db')
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS faces
#                      (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
#         c.execute("SELECT name, face_data FROM faces")
#         rows = c.fetchall()
#
#         image = cv2.imread('add.jpg')
#         face_encoding = face_recognition.face_encodings(image)[0]
#         face_encoding_np = np.array(face_encoding)
#         for row in rows:
#             stored_face_encoding = np.frombuffer(row[1])
#             if np.array_equal(face_encoding_np, stored_face_encoding):
#                 conn.close()
#                 return row[0]
#         conn.close()
#         return "NONE"
#     except:
#         return "NONE"


def read_face_name():
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces
                 (id INTEGER PRIMARY KEY, name TEXT, face_data BLOB)''')
    c.execute("SELECT name, face_data FROM faces")
    rows = c.fetchall()
    cap = cv2.VideoCapture(0)
    consecutive_failures = 0

    while True:
        ret, frame = cap.read()
        face_encodings = face_recognition.face_encodings(frame)
        if len(face_encodings) > 0 and consecutive_failures > 10:
            for row in rows:
                conn.close()
                cap.release()
                cv2.destroyAllWindows()
                return row[0]
        cv2.imshow('Barcodes', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        consecutive_failures += 1
        if consecutive_failures == 100:
            conn.close()
            cap.release()
            cv2.destroyAllWindows()
            return "NONE"


def delete_all_faces():
    try:
        conn = sqlite3.connect('faces.db')
        c = conn.cursor()
        c.execute("DELETE FROM faces")
        conn.commit()
        conn.close()
        return "所有人脸已删除"
    except:
        return "删除失败"

# print(delete_all_faces())
