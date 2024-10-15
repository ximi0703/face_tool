#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Author   : chuanwen.peng
# @Time     : 2022/9/6 10:55
# @File     : Application.py
# @Project  : XR_face_Tools
"""
from page.FaceDetectPage import FaceDetectPagePhoto, FaceDetectPageCamera, FaceDetectPageBatch
from page.FaceSearchPage import FaceSearchPagePhoto, FaceSearchPageCamera, FaceSearchPageBatch
from page.FaceLivePage import FaceLivePagePhoto, FaceLivePageCamera, FaceLivePageBatch
from page.FaceTrackPage import FaceTrackPagePhoto, FaceTrackPageCamera, FaceTrackPageBatch
from page.mainPage import MyWin


class Application(MyWin, FaceDetectPagePhoto, FaceDetectPageCamera, FaceDetectPageBatch, FaceSearchPagePhoto,
                  FaceSearchPageCamera, FaceSearchPageBatch, FaceLivePagePhoto, FaceLivePageCamera, FaceLivePageBatch,
                  FaceTrackPagePhoto, FaceTrackPageCamera, FaceTrackPageBatch):
    def __init__(self):
        self.home_page()

    def home_page(self, page="default_page"):
        try:
            self.win.destroy()
        except Exception as e:
            print(e)
        MyWin.__init__(self,
                       face_detect_photo=self.face_detect_photo,
                       face_detect_camera=self.face_detect_camera,
                       face_detect_batch=self.face_detect_batch,
                       face_search_photo=self.face_search_photo,
                       face_search_camera=self.face_search_camera,
                       face_search_batch=self.face_search_batch,
                       face_live_photo=self.face_live_photo,
                       face_live_camera=self.face_live_camera,
                       face_live_batch=self.face_live_batch,
                       face_track_photo=self.face_track_photo,
                       face_track_camera=self.face_track_camera,
                       face_track_batch=self.face_track_batch,
                       page=page
                       )

    def face_detect_photo(self):
        self.win.destroy()
        FaceDetectPagePhoto.__init__(self, home_page=self.home_page)

    def face_detect_camera(self):
        self.win.destroy()
        FaceDetectPageCamera.__init__(self, home_page=self.home_page)

    def face_detect_batch(self):
        self.win.destroy()
        FaceDetectPageBatch.__init__(self, home_page=self.home_page)

    def face_search_photo(self):
        self.win.destroy()
        FaceSearchPagePhoto.__init__(self, home_page=self.home_page)

    def face_search_camera(self):
        self.win.destroy()
        FaceSearchPageCamera.__init__(self, home_page=self.home_page)

    def face_search_batch(self):
        self.win.destroy()
        FaceSearchPageBatch.__init__(self, home_page=self.home_page)
        # self.root = FaceSearchPageBatch.__init__(self, home_page=self.home_page).win

    def face_live_photo(self):
        self.win.destroy()
        FaceLivePagePhoto.__init__(self, home_page=self.home_page)

    def face_live_camera(self):
        self.win.destroy()
        FaceLivePageCamera.__init__(self, home_page=self.home_page)

    def face_live_batch(self):
        self.win.destroy()
        FaceLivePageBatch.__init__(self, home_page=self.home_page)

    def face_track_photo(self):
        self.win.destroy()
        FaceTrackPagePhoto.__init__(self, home_page=self.home_page)

    def face_track_camera(self):
        self.win.destroy()
        FaceTrackPageCamera.__init__(self, home_page=self.home_page)

    def face_track_batch(self):
        self.win.destroy()
        FaceTrackPageBatch.__init__(self, home_page=self.home_page)


if __name__ == '__main__':
    Application()
