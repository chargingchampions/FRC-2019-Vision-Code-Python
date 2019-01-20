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
from networktables import NetworkTables
from grip import GripRetroreflectivePipeline

exposure_ID = 15
brightness_ID = 10
brightness = 0
exposure = -10000

def extra_processing(pipeline):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []

    print(pipeline.filter_contours_output.__len__())
    for contour in pipeline.filter_contours_output:
        #returns a Box2D structure which contains following detals
        #( top-left corner(x,y), (width, height), angle of rotation )
        point, dimensions, angle = cv2.minAreaRect(contour)
        x, y = point
        w, h = dimensions
        print(angle)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)

    # Publish to the '/vision/red_areas' network table
    #table = NetworkTables.getTable('/vision/red_areas')
    #table.putNumberArray('x', center_x_positions)
    #table.putNumberArray('y', center_y_positions)
    #table.putNumberArray('width', widths)
    #table.putNumberArray('height', heights)


def main():
    print('Initializing NetworkTables')
    #NetworkTables.setClientMode()
    #NetworkTables.setIPAddress('localhost')
    NetworkTables.initialize()

    print('Creating video capture')
    cap = cv2.VideoCapture(1)
    cap.set(brightness_ID, brightness)
    cap.set(exposure_ID, exposure)

    print('Creating pipeline')
    pipeline = GripRetroreflectivePipeline()

    print('Running pipeline')
    while cap.isOpened():
        have_frame, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        cv2.waitKey(25)
        
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)

    print('Capture closed')


if __name__ == '__main__':
    main()