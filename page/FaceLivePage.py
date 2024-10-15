#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/8 11:25
# @File     : FaceLivePage.py
# @Project  : XR_face_Tools
"""
import tkinter as tk
from tkinter import ttk

PAGE = "live_detect"


class FaceLivePagePhoto:
    def __init__(self, home_page):
        self.home_page = home_page

        self.name = "XR-活体检测-照片检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=40)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=40)

        tk.Button(self.face_detect, text="图片结果输出", background="#545454", width=40, height=10).place(x=60, y=80)
        tk.Button(self.face_detect, text="数据结果输出", background="#545454", width=40, height=10).place(x=360, y=80)
        tk.Button(self.face_detect, text="选取图片", background="green", width=20, height=3).place(x=430, y=280)
        tk.Button(self.face_detect, text="开始检测", background="green", width=20, height=3).place(x=120, y=280)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=360)

        self.show()
        self.win.mainloop()

    def go_home_page(self, page):
        self.home_page(page=page)

    def alg_select(self, a):
        print(self.combox_list.get())

    def show(self):
        self.face_detect.place(x=0, y=0)

    def auto_center(self, height, width):
        '''
        窗口自动居中
        :param height: 长
        :param width: 宽
        :return:
        '''
        cur_height = height
        cur_width = width
        scn_width, scn_height = self.win.maxsize()
        tmp_cnf = '%dx%d+%d+%d' % (cur_height, cur_width, (scn_width - cur_height) / 2, (scn_height - cur_width) / 2)
        self.win.geometry(tmp_cnf)
        # 页面大小不可调整
        self.win.resizable(width=False, height=False)


class FaceLivePageCamera:
    def __init__(self, home_page):
        self.home_page = home_page

        self.name = "XR-活体检测-摄像头检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Label(self.face_detect, text="摄像头列表： ").place(x=60, y=45)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("摄像头1", "摄像头2")
        self.combox_list.current(0)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=45)

        tk.Button(self.face_detect, text="摄像头实时画面", background="#545454", width=40, height=10).place(x=60, y=80)
        tk.Button(self.face_detect, text="图片结果输出", background="#545454", width=30, height=7).place(x=420, y=80)
        tk.Button(self.face_detect, text="数据结果输出", background="#545454", width=30, height=7).place(x=420, y=220)
        tk.Button(self.face_detect, text="开始检测", background="green", width=20, height=3).place(x=120, y=280)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=360)

        self.show()
        self.win.mainloop()

    def go_home_page(self, page):
        self.home_page(page=page)

    def alg_select(self, a):
        print(self.combox_list.get())

    def show(self):
        self.face_detect.place(x=0, y=0)

    def auto_center(self, height, width):
        '''
        窗口自动居中
        :param height: 长
        :param width: 宽
        :return:
        '''
        cur_height = height
        cur_width = width
        scn_width, scn_height = self.win.maxsize()
        tmp_cnf = '%dx%d+%d+%d' % (cur_height, cur_width, (scn_width - cur_height) / 2, (scn_height - cur_width) / 2)
        self.win.geometry(tmp_cnf)
        # 页面大小不可调整
        self.win.resizable(width=False, height=False)


class FaceLivePageBatch:
    def __init__(self, home_page):
        self.home_page = home_page

        self.name = "XR-活体检测-批量检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Button(self.face_detect, text="选择数据集及标注文件", background="green", width=20, height=3).place(x=450, y=45)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("文件地址1", "文件地址2")
        self.combox_list.current(0)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=60, y=65)

        tk.Button(self.face_detect, text="数据结果输出", background="#545454", width=82, height=8).place(x=60, y=120)

        tk.Button(self.face_detect, text="开始检测", background="green", width=20, height=3).place(x=120, y=280)
        tk.Button(self.face_detect, text="保存数据", background="green", width=20, height=3).place(x=450, y=280)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=360)

        self.show()
        self.win.mainloop()

    def go_home_page(self, page):
        self.home_page(page=page)

    def alg_select(self, a):
        print(self.combox_list.get())

    def show(self):
        self.face_detect.place(x=0, y=0)

    def auto_center(self, height, width):
        '''
        窗口自动居中
        :param height: 长
        :param width: 宽
        :return:
        '''
        cur_height = height
        cur_width = width
        scn_width, scn_height = self.win.maxsize()
        tmp_cnf = '%dx%d+%d+%d' % (cur_height, cur_width, (scn_width - cur_height) / 2, (scn_height - cur_width) / 2)
        self.win.geometry(tmp_cnf)
        # 页面大小不可调整
        self.win.resizable(width=False, height=False)


if __name__ == '__main__':
    pass
