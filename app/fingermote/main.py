import numpy as np
import cv2
from random import randint
import math
import sys

__author__ = 'Idan'

fgbg = cv2.createBackgroundSubtractorMOG2()

frame = cv2.imread('G:\\t.jpg')

def main():
    cap = cv2.VideoCapture(0)
    jedi_counter = 0
    lower_range = (240,)*3
    upper_range = (255,)*3
    fingermote_rect = None
    points = None
    frame_missing = 5
    while( cap.isOpened() ) :
        ret, frame = cap.read()
        
        #asa = fgbg.apply(frame)

        #no_back = cv2.bitwise_and(frame, frame, mask=asa)

        me = cv2.inRange(frame, tuple(lower_range), tuple(upper_range))
        me = fgbg.apply(me)

        me = cv2.erode(me, None)
        #me = cv2.dilate(me, None)

        im2, contours, hierarchy = cv2.findContours(me,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours) > 0):
            new_fingermote_rect = cv2.boundingRect(contours[0])
            min_dist = 0
            if fingermote_rect:
                min_dist = dist(new_fingermote_rect[0], new_fingermote_rect[1], fingermote_rect[0], fingermote_rect[1])
                for cnt in contours:
                    rect = cv2.boundingRect(cnt)
                    d = dist(rect[0], rect[1], fingermote_rect[0], fingermote_rect[1])
                    if(d < min_dist and
                            abs(new_fingermote_rect[3] - fingermote_rect[3]) < abs(rect[3] - fingermote_rect[3])):
                        min_dist = d
                        new_fingermote_rect = rect

            if(False):
                frame_missing += 1
            else:
                frame_missing = 0
                if(points is None):
                    points = np.array([[new_fingermote_rect[0], new_fingermote_rect[1]]], dtype='int32')
                else:
                    points = np.concatenate((points, [[new_fingermote_rect[0], new_fingermote_rect[1]]]))
                fingermote_rect = new_fingermote_rect

        else:
            if(frame_missing < 5):
                frame_missing += 1

        if(frame_missing == 5):
            if(not points is None and len(points) > 3):
                if(points[0][0] < points[len(points)-1][0]):
                    print "right"
                    sys.stdout.flush()
                else:
                    print "left"
                    sys.stdout.flush()
                    
            fingermote_rect = None
            points = None

        if(not points is None):
            cv2.polylines(frame, [points], False, (255,255,255))

        #cv2.imshow('input', frame)
        k = cv2.waitKey(1)
        if k == 27:
           break

    cv2.destroyAllWindows()

def dist(x1,x2,y1,y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


if __name__ == '__main__':
    print "Idan is in"
    sys.stdout.flush()
    main()
    print "right"
    #cv2.destroyAllWindows()


