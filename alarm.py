import csv
import time
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import QTime, QTimer
from Text2Voice import text2voice
def play(save_file):
    command = [
        "aplay",
        save_file
    ]

    # 运行命令行
    subprocess.run(command, check=True)
class AlarmClock(QWidget):
    def __init__(self):
        super().__init__()
        self.alarm_times = []
        self.init_ui()
        self.read_alarm_times()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alarm)
        self.timer.start(1000)  # Check every minute

    def init_ui(self):
        self.setWindowTitle('Alarm Clock')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Add Alarm Time (HH:MM):')
        self.edit = QLineEdit()
        self.button_add = QPushButton('Add Alarm')
        self.button_add.clicked.connect(self.add_alarm)

        self.button_delete = QPushButton('Delete All Alarms')
        self.button_delete.clicked.connect(self.delete_alarms)

        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def add_alarm(self):
        alarm_time = self.edit.text()
        if alarm_time:
            self.alarm_times.append(alarm_time)
            with open('alarm_times.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([alarm_time])
            self.edit.clear()

    def delete_alarms(self):
        self.alarm_times = []
        open('alarm_times.csv', 'w').close()

    def read_alarm_times(self):
        with open('alarm_times.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.alarm_times.append(row[0])

    def check_alarm(self):
        current_time = QTime.currentTime().toString('HH:mm')
        if current_time in self.alarm_times:
            save_file=text2voice("闹钟时间已到")
            play(save_file)
            print('Hello')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AlarmClock()
    clock.show()
    sys.exit(app.exec_())