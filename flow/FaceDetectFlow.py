#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/9 13:28
# @File     : FaceDetectFlow.py
# @Project  : XR_face_Tools
"""
# import tkinter
#
# from tkinter import *
#
# from PIL import Image, ImageTk  ###这个是没有想到的模块，也不确定能不能省
#
# from tkinter.filedialog import askopenfilename
#
# import time
#
# import cv2
#
# root = Tk()
#
# root.geometry('500x500')  ##这个小了一点，不知道怎么自适应
#
# root.title('图片处理')
#
#
# def choosepic():
#     path_ = askopenfilename()
#     img = cv2.imread(path_)
#     current_image = Image.fromarray(img)
#     imgtk = ImageTk.PhotoImage(image=current_image)
#     image_label.config(image=imgtk)
#     image_label.image = imgtk  # keep a reference
#
#
# path = StringVar()
#
# Button(root, text='选择图片', command=choosepic).pack()
#
# # file_entry = Entry(root, state='readonly', text=path)
#
# # file_entry.pack()
#
# image_label = Label(root)
#
# image_label.pack()
#
# root.mainloop()

import tkinter as tk


def add_image():
    text.image_create(tk.END, image=img)  # Example 1
    text.window_create(tk.END, window=tk.Label(text, image=img))  # Example 2


root = tk.Tk()

text = tk.Text(root)
text.pack(padx=20, pady=20)
img = tk.PhotoImage(file="../data/000013.jpg")
tk.Button(root, text="Insert", command=add_image).pack()

root.mainloop()
