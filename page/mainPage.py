#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/6 10:59
# @File     : mainPage.py
# @Project  : XR_face_Tools
"""
import tkinter as tk
from tkinter import ttk


class MyWin:
    def __init__(self, face_detect_photo, face_detect_camera, face_detect_batch, face_search_photo, face_search_camera,
                 face_search_batch, face_live_photo, face_live_camera, face_live_batch, face_track_photo,
                 face_track_camera, face_track_batch, page="default_page"):
        page_dic = {
            "default_page": self.default_page,
            "face_search": self.face_search_1,
            "live_detect": self.live_detect,
            "face_track": self.face_track,
        }
        self.face_detect_photo = face_detect_photo
        self.face_detect_camera = face_detect_camera
        self.face_detect_batch = face_detect_batch
        self.face_search_photo = face_search_photo
        self.face_search_camera = face_search_camera
        self.face_search_batch = face_search_batch
        self.face_live_photo = face_live_photo
        self.face_live_camera = face_live_camera
        self.face_live_batch = face_live_batch
        self.face_track_photo = face_track_photo
        self.face_track_camera = face_track_camera
        self.face_track_batch = face_track_batch

        self.name = "XR-人脸识别工具箱"
        self.win = tk.Tk()
        self.win.title("XR-人脸识别工具箱")
        self.setup_ui()
        page_dic[page]()
        self.win.mainloop()

    def auto_center(self, height, width):
        '''
        窗口自动居中
        :param height: 长
        :param width: 宽
        :return:
        '''
        cur_height = height
        cur_width = width
        # scn_width, scn_height = self.win.maxsize()
        scn_width, scn_height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        tmp_cnf = '%dx%d+%d+%d' % (cur_height, cur_width, (scn_width - cur_height) / 2, (scn_height - cur_width) / 2)
        self.win.geometry(tmp_cnf)
        # 页面大小不可调整
        self.win.resizable(width=False, height=False)

    def setup_ui(self):
        # 设置屏幕居中显示
        self.auto_center(720, 420)
        # 添加菜单按钮组件
        self.detect_btn = tk.Button(self.win, text="人脸检测", bd=0, command=self.default_page, font=('微软雅黑', 10))
        self.recogn_btn = tk.Button(self.win, text="人脸识别", bd=0, command=self.face_search_1, font=('微软雅黑', 10))
        self.live_detect_btn = tk.Button(self.win, text="活体检测", bd=0, command=self.live_detect, font=('微软雅黑', 10))
        self.track_btn = tk.Button(self.win, text="人脸跟踪", bd=0, command=self.face_track, font=('微软雅黑', 10))
        self.author_but = tk.Button(self.win, text="By:  chuanwen.peng", bd=0, font=('微软雅黑', 10, "bold"),
                                    foreground="Blue")
        self.detect_btn.place(x=0, y=-2)
        self.recogn_btn.place(x=60, y=-2)
        self.live_detect_btn.place(x=120, y=-2)
        self.track_btn.place(x=180, y=-2)
        self.author_but.place(x=880, y=-2)

    def default_page(self):
        self.setup_ui()
        self.detect_btn["background"] = "#03a9f4"
        self.detect_btn["foreground"] = "#FFFFFF"
        face_detect = self.FaceDetect(self.win, self.face_detect_photo, self.face_detect_camera, self.face_detect_batch)
        face_detect.show()

    def face_search_1(self):
        self.setup_ui()
        self.recogn_btn["background"] = "#03a9f4"
        self.recogn_btn["foreground"] = "#FFFFFF"
        face_search = self.FaceSearch(self.win, self.face_search_photo, self.face_search_camera, self.face_search_batch)
        face_search.show()

    def live_detect(self):
        self.setup_ui()
        self.live_detect_btn["background"] = "#03a9f4"
        self.live_detect_btn["foreground"] = "#FFFFFF"
        live_detect = self.LiveDetect(self.win, self.face_live_photo, self.face_live_camera, self.face_live_batch)
        live_detect.show()

    def face_track(self):
        self.setup_ui()
        self.track_btn["background"] = "#03a9f4"
        self.track_btn["foreground"] = "#FFFFFF"
        face_track = self.FaceTrack(self.win, self.face_track_photo, self.face_track_camera, self.face_track_batch)
        face_track.show()

    def run(self):
        self.win.mainloop()

    class FaceSearch:
        def __init__(self, master, face_search_photo, face_search_camera, face_search_batch):
            self.face_search_photo = face_search_photo
            self.face_search_camera = face_search_camera
            self.face_search_batch = face_search_batch

            self.name = "人脸识别页面"
            self.master = master
            self.face_detect = tk.Frame(self.master, bg="#B0E0E6", height="400", width="720")
            self.setup_ui()

        def setup_ui(self):
            tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=80, y=40)
            self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
            self.combox_list["values"] = ("星纪", "旷世")
            self.combox_list.current(1)
            self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
            self.combox_list.place(x=380, y=40)

            tk.Button(self.face_detect, text="批量识别", background="green", width=80, height=6,
                      command=self.go_face_search_batch).place(x=80, y=80)
            tk.Button(self.face_detect, text="照片识别", background="green", width=30, height=6,
                      command=self.go_face_search_photo).place(x=80, y=210)
            tk.Button(self.face_detect, text="摄像头识别", background="green", width=30, height=6,
                      command=self.go_face_search_camera).place(x=430, y=210)
            tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                     height=2).place(
                x=140,
                y=360)

        def go_face_search_photo(self):
            self.face_search_photo()

        def go_face_search_camera(self):
            self.face_search_camera()

        def go_face_search_batch(self):
            self.face_search_batch()

        def alg_select(self, a):
            print(self.combox_list.get())

        def show(self):
            self.face_detect.place(x=0, y=25)

    class LiveDetect:
        def __init__(self, master, face_live_photo, face_live_camera, face_live_batch):
            self.face_live_photo = face_live_photo
            self.face_live_camera = face_live_camera
            self.face_live_batch = face_live_batch

            self.name = "活体检测页面"
            self.master = master
            self.face_detect = tk.Frame(self.master, bg="#B0E0E6", height="400", width="720")
            self.setup_ui()

        def setup_ui(self):
            tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=80, y=40)
            self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
            self.combox_list["values"] = ("星纪", "旷世")
            self.combox_list.current(1)
            self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
            self.combox_list.place(x=380, y=40)

            tk.Button(self.face_detect, text="批量检测", background="green", width=80, height=6,
                      command=self.go_face_live_batch).place(x=80, y=80)
            tk.Button(self.face_detect, text="照片检测", background="green", width=30, height=6,
                      command=self.go_face_live_photo).place(x=80, y=210)
            tk.Button(self.face_detect, text="摄像头检测", background="green", width=30, height=6,
                      command=self.go_face_live_camera).place(x=430, y=210)
            tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                     height=2).place(
                x=140,
                y=360)

        def go_face_live_photo(self):
            self.face_live_photo()

        def go_face_live_camera(self):
            self.face_live_camera()

        def go_face_live_batch(self):
            self.face_live_batch()

        def alg_select(self, a):
            print(self.combox_list.get())

        def show(self):
            self.face_detect.place(x=0, y=25)

    class FaceTrack:
        def __init__(self, master, face_track_photo, face_track_camera, face_track_batch):
            self.face_track_photo = face_track_photo
            self.face_track_camera = face_track_camera
            self.face_track_batch = face_track_batch

            self.name = "人脸跟踪页面"
            self.master = master
            self.face_detect = tk.Frame(self.master, bg="#B0E0E6", height="400", width="720")
            self.setup_ui()

        def setup_ui(self):
            tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=80, y=40)
            self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
            self.combox_list["values"] = ("星纪", "旷世")
            self.combox_list.current(1)
            self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
            self.combox_list.place(x=380, y=40)

            tk.Button(self.face_detect, text="批量检测", background="green", width=80, height=6,
                      command=self.go_face_track_batch).place(x=80, y=80)
            tk.Button(self.face_detect, text="照片检测", background="green", width=30, height=6,
                      command=self.go_face_track_photo).place(x=80, y=210)
            tk.Button(self.face_detect, text="摄像头检测", background="green", width=30, height=6,
                      command=self.go_face_track_camera).place(x=430, y=210)
            tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                     height=2).place(
                x=140,
                y=360)

        def go_face_track_photo(self):
            self.face_track_photo()

        def go_face_track_camera(self):
            self.face_track_camera()

        def go_face_track_batch(self):
            self.face_track_batch()

        def alg_select(self, a):
            print(self.combox_list.get())

        def show(self):
            self.face_detect.place(x=0, y=25)

    class FaceDetect:
        def __init__(self, master, face_detect_photo, face_detect_camera, face_detect_batch):
            self.face_detect_photo = face_detect_photo
            self.face_detect_camera = face_detect_camera
            self.face_detect_batch = face_detect_batch

            self.name = "人脸检测页面"
            self.master = master
            self.face_detect = tk.Frame(self.master, bg="#B0E0E6", height="400", width="720")
            self.setup_ui()

        def setup_ui(self):
            tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=80, y=40)
            self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
            self.combox_list["values"] = ("星纪", "旷世")
            self.combox_list.current(1)
            self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
            self.combox_list.place(x=380, y=40)

            tk.Button(self.face_detect, text="批量检测", background="green", width=80, height=6,
                      command=self.go_face_detect_batch).place(x=80, y=80)
            tk.Button(self.face_detect, text="照片检测", background="green", width=30, height=6,
                      command=self.go_face_detect_photo).place(x=80, y=210)
            tk.Button(self.face_detect, text="摄像头检测", background="green", width=30, height=6,
                      command=self.go_face_detect_camera).place(x=430, y=210)
            tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                     height=2).place(
                x=140, y=360)

        def go_face_detect_photo(self):
            self.face_detect_photo()

        def go_face_detect_camera(self):
            self.face_detect_camera()

        def go_face_detect_batch(self):
            self.face_detect_batch()

        def alg_select(self, a):
            print(self.combox_list.get())

        def show(self):
            self.face_detect.place(x=0, y=25)


if __name__ == '__main__':
    win = MyWin()
    win.run()
