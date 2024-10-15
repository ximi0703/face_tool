#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/6 10:56
# @File     : FaceSearchPage.py
# @Project  : XR_face_Tools
"""
import ctypes
import os
import re
import shutil
import threading
import time
import tkinter
import tkinter as tk
from tkinter import ttk, filedialog, dialog
from tkinter.filedialog import askopenfilename, askdirectory

import cv2
import numpy as np
import xlwt as xlwt
from PIL import Image, ImageTk
import uiautomator2 as u2
from flow.InterfaceClass import KShiFace, XJSDFace

PAGE = "face_search"
count_register, count_search = 0, 0


def init_camera_devices(ip='10.100.100.181'):
    try:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../src/xgimiCameraDLL.dll")
        dll = ctypes.CDLL(path)
        dll.getCameraList.restype = ctypes.c_char_p
        cameraString = dll.getCameraList()
        cameraString = cameraString.decode()
        cameras_list = cameraString.strip().split(";")
        cameras_list = [i for i in cameras_list if i]
    except Exception as ex:
        print("get_camera_fail,{}".format(ex))
        cameras_list = []
    cameras_list1 = cameras_list.copy()
    [cameras_list.remove(i) for i in cameras_list1 if "DroidCam" in i]
    cameras_list.append(get_cam_url(ip))
    return cameras_list


def get_cam_url(ip, port=4747, res='480p'):
    res_dict = {
        '240p': '320x240',
        '480p': '640x480',
        '720p': '1280x720',
        '1080p': '1920x1080',
    }
    url = f'http://{ip}:{port}/mjpegfeed?{res_dict[res]}'
    return url


def thread_it(func, *args):
    # 创建线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.setDaemon(True)
    # 启动线程
    t.start()


def get_face_search(face_set, file_name, choose_alg):
    alg_dic = {
        "星纪": XJSDFace,
        "旷世": KShiFace
    }
    ks_face = alg_dic[choose_alg]()
    ret = ks_face.search_face(face_set, file_name)
    return ret


def get_face_set(face_set, choose_alg):
    alg_dic = {
        "星纪": XJSDFace,
        "旷世": KShiFace
    }
    ks_face = alg_dic[choose_alg]()
    ret = ks_face.add_face_set(face_set)
    return ret


def get_face_add(face_set, face_tokens, choose_alg):
    alg_dic = {
        "星纪": XJSDFace,
        "旷世": KShiFace
    }
    ks_face = alg_dic[choose_alg]()
    ret = ks_face.add_face(face_set, face_tokens)
    if choose_alg == "星纪":
        if ret["msg"] == 'success':
            return True
        else:
            return False
    else:
        if ret["faceset_token"]:
            return True
        else:
            return False


def get_face_detect(file_name, choose_alg):
    alg_dic = {
        "星纪": XJSDFace,
        "旷世": KShiFace
    }
    ks_face = alg_dic[choose_alg]()
    ret = ks_face.detect_face(file_name=file_name)
    if choose_alg == "星纪":
        return ret['data']["faceToken"]
    else:
        return ret['faces'][0]["face_token"]


class FaceSearchPagePhoto:
    def __init__(self, home_page):
        self.face_set = ''

        self.name = "XR-人脸识别-照片识别"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_search = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_search, text="选择需要测试的算法： ").place(x=60, y=40)
        self.combox_list = ttk.Combobox(self.face_search, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.alg = "旷世"
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=40)

        self.image_label = tk.Label(self.face_search, text="图片结果输出")
        self.image_label.place(x=20, y=80, height=160, width=320)

        scrollbar_v = tkinter.Scrollbar(self.face_search)
        scrollbar_v.place(x=673, y=81, height=172)

        self.text_label = tk.Text(self.face_search, width=43, height=13)
        self.text_label.place(x=370, y=80)
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        self.file_path = ""

        tk.Button(self.face_search, text="选取图片", background="green", width=20, height=3,
                  command=lambda: thread_it(self.choose_pic())).place(x=430, y=280)
        tk.Button(self.face_search, text="开始识别", background="green", width=20, height=3,
                  command=lambda: thread_it(self.search_face())).place(x=120, y=280)
        tk.Label(self.face_search, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_search, text="返回主页", background="green", width=20, height=2,
                  command=lambda: home_page(PAGE)).place(
            x=460, y=360)

        self.face_search.place(x=0, y=0)
        self.win.mainloop()

    def search_face(self):
        if not self.file_path:
            tkinter.messagebox.showinfo('错误', '请先选择人脸照片！')
        if self.alg == "星纪":
            # TODO 传入face_set_id
            self.face_set = "77"
            boxes_all = get_face_search(self.face_set, self.file_path, self.alg)
            text = '''
"confidence": %s,
"face_token": %s"
''' % (boxes_all[0], boxes_all[1])

            self.text_label.delete(1.0, tkinter.END)
            # text = "星纪算法，暂不支持绘制人脸框"
            self.text_label.insert(tkinter.END, text)
        else:
            # TODO 传入face_set_token
            self.face_set = "93b24dc01a96970cae8d696da8b70aeb"
            boxes_all = get_face_search(self.face_set, self.file_path, self.alg)
            print(boxes_all)

            self.text_label.delete(1.0, tkinter.END)

            text = '''
"confidence": %s,
"face_token": %s"
''' % (boxes_all[0], boxes_all[1])

            self.text_label.insert(tkinter.END, text)

            os.remove(self.file_path)

    def choose_pic(self):
        self.file_path = askopenfilename()
        image = Image.open(self.file_path)
        # 重设尺寸
        image = image.resize((320, 160), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(image=image)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def alg_select(self, a):
        print(self.combox_list.get())

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


class FaceSearchPageCamera:
    def __init__(self, home_page):
        self.home_page = home_page
        self.capturing = True
        self.face_set = ''

        self.frame = 0

        self.name = "XR-人脸识别-摄像头识别"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_search = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_search, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_search, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.combox_list.current(1)
        self.alg = "旷世"
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Label(self.face_search, text="摄像头列表： ").place(x=60, y=45)
        self.combox_list_camera = ttk.Combobox(self.face_search, textvariable=tk.StringVar(), width=35)

        self.camera_list = init_camera_devices()
        self.combox_list_camera["values"] = self.camera_list
        self.combox_list_camera.current(0)
        self.camera = self.camera_list[0]
        self.combox_list_camera.bind("<<ComboboxSelected>>", self.camera_select)
        self.combox_list_camera.place(x=380, y=45)

        self.camera_label = tk.Label(self.face_search, text="摄像头实时画面")
        self.camera_label.place(x=60, y=80, height=200, width=290)

        self.image_label = tk.Label(self.face_search, text="图片结果输出")
        self.image_label.place(x=420, y=80, height=130, width=220)

        scrollbar_v = tkinter.Scrollbar(self.face_search)
        scrollbar_v.place(x=665, y=220, height=122)

        self.text_label = tk.Text(self.face_search, width=43, height=9)
        self.text_label.place(x=360, y=220)
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        self.start_button = tk.Button(self.face_search, text="开始检测", width=10, height=3,
                                      command=lambda: thread_it(self.search_camera_detect()))
        self.start_button.place(x=120, y=290)

        self.open_camera = tk.Button(self.face_search, text="打开摄像头", width=10, height=3,
                                     command=lambda: thread_it(self.search_camera_open()))
        self.open_camera.place(x=240, y=290)
        tk.Label(self.face_search, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_search, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.go_home_page(PAGE)).place(
            x=460, y=360)

        try:
            self.driver = u2.connect()
        except Exception as e:
            print(e)
            tkinter.messagebox.showinfo('错误', '请先连接设备获取摄像头列表！')
            self.home_page(PAGE)
        self.face_search.place(x=0, y=0)
        self.win.mainloop()

    def search_camera_detect(self):
        try:
            if isinstance(self.frame, int):
                tkinter.messagebox.showinfo('错误', '请先选择摄像头并打开！')
        except Exception as e:
            print(e)
        # TODO 读取某一帧
        if not os.path.exists("./temp_img"):
            os.mkdir("./temp_img")
        file_name = os.path.join("./temp_img", str(time.time_ns()) + ".png")
        cv2.imwrite(file_name, self.frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        if self.alg == "星纪":
            # TODO 传入face_set_id
            self.face_set = "77"
            boxes_all = get_face_search(self.face_set, file_name, self.alg)
            text = '''
"confidence": %s,
"face_token": %s"
''' % (boxes_all[0], boxes_all[1])

            self.text_label.delete(1.0, tkinter.END)
            # text = "星纪算法，暂不支持绘制人脸框"
            self.text_label.insert(tkinter.END, text)

            image = Image.open(file_name)
            image = image.resize((220, 130), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
        else:
            # TODO 传入face_set_token
            self.face_set = "93b24dc01a96970cae8d696da8b70aeb"
            boxes_all = get_face_search(self.face_set, self.file_path, self.alg)
            print(boxes_all)

            self.text_label.delete(1.0, tkinter.END)

            text = '''
"confidence": %s,
"face_token": %s"
''' % (boxes_all[0], boxes_all[1])

            self.text_label.insert(tkinter.END, text)

            image = Image.open(file_name)
            image = image.resize((220, 130), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            os.remove(file_name)

    def search_camera_open(self):
        print(self.camera, self.alg)
        camera_index = self.camera_list.index(self.camera)
        if "http://" in self.camera:
            self.driver.app_start("com.dev47apps.droidcamx", wait=True)
            self.cap = cv2.VideoCapture(self.camera)
            # print(cap)
            # self.driver.press("home")
        else:
            self.cap = cv2.VideoCapture(camera_index)
        if self.cap.isOpened():
            print('HIKVISION')
        else:
            self.cap = cv2.VideoCapture(self.camera)
            print('DaHua')
        self.open_camera['state'] = tk.DISABLED
        while self.capturing:
            ref, self.frame = self.cap.read()
            # print(self.frame)
            self.search_get_camera_img()

    def go_home_page(self, page):
        try:
            self.capturing = False
            self.cap.release()
            self.driver.app_stop("com.dev47apps.droidcamx")
        except Exception as e:
            print(e)
        self.home_page(page=page)

    def search_get_camera_img(self):
        cv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        pil_image = Image.fromarray(cv_image)
        pil_image = pil_image.resize((290, 200), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(image=pil_image)

        self.camera_label.config(image=img_tk)
        self.camera_label.image = img_tk

        self.face_search.update()
        self.face_search.after(1)

    def camera_select(self, a):
        self.camera = self.combox_list_camera.get()
        print(self.combox_list_camera.get())

    def alg_select(self, a):
        print(self.combox_list.get())

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


class FaceSearchPageBatch:
    def __init__(self, home_page):
        self.home_page = home_page
        self.face_set = ''

        self.name = "XR-人脸识别-批量识别"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_search = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_search, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_search, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.alg = "旷世"
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Button(self.face_search, text="选择数据集及标注文件", background="green", width=20, height=2,
                  command=lambda: thread_it(self.search_select_path())).place(x=280, y=45)
        self.img_path = tk.StringVar()
        self.img_path.set(os.path.abspath("data"))
        self.data_img = os.path.abspath("data")
        self.file_img = tk.Entry(self.face_search, textvariable=self.img_path, width=30)  # 初始化
        self.file_img.place(x=60, y=65)

        tk.Label(self.face_search, text="人脸数据集:").place(x=440, y=63)
        self.face_set_var = tk.StringVar()
        self.face_set_var.set('test')
        ttk.Entry(self.face_search, textvariable=self.face_set_var, width=8).place(x=515, y=63)

        tk.Button(self.face_search, text="注册", background="green", width=8, height=2,
                  command=lambda: thread_it(self.register_face_set())).place(
            x=580, y=45)

        tk.Label(self.face_search, text="PG注册集:").place(x=60, y=120)
        self.pg_register_count = tk.StringVar()
        self.pg_register_count.set('10')
        ttk.Entry(self.face_search, textvariable=self.pg_register_count, width=5).place(x=130, y=120)

        tk.Label(self.face_search, text="PG识别集:").place(x=220, y=120)
        self.pg_search_count = tk.StringVar()
        self.pg_search_count.set('10')
        ttk.Entry(self.face_search, textvariable=self.pg_search_count, width=5).place(x=290, y=120)

        tk.Label(self.face_search, text="PN注册集:").place(x=380, y=120)
        self.pn_register_count = tk.StringVar()
        self.pn_register_count.set('10')
        ttk.Entry(self.face_search, textvariable=self.pn_register_count, width=5).place(x=450, y=120)

        tk.Label(self.face_search, text="PN识别集:").place(x=540, y=120)
        self.pn_search_count = tk.StringVar()
        self.pn_search_count.set('10')
        ttk.Entry(self.face_search, textvariable=self.pn_search_count, width=5).place(x=610, y=120)

        scrollbar_v = tkinter.Scrollbar(self.face_search)
        scrollbar_v.place(x=673, y=150, height=147)

        self.text_label = tk.Text(self.face_search, width=87, height=11)
        self.text_label.place(x=60, y=150)
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        self.start_button = tk.Button(self.face_search, text="开始识别", width=20, height=3,
                                      command=lambda: thread_it(self.search_face_start()))
        self.start_button.place(x=120, y=310)
        tk.Button(self.face_search, text="保存数据", background="green", width=20, height=3,
                  command=lambda: thread_it(self.search_save_file())).place(x=450, y=310)
        tk.Label(self.face_search, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_search, text="返回主页", background="green", width=20, height=1,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=380)

        self.face_search.place(x=0, y=0)
        self.win.mainloop()

    def register_face_set(self):
        self.face_set = get_face_set(self.face_set_var.get(), self.alg)
        self.console_log_search("注册人脸库完成！人脸库： %s" % self.face_set)
        print(self.face_set)

    def get_file_txt(self, pg_register_img, pn_register_img, pg_search_img, pn_search_img):
        if os.path.exists(self.mark_txt):
            os.remove(self.mark_txt)
        pg_register_img.extend(pn_register_img)
        all_img_li = []
        zero_li = [i for i in range(len(pn_search_img))]
        pg_register_img.extend(zero_li)

        pn_index = int(self.pg_register_count.get()) + int(self.pn_register_count.get())
        for index, reg in enumerate(pg_register_img):
            line = ["0", "0", "0"]
            if isinstance(reg, str) and re.findall(r".*\\(.*?).jpg", reg, re.S):
                if re.findall(r".*\\(.*?).jpg", reg, re.S)[0].count('0') > 1:
                    line[0] = reg
                    line[1] = "0"
                    line[2] = "0"
                else:
                    # PG
                    line[0] = reg
                    line[1] = pg_search_img[index]
                    line[2] = "1"
            else:
                line[0] = "0"
                # print(index - pn_index, pn_search_img[index - pn_index])
                line[1] = pn_search_img[index - pn_index]
                line[2] = "0"
            all_img_li.append(line)

        with open(self.mark_txt, 'a', encoding="utf-8") as f:
            for line in all_img_li:
                f.writelines("\t\t".join(line))
                f.writelines('\n')

    def register_face(self):
        global count_register
        with open(self.mark_txt, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            # 注册集
            register_li = [i.split()[0] for i in lines if i.split()[0] != '0']
        face_li = []

        # try:
        #     face_name = []
        #     face_token = get_face_detect(register_li[count_register], self.alg)
        #     time.sleep(1)
        #     face_set = int(self.face_set) if self.alg == "星纪" else self.face_set
        #     ret = get_face_add(face_set, face_token, self.alg)
        #     time.sleep(1)
        #     number = count_register + 1
        #     if ret:
        #         # TODO 标注人脸姓名和token
        #         face_name.append(register_li[count_register])
        #         face_name.append(face_token)
        #         face_li.append(face_name)
        #         with open(self.token_file, 'a', encoding="utf-8") as f:
        #             f.writelines("\t\t".join(face_name))
        #             f.writelines('\n')
        #         self.console_log_search("注册人脸成功, 当前：%s个, 当前人脸：%s" % (number, register_li[count_register]))
        #     else:
        #         number -= 1
        #         self.console_log_search(register_li[count_register])
        # except Exception as e:
        #     print(e)
        #
        # count_register += 1
        # rep = self.face_search.after(10, self.register_face)
        # if count_register >= len(register_li):
        #     self.face_search.after_cancel(rep)
        #     count_register = 0
        for regi in register_li:
            try:
                face_name = []
                count_register += 1
                face_token = get_face_detect(regi, self.alg)
                time.sleep(1)
                ret = get_face_add(self.face_set, face_token, self.alg)
                time.sleep(1)
                if ret:
                    # TODO 标注人脸姓名和token
                    face_name.append(regi)
                    face_name.append(face_token)
                    face_li.append(face_name)
                    with open(self.token_file, 'a', encoding="utf-8") as f:
                        f.writelines("\t\t".join(face_name))
                        f.writelines('\n')
                    self.console_log_search("注册人脸成功, 当前：%s个, 当前人脸：%s" % (count_register, regi))
            except Exception as e:
                print(e)
                count_register -= 1

    def search(self):
        global count_search
        search_pg_li = []
        search_pn_li = []
        all_data = []
        with open(self.mark_txt, 'r', encoding="gbk") as f:
            lines = f.readlines()
            for line in lines:
                if line.split()[-1] == '1':
                    search_pg_li.append(line.split()[1])
                elif line.split()[0] == '0':
                    search_pn_li.append(line.split()[1])
                all_data.append(line.split())
        token_dic = {}
        with open(self.token_file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                token_dic[line.split()[1]] = line.split()[0]
        all_face_pg = []

        for pg in search_pg_li:
            try:
                pg_li = []
                pg_li.append(pg)
                face_token = get_face_detect(pg, self.alg)
                if face_token:
                    result, token = get_face_search(self.face_set, pg, self.alg)
                    token_file = token_dic[token]
                    ret = 1 if [i for i in all_data if pg in i and token_file in i] else 0
                    pg_li.append(token_dic[token])
                    pg_li.append(token)
                    pg_li.append(result)
                    pg_li.append(ret)
                else:
                    result, ret, token = "null", "null", "null"
                    pg_li.append("null")
                    pg_li.append(token)
                    pg_li.append(result)
                    pg_li.append(0)
                self.console_log_search("当前识别人脸照片：%s， 返回人脸照片：%s" % (pg, pg_li[1]))
                all_face_pg.append(pg_li)
            except Exception as e:
                print(e)
        all_face_pn = []
        for pn in search_pn_li:
            try:
                pn_li = []
                pn_li.append(pn)
                face_token = get_face_detect(pn, self.alg)
                if face_token:
                    result, token = get_face_search(self.face_set, pn, self.alg)
                    token_file = token_dic[token]
                    ret = 1 if [i for i in all_data if pn in i and token_file in i] else 0
                    pn_li.append(token_dic[token])
                    pn_li.append(token)
                    pn_li.append(result)
                    pn_li.append(ret)
                else:
                    result, ret, token = "null", "null", "null"
                    pn_li.append("null")
                    pn_li.append(token)
                    pn_li.append(result)
                    pn_li.append(0)
                self.console_log_search("当前识别人脸照片：%s， 返回人脸照片：%s" % (pn, pn_li[1]))
                all_face_pn.append(pn_li)
            except Exception as e:
                print(e)
        self.start_button['state'] = tk.NORMAL
        return all_face_pg, all_face_pn

    def write_to_excel(self, pg, pn, file_name):
        wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet1 = wb.add_sheet('pg', cell_overwrite_ok=True)
        sheet2 = wb.add_sheet('pn', cell_overwrite_ok=True)
        # 表头
        for col, i in enumerate(["PG识别集", "Gallery_Return", "token", "相似度", "result"]):
            sheet1.write(0, col, i)
        for col, i in enumerate(["PN识别集", "Gallery_Return", "token", "相似度", "result"]):
            sheet2.write(0, col, i)

        for row in range(len(pg)):
            for col in range(len(pg[row])):
                sheet1.write(row + 1, col, pg[row][col])
        for row in range(len(pn)):
            for col in range(len(pn[row])):
                sheet2.write(row + 1, col, pn[row][col])
        width_list = [40, 40, 20]
        for width in range(len(width_list)):
            sheet1.col(width).width = 256 * width_list[width]
            sheet2.col(width).width = 256 * width_list[width]
        wb.save(file_name)

    def search_face_start(self):
        self.start_button['state'] = tk.DISABLED
        try:
            pg_base_path = os.path.join(self.data_img, "Images")
            data_files = os.listdir(pg_base_path)
            base_data = [os.path.join(pg_base_path, i, "frontal") for i in data_files]
            base_data_pg = [i for i in base_data if len(os.listdir(i)) >= 2]

            self.console_log_search("pg数据集总长度为： %s" % len(base_data_pg))
            # 去除少于两张照片的人
            base_data_files = base_data_pg[:int(self.pg_register_count.get())]
            pg_register_img = [os.path.join(i, os.listdir(i)[0]) for i in base_data_files]

            pn_base_path = os.path.join(self.data_img, "img_align_celeba")
            pn_base = [os.path.join(pn_base_path, i) for i in os.listdir(pn_base_path)]
            pn_register_img = pn_base[:int(self.pn_register_count.get())]

            self.console_log_search("pn数据集总长度为： %s" % len(pn_base))

            base_data_pn = base_data_pg[int(self.pg_register_count.get()):int(self.pg_search_count.get()) + int(
                self.pg_register_count.get())]
            pg_search_img = [os.path.join(i, os.listdir(i)[1]) for i in base_data_pg]
            pn_search_img = [os.path.join(pn_base_path, i) for i in os.listdir(pn_base_path)][
                            int(self.pn_register_count.get()):int(self.pn_search_count.get()) + int(
                                self.pn_register_count.get())]
            if int(self.pn_search_count.get()) + int(self.pn_register_count.get()) >= len(pn_base) or int(
                    self.pg_search_count.get()) + int(self.pg_register_count.get()) >= len(base_data_pg):
                tkinter.messagebox.showinfo('错误', '选择的数据集大于数据集总数量！')
                self.start_button['state'] = tk.NORMAL
        except Exception as e:
            print(e)

        self.mark_txt = "tokens.txt"
        if not os.path.exists(self.mark_txt):
            # 拿去注册并且生成注册文件
            self.get_file_txt(pg_register_img, pn_register_img, pg_search_img, pn_search_img)

        # TODO 批量注册
        self.token_file = "register_tokens%s.txt" % self.alg
        # if os.path.exists(self.token_file):
        #     os.remove(self.token_file)
        self.register_face()

        self.console_log_search("开始识别人脸")
        all_face_pg, all_face_pn = self.search()
        print(all_face_pn, all_face_pg)

        self.write_to_excel(all_face_pg, all_face_pn, "report\\result_%s.xlsx" % self.alg)
        self.console_log_search("写入文件成功！文件： %s" % 'report\\result_%s.xlsx' % self.alg)

    def console_log_search(self, string):
        if self.text_label.get("1.0", tk.END) == '数据结果输出\n':
            self.text_label.delete(1.0, tkinter.END)
            self.text_label.insert("1.0", "\r" + string)

        else:
            self.text_label.insert(tk.END, "\r" + string)
        self.text_label.insert(tk.END, "\n")
        self.text_label.focus_force()
        self.text_label.see(tk.END)
        self.text_label.update()

        if not os.path.exists("./report"):
            os.mkdir("./report")
        with open("./report/log.log", 'a+', encoding='utf-8') as f:
            f.writelines(string)
            f.writelines("\n")

    def search_save_file(self):
        path = "."
        if not os.path.exists(path):
            os.mkdir(path)
        file_path = filedialog.asksaveasfilename(title=u'保存文件',
                                                 initialdir=r'./report',
                                                 initialfile='log.txt',
                                                 filetypes=[('TXT', '*.txt'), ('All files', '*')])
        if file_path is not None and file_path != '':
            shutil.move("./report/log.log", file_path)
            dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
                                 'strings': ('OK', 'Cancle')})

    def search_select_path(self):
        path_ = askdirectory()
        if path_ == "":
            self.img_path.get()
        else:
            path_ = path_.replace("/", "\\")
            self.img_path.set(path_)
        self.data_img = path_

    def go_home_page(self, page):
        self.home_page(page=page)

    def alg_select(self, a):
        print(self.combox_list.get())

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
