# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 13:10:58 2019

@author: Albert Lin
"""

#!/usr/bin/python3

"""
taken from GRIP repository
Sample program that uses a generated GRIP pipeline to detect lines in an image and publish important features to NetworkTables.
"""

import cv2
import numpy as np
from networktables import NetworkTables
from grip import GripRetroreflectivePipeline

exposure_ID = 15
#brightness_ID = 10
#brightness = 0
exposure = -10000
H_FOV = 53
V_FOV = 43.3964

def extra_processing(pipeline, frame, width, height):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    x_angle_table = []
    distance_table = []

    print(pipeline.filter_contours_output.__len__())
    for contour in pipeline.filter_contours_output:
        #returns a Box2D structure which contains following detals
        #( top-left corner(x,y), (width, height), angle of rotation )
        rect = cv2.minAreaRect(contour)
        point, dimensions, angle = rect
        boxPoints = cv2.boxPoints(rect)
        
        #print('boxPoints = ', boxPoints)
        #print('point, dimensions = ', point, dimensions)
        #print('angle: ', angle)
        #keeping only the right-slanted lines
        if (angle > -85 and angle < -65):
            boxPoints = np.int0(boxPoints)
            x, y = np.sum(boxPoints, axis = 0)/4
            #now, x and y are the coordinates of the center pixel of the target
            x_angle = (width/2-x)/width*H_FOV
            print(x_angle)
            x_angle_table.append(x_angle)
            distance_table.append(y)
            cv2.drawContours(frame,[boxPoints],0,(0,0,255),2)
            cv2.circle(frame, (int(x), int(y)), 4, (0, 0, 255))

    # Publish to the '/vision/lines' network table
    #table = NetworkTables.getTable('/vision/lines')
    #table.putNumberArray('x', center_x_positions)
    #table.putNumberArray('y', center_y_positions)
    #table.putNumberArray('width', widths)
    #table.putNumberArray('height', heights)
    return frame


def main():
    print('Initializing NetworkTables')
    #NetworkTables.setClientMode()
    #NetworkTables.setIPAddress('localhost')
    NetworkTables.initialize()

    print('Creating video capture')
    cap = cv2.VideoCapture(1)
    #cap.set(brightness_ID, brightness)
    cap.set(exposure_ID, exposure)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print('Creating pipeline')
    pipeline = GripRetroreflectivePipeline()

    print('Running pipeline')
    while cap.isOpened():
        have_frame, frame = cap.read()
        
        if have_frame:
            pipeline.process(frame)
            processed_frame = extra_processing(pipeline, frame, width, height)
            # Display the resulting frame
            cv2.imshow('Frame', processed_frame)
            cv2.waitKey(25)

    print('Capture closed')


if __name__ == '__main__':
    main()