import socket
import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror, showwarning

import api
from wordSegment import foolnltkSeg, jiebaSeg


class IflyGui(tk.Tk):

    FONT_LARGE = ('YaHei', 12)
    FONT_MED = ('YaHei', 12)

    MAX_ROW = 10 
    MAX_COLUMN = 10

    ROW_PADDING = 10
    COL_PADDING = 1
    HEIGHT = 8
    BTN_WIDTH = 42
    TEXT_WIDTH = 46

    def __init__(self):
        super(IflyGui, self).__init__()

        self.msg = []

        self.title('114查询')
        self.resizable(width=False, height=False) 

        style = ttk.Style(self)
        style.theme_use('clam')

        for row in range(self.MAX_ROW):
            self.columnconfigure(row, pad=self.ROW_PADDING) 

        for column in range(self.MAX_COLUMN):
            self.rowconfigure(column, pad=self.COL_PADDING)


        self.widget_ = []
        self.frm = []
        
        texts = ['结巴分词结果：', 'fool分词结果：', '结巴关键词：', 'fool关键词：']

        row = 0
        frow = 0

        text = '输入查询内容：'

        self.frm.append(ttk.Frame(self))
        self.frm[-1].grid(row=frow, column=0)
        frow += 1

        self.widget_.append(tk.Label(self.frm[-1], text=text, font=self.FONT_LARGE))
        self.widget_[-1].grid(row=row, column=0, sticky=tk.SW)
        row += 1

        self.widget_.append(tk.Text(self.frm[-1], height=self.HEIGHT, width=self.TEXT_WIDTH * 2, font=self.FONT_MED))
        self.widget_[-1].grid(row=row, column=0)
        row += 1
        
        i = 0
        while i < len(texts):
        # for text in texts:
            self.frm.append(ttk.Frame(self))
            self.frm[-1].grid(row=frow, column=0)
            frow += 1

            self.widget_.append(tk.Label(self.frm[-1], text=texts[i], font=self.FONT_LARGE))
            self.widget_[-1].grid(row=row, column=0, sticky=tk.SW)
            i += 1

            self.widget_.append(tk.Text(self.frm[-1], height=self.HEIGHT, width=self.TEXT_WIDTH, font=self.FONT_MED))
            self.widget_[-1].grid(row=row + 1, column=0)

            self.widget_.append(tk.Label(self.frm[-1], text=texts[i], font=self.FONT_LARGE))
            self.widget_[-1].grid(row=row, column=1, sticky=tk.SW)
            i += 1

            self.widget_.append(tk.Text(self.frm[-1], height=self.HEIGHT, width=self.TEXT_WIDTH, font=self.FONT_MED))
            self.widget_[-1].grid(row=row + 1, column=1)

            row += 2
        

        texts = ['fool', 'jieba']
        i = 0
        row = 0

        self.frm.append(ttk.Frame(self))
        self.frm[-1].grid(row=0, column=2, rowspan=3)


        while i < len(texts):


            result_lable = tk.Label(self.frm[-1], text=texts[i], font=self.FONT_LARGE)
            result_lable.grid(row=row, column=0, sticky='sw')
            i += 1
            row += 1
            self.widget_.append(result_lable)

            result_text = tk.Text(self.frm[-1], height=self.HEIGHT * 3 // 2 + 1, font=self.FONT_MED)
            result_text.grid(row=row, column=0)
            row += 1
            self.widget_.append(result_text)

        self.button_ = [('接收', self.receive),('分词', self._segment), ('查询', self._search), ('清空', self._clear)]
        self.text_command = []
        
        button_frm = ttk.Frame(self, padding=5)
        button_frm.grid(row=6, column=0, columnspan=3, sticky='sw')
        col= 0
        for text, command in self.button_:
            self.text_command.append(tk.Button(button_frm, text=text, command=command, width=self.BTN_WIDTH, font=self.FONT_LARGE))
            self.text_command[-1].grid(row=6, column=col)
            col += 1


    def _search(self):
        line = self.widget_[1].get('1.0', 'end').strip()
        if line == '':
            showerror(message='请输入查询内容！')
            return
        else:
            self._segment()
            self.widget_[11].delete('1.0', 'end')
            self.widget_[13].delete('1.0', 'end')

            fool_result, jieba_result = api.query(line)
            result_list, jieba_list = api.format(fool_result), api.format(jieba_result)

            content = ''.join([
                f'{index}.{phonenum},{all_name}\n' 
                for index, (phonenum, all_name) in enumerate(result_list, 1)
            ])

            jieba_content = ''.join([
                f'{index}.{phonenum},{all_name}\n' 
                for index, (phonenum, all_name) in enumerate(jieba_list, 1)
            ])

            self.widget_[11].insert('insert', content)
            self.widget_[13].insert('insert', jieba_content)

            params = (self.widget_[i].get('1.0', 'end').strip()
                      for i in range(1, len(self.widget_), 2))
            api._save_query(*params)


    def _segment(self):
        query = self.widget_[1].get('1.0', 'end').strip()
        if query == '':
            showerror(message='请输入查询内容！')
            return
        else:
            [self.widget_[i].delete('1.0', 'end') for i in range(3, 10, 2)]

            self.widget_[5].insert(tk.INSERT,
                                   ','.join(foolnltkSeg.get_segmentation(query)))
            self.widget_[9].insert(tk.INSERT,
                                   ','.join(foolnltkSeg.get_keywords(query)))
            self.widget_[3].insert(tk.INSERT,
                                   ','.join(jiebaSeg.get_segmentation(query)))
            self.widget_[7].insert(tk.INSERT,
                                   ','.join(jiebaSeg.get_keywords(query)))
        

    def _clear(self):
        for i in range(1, len(self.widget_), 2):
            self.widget_[i].delete('1.0', 'end')

    def run(self):

        Thread(target=self.listen, args=()).start()
        self.mainloop()

    def receive(self):
        if len(self.msg):
            msg = self.msg.pop(0)
            self.widget_[1].delete('1.0', 'end')
            self.widget_[1].insert(tk.INSERT, msg)
        else:
            showerror(message='当前没有消息待接收！')

        self.text_command[0].configure(text=f'接收（{len(self.msg)}）')

    def listen(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('0.0.0.0', 10005))
        srv.listen(50)

        def retrive(conn, addr):
            while True:
                buff = conn.recv(1024)
                buff = buff.decode()
                if not buff:
                    print('close from:', str(addr))
                    break
                print(buff)
                if self.widget_[1].get('1.0', 'end').strip() == '':
                    self.widget_[1].insert(tk.INSERT, buff)
                else:
                    self.msg.append(buff)
                    self.text_command[0].configure(text=f'接收（{len(self.msg)}）')

        while True:
            conn, addr = srv.accept()
            print('connected from: ', str(addr))
            Thread(target=retrive, args=(conn,addr)).start()


if __name__ == '__main__':
    app = IflyGui()
    app.run()
