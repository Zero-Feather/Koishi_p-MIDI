import rtmidi2
import time
from pynput.keyboard import Key, Controller
import json

# 打开 JSON 文件
with open('data.json', 'r') as file:
    data = json.load(file)

# 创建键盘控制器
keyboard = Controller()

def midi_to_keyboard(message):
    """这个函数用于判断按下的midi按键并模拟按下键盘的特定按键"""
    key = list(data[f'{message[1]}'])[0]
    if message[0] == 128:
        keyboard.press(key)
    else:
        keyboard.release(key)

# 定义回调函数来处理 MIDI 消息
def midi_callback(message, timestamp):
    print(f"Received message at time {timestamp}: {message}")
    midi_to_keyboard(message)

# 创建 MidiIn 对象
midi_in = rtmidi2.MidiIn()

# 打开第一个可用的 MIDI 输入端口
midi_in.open_port(0)

# 将回调函数分配给 MidiIn 对象
midi_in.callback = midi_callback

# 开始接收 MIDI 数据
try:
    while True:
        if midi_in.get_message():
            midi_in.callback(midi_in.get_message(), time.time())
        # time.sleep(0.1)  # 短暂暂停以避免过度占用 CPU
except KeyboardInterrupt:
    print("Exiting MIDI input loop.")

# 关闭 MIDI 输入端口
midi_in.close_port()