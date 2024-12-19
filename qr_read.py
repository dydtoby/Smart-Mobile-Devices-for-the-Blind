import sqlite3
import cv2
from pyzbar.pyzbar import decode


def read_qr_code():
    try:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            barcodes = decode(frame)
            cv2.imshow('Barcodes', frame)
            if barcodes:
                qr_code_data = barcodes[0].data.decode('utf-8')
                print(qr_code_data)
                cap.release()
                cv2.destroyAllWindows()
                return qr_code_data
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        print("No barcodes detected")
        return "未检测到二维码"
    except:
        return "读取二维码信息失败"


def insert_item(item_id, content):
    try:
        conn = sqlite3.connect('items.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (item_id, content) VALUES (?, ?)", (item_id, content))
        conn.commit()
        conn.close()
        return "物品信息已成功存入数据库"
    except:
        return "存入数据库失败,未寻找到二维码"


def read_item(item_id):
    try:
        conn = sqlite3.connect('items.db')
        c = conn.cursor()
        c.execute("SELECT content FROM items WHERE item_id=?", (item_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
        else:
            return "未找到对应物品信息"
    except:
        return "读取数据库失败"