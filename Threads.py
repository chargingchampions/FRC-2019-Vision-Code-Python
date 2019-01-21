# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 19:12:38 2019

@author: Albert Lin
"""

"""
the thread that captures images from the camera
get the most recent one with read()
"""

import cv2
from threading import Thread



class CameraThread(Thread):
    sourceID = 1
    exposure_ID = 15
    #brightness_ID = 10 #unsure if ID is right, and change in brightness not needed anyways
    #brightness = -100
    exposure = -10000
    frame = None
    
    cap = cv2.VideoCapture(sourceID)
    cap.set(exposure_ID, exposure)
        
    def run(self):
        while self.cap.isOpened():
            self.cap.grab()
        print('camera is closed')
        
    def read(self):
        if self.cap.isOpened():
            have_frame, self.frame = self.cap.read()
            return have_frame, self.frame
        return False, self.frame
