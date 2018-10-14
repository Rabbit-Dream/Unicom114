#-*- coding: utf-8 -*-

'''
Date: 2018/10/01
Brief: 通过麦克风录音生成wav,调用科大讯飞API生成文本
@auth: 潘壮壮
'''

import wave
# 导入多线程包
import threading
# 导入语音处理包
from pyaudio import PyAudio,paInt16
# 导入键盘监视包
from pynput import keyboard
# 导入KdxfAPI实现语音转文本
from voice_txt import KdxfAPI

# 相当于定义静态变量
class Foo(object):
    Key = False

framerate=16000     #采样频率
NUM_SAMPLES=2000    #一次性录音采样字节大小
channels=1          #声道
sampwidth=2         #采样字节

#################录音并写入文件#################
def save_wave_file(filename,data):

    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():

    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    print("录音开始！！！")
    while Foo.Key == False:#控制录音结束
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        print('.')
    print("录音结束！！！按 esc 退出")
    save_wave_file('01.wav',my_buf)
    stream.close()

##################键盘监视#####################

def on_press(key):
    if key == keyboard.Key.right:
        # 如果按键盘右键，Foo.Key将会被赋值为 True（此处的Foo.Key相当于静态变量）
        Foo.Key = True
def on_release(key):
    if key == keyboard.Key.esc:
        # 按esc键结束监视 
        return False
# 键盘监视
def JianShi():
    with keyboard.Listener(on_press = on_press,on_release=on_release) as listener:
        listener.join()

##################主函数开启多线程##############

def main():
    #多线程为了实现键盘监视来结束录音
    t1 = threading.Thread(target=JianShi)
    t1.start()

    t2 = threading.Thread(target=my_record)
    t2.start()

    t1.join()
    t2.join()

if __name__ == '__main__':
    main()
    print(Foo.Key)
    xf = KdxfAPI("01.wav")
    xf.fun()



