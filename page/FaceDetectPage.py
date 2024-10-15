#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/6 10:56
# @File     : FaceDetectPage.py
# @Project  : XR_face_Tools
"""
import ctypes
import os
import shutil
import threading
import time
import tkinter
import tkinter as tk
from tkinter import ttk, RIGHT, BOTTOM, HORIZONTAL, Y, X, NONE, filedialog, dialog
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror

import uiautomator2 as u2
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
from flow.InterfaceClass import KShiFace, XJSDFace

PAGE = "default_page"
count = 0


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


def get_face_detect(file_name, choose_alg):
    alg_dic = {
        "星纪": XJSDFace,
        "旷世": KShiFace
    }
    ks_face = alg_dic[choose_alg]()
    ret = ks_face.detect_face(file_name=file_name)
    # return list(ret["faces"][0]["face_rectangle"].values())
    return ret


class FaceDetectPagePhoto:
    def __init__(self, home_page):
        self.home_page = home_page

        self.name = "XR-人脸检测-照片检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=40)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.alg = "旷世"
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=40)

        self.image_label = tk.Label(self.face_detect, text="图片结果输出")
        self.image_label.place(x=20, y=80, height=160, width=320)

        scrollbar_v = tkinter.Scrollbar(self.face_detect)
        scrollbar_v.place(x=673, y=81, height=172)

        self.text_label = tk.Text(self.face_detect, width=43, height=13)
        self.text_label.place(x=370, y=80)
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        self.file_path = ""

        tk.Button(self.face_detect, text="选取图片", background="green", width=20, height=3,
                  command=lambda: thread_it(self.choose_pic())).place(x=430, y=280)
        tk.Button(self.face_detect, text="开始检测", background="green", width=20, height=3,
                  command=lambda: thread_it(self.draw_face())).place(x=120, y=280)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=360)

        self.face_detect.place(x=0, y=0)
        self.win.mainloop()

    def draw_face(self):
        if not self.file_path:
            tkinter.messagebox.showinfo('错误', '请先选择人脸照片！')
        if self.alg == "星纪":
            boxes_all = get_face_detect(self.file_path, self.alg)
            # print(boxes_all)
            text = '''
星纪算法， 暂不支持输出人脸框！！！
'code': %s,
'data': 
'faceToken': %s',
'msg': %s'
        ''' % (boxes_all["code"], boxes_all["data"]["faceToken"], boxes_all["msg"])

            self.text_label.delete(1.0, tkinter.END)
            # text = "星纪算法，暂不支持绘制人脸框"
            self.text_label.insert(tkinter.END, text)
        else:
            boxes_all = get_face_detect(self.file_path, self.alg)
            print(boxes_all)
            boxes_img = list(boxes_all["faces"][0]["face_rectangle"].values())
            img = cv2.imdecode(np.fromfile(self.file_path, dtype=np.uint8), -1)
            if boxes_img is not None:
                # 画人脸框
                cv2.rectangle(img, (boxes_img[1], boxes_img[0]),
                              (boxes_img[2] + boxes_img[1], boxes_img[0] + boxes_img[3]), (220, 20, 60), 2)
            cv2.waitKey(0)
            self.file_path = self.file_path.replace(self.file_path.split('.')[0], self.file_path.split('.')[0] + "_t")
            print(self.file_path)
            cv2.imwrite(self.file_path, img)

            image = Image.open(self.file_path)
            image = image.resize((320, 160), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            self.text_label.delete(1.0, tkinter.END)

            text = '''
"time_used": %s,
"faces": 
"face_token": "%s",
"face_rectangle":
    "top": %s,
    "left": %s,
    "width": %s,
    "height": %s
"face_num": %s
''' % (boxes_all["time_used"], boxes_all["faces"][0]["face_token"],
       boxes_all["faces"][0]["face_rectangle"]["top"],
       boxes_all["faces"][0]["face_rectangle"]["left"], boxes_all["faces"][0]["face_rectangle"]["width"],
       boxes_all["faces"][0]["face_rectangle"]["height"], boxes_all["face_num"])

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
        self.alg = self.combox_list.get()
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


class FaceDetectPageCamera:
    def __init__(self, home_page):
        self.home_page = home_page
        self.capturing = True

        self.frame = 0

        self.name = "XR-人脸检测-摄像头检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")

        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.combox_list.current(1)
        self.alg = "旷世"
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Label(self.face_detect, text="摄像头列表： ").place(x=60, y=45)
        self.combox_list_camera = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)

        self.camera_list = init_camera_devices()
        self.combox_list_camera["values"] = self.camera_list
        self.combox_list_camera.current(0)
        self.camera = self.camera_list[0]
        self.combox_list_camera.bind("<<ComboboxSelected>>", self.camera_select)
        self.combox_list_camera.place(x=380, y=45)

        self.camera_label = tk.Label(self.face_detect, text="摄像头实时画面")
        self.camera_label.place(x=60, y=80, height=200, width=290)

        self.image_label = tk.Label(self.face_detect, text="图片结果输出")
        self.image_label.place(x=420, y=80, height=130, width=220)

        scrollbar_v = tkinter.Scrollbar(self.face_detect)
        scrollbar_v.place(x=665, y=220, height=122)

        self.text_label = tk.Text(self.face_detect, width=43, height=9)
        self.text_label.place(x=360, y=220)
        # self.display_text.set("数据结果输出")
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        # tk.Button(self.face_detect, text="数据结果输出", background="#545454", width=30, height=7).place(x=420, y=220)
        self.start_button = tk.Button(self.face_detect, text="开始检测", width=10, height=3,
                                      command=lambda: thread_it(self.camera_detect()))
        self.start_button.place(x=120, y=290)

        self.open_camera = tk.Button(self.face_detect, text="打开摄像头", width=10, height=3,
                                     command=lambda: thread_it(self.camera_open()))
        self.open_camera.place(x=240, y=290)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.go_home_page(PAGE)).place(
            x=460, y=360)

        try:
            self.driver = u2.connect()
        except Exception as e:
            print(e)
            tkinter.messagebox.showinfo('错误', '请先连接设备获取摄像头列表！')
            self.home_page(PAGE)
        self.face_detect.place(x=0, y=0)
        self.win.mainloop()

    def go_home_page(self, page):
        try:
            self.capturing = False
            self.cap.release()
            self.driver.app_stop("com.dev47apps.droidcamx")
        except Exception as e:
            print(e)
        self.home_page(page=page)

    def alg_select(self, a):
        self.alg = self.combox_list.get()
        print(self.combox_list.get())

    def camera_detect(self):
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
            boxes_all = get_face_detect(file_name, self.alg)
            # print(boxes_all)
            text = '''
星纪算法， 暂不支持输出人脸框！！！
'code': %s,
'data': 
'faceToken': %s',
'msg': %s'
        ''' % (boxes_all["code"], boxes_all["data"]["faceToken"], boxes_all["msg"])

            image = Image.open(file_name)
            image = image.resize((220, 130), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            self.text_label.delete(1.0, tkinter.END)
            # text = "星纪算法，暂不支持绘制人脸框"
            self.text_label.insert(tkinter.END, text)
        else:
            boxes_all = get_face_detect(file_name, self.alg)
            print(boxes_all)
            boxes_img = list(boxes_all["faces"][0]["face_rectangle"].values())
            img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
            if boxes_img is not None:
                # 画人脸框
                cv2.rectangle(img, (boxes_img[1], boxes_img[0]),
                              (boxes_img[2] + boxes_img[1], boxes_img[0] + boxes_img[3]), (220, 20, 60), 2)
            cv2.waitKey(0)
            # image_path = file_name.replace(file_name.split('.')[0], file_name.split('.')[0] + "_t")
            # print(image_path)
            cv2.imwrite(file_name, img)

            image = Image.open(file_name)
            image = image.resize((220, 130), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(image=image)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            self.text_label.delete(1.0, tkinter.END)

            text = '''
"time_used": %s,
"faces": 
"face_token": "%s",
"face_rectangle":
    "top": %s,
    "left": %s,
    "width": %s,
    "height": %s
"face_num": %s
''' % (boxes_all["time_used"], boxes_all["faces"][0]["face_token"],
       boxes_all["faces"][0]["face_rectangle"]["top"],
       boxes_all["faces"][0]["face_rectangle"]["left"], boxes_all["faces"][0]["face_rectangle"]["width"],
       boxes_all["faces"][0]["face_rectangle"]["height"], boxes_all["face_num"])

            self.text_label.insert(tkinter.END, text)

            os.remove(file_name)

    def camera_open(self):
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
            self.get_camera_img()

            # frame = cv2.flip(frame, 1)  # 摄像头翻转
            # cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # pil_image = Image.fromarray(cv_image)
            # # pil_image = pil_image.resize((3200, 1600), Image.ANTIALIAS)
            # img_tk = ImageTk.PhotoImage(image=pil_image)
            #
            # self.camera_label.config(image=img_tk)
            # self.camera_label.image = img_tk
            #
            # self.face_detect.update()
            # self.face_detect.after(1)

    def get_camera_img(self):
        # frame = cv2.flip(self.frame, 1)  # 摄像头翻转
        cv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        pil_image = Image.fromarray(cv_image)
        pil_image = pil_image.resize((290, 200), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(image=pil_image)

        self.camera_label.config(image=img_tk)
        self.camera_label.image = img_tk

        self.face_detect.update()
        self.face_detect.after(1)

    def camera_select(self, a):
        self.camera = self.combox_list_camera.get()
        print(self.combox_list_camera.get())

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


class FaceDetectPageBatch:
    def __init__(self, home_page):
        self.home_page = home_page

        self.name = "XR-人脸检测-批量检测"
        self.win = tk.Tk()
        self.win.title(self.name)
        self.auto_center(720, 420)
        self.face_detect = tk.Frame(self.win, bg="#B0E0E6", height="420", width="720")
        tk.Label(self.face_detect, text="选择需要测试的算法： ").place(x=60, y=15)
        self.combox_list = ttk.Combobox(self.face_detect, textvariable=tk.StringVar(), width=35)  # 初始化
        self.combox_list["values"] = ("星纪", "旷世")
        self.alg = "旷世"
        self.combox_list.current(1)
        self.combox_list.bind("<<ComboboxSelected>>", self.alg_select)
        self.combox_list.place(x=380, y=15)

        tk.Button(self.face_detect, text="选择数据集及标注文件", background="green", width=20, height=3,
                  command=lambda: thread_it(self.select_path())).place(x=450, y=45)
        self.img_path = tk.StringVar()
        self.img_path.set(os.path.abspath("data"))
        self.data_img = os.path.abspath("data")
        self.file_img = tk.Entry(self.face_detect, textvariable=self.img_path, width=35)  # 初始化
        self.file_img.place(x=60, y=65)

        scrollbar_v = tkinter.Scrollbar(self.face_detect)
        scrollbar_v.place(x=673, y=120, height=147)

        self.text_label = tk.Text(self.face_detect, width=87, height=11)
        self.text_label.place(x=60, y=120)
        self.text_label.insert(1.0, "数据结果输出")

        self.text_label.config(yscrollcommand=scrollbar_v.set)

        self.start_button = tk.Button(self.face_detect, text="开始检测", state=tk.NORMAL, width=20,
                                      height=3, command=lambda: thread_it(self.detect_face()))
        self.start_button.place(x=120, y=280)
        tk.Button(self.face_detect, text="保存数据", background="green", width=20, height=3,
                  command=lambda: thread_it(self.save_file())).place(x=450, y=280)
        tk.Label(self.face_detect, text="%s" % self.name, bg="#B0E0E6", font=('华文琥珀', 12), width=50,
                 height=2).place(
            x=140, y=380)

        tk.Button(self.face_detect, text="返回主页", background="green", width=20, height=2,
                  command=lambda: self.home_page(PAGE)).place(
            x=460, y=360)

        self.face_detect.place(x=0, y=0)
        self.win.mainloop()

    def detect_face(self):
        global count
        if self.alg == "星纪":
            # 遍历文件夹，做图片识别
            self.start_button['state'] = tk.DISABLED
            data_files = os.listdir(self.data_img)
            data_files = [i for i in data_files if i.endswith("jpg") or i.endswith("png")]
            # TODO 不用for循环
            # global count
            data_img = os.path.join(self.data_img, data_files[count])
            img_ret = get_face_detect(data_img, self.alg)
            text = '''第%s次人脸检测，当前图片地址: %s, 检测状态: %s''' % (count + 1, data_img, img_ret["msg"])
            self.console_log(text)

            count += 1
            rep = self.face_detect.after(500, self.detect_face)
            if count >= len(data_files):
                self.face_detect.after_cancel(rep)
                self.start_button['state'] = tk.NORMAL
                count = 0
        else:
            # 遍历文件夹，做图片识别
            self.start_button['state'] = tk.DISABLED
            data_files = os.listdir(self.data_img)
            data_files = [i for i in data_files if i.endswith("jpg") or i.endswith("png")]
            # TODO 不用for循环
            # global count
            data_img = os.path.join(self.data_img, data_files[count])
            img_ret = get_face_detect(data_img, self.alg)
            msg = "success" if img_ret["faces"] else "failed"
            text = '''第%s次人脸检测，当前图片地址: %s, 检测状态: %s''' % (count + 1, data_img, msg)
            self.console_log(text)

            count += 1
            rep = self.face_detect.after(500, self.detect_face)
            if count >= len(data_files):
                self.face_detect.after_cancel(rep)
                self.start_button['state'] = tk.NORMAL
                count = 0

    def save_file(self):
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

    def console_log(self, string):
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



    def select_path(self):
        path_ = askdirectory()
        if path_ == "":
            self.img_path.get()
        else:
            path_ = path_.replace("/", "\\")
            self.img_path.set(path_)
        self.data_img = path_

    def alg_select(self, a):
        self.alg = self.combox_list.get()
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
