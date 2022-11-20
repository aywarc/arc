from djitellopy import Tello
import cv2
import time
import math
import os


def pic(tello):
    tello.streamoff()
    tello.streamon()
    img = tello.get_frame_read().frame
    return img

def distance(loc):
    return math.sqrt(loc[0]**2 + loc[1]**2)

def popBalloon(l, tello):
    if len(l) <= 0:
        return
    x = l[0][0]
    y = l[0][1]
    if x < 0:
        tello.move_left(x*30) # move to x coordinate
    else:
        tello.move_right(x*30) # move to x coordinate
    if y < 0:
        tello.move_down(x*30) # move to y coordinate
    else:
        tello.move_up(x*30) # move to y coordinate
    tello.move_forward(70)
    tello.move_back(70)
    nl = []
    for i in l[1:]:
        nl.append([i[0]-x,i[1]-y])
    return popBalloon(nl.sort(key=distance))

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
params = cv2.aruco.DetectorParameters_create()
locations = {2: [[1,1],[3,2],[5,3]],
             6: [[5,1],[5,2],[6,3]],
             9: [[2,1],[1,2],[4,3]],
             11: [[6,1],[4,2],[2,3]],
             14: [[3,1],[6,2],[1,3]],
             18: [[4,1],[2,2],[3,3]]
            }
path = os.path.dirname(os.path.realpath(__file__))
with open(path + r'\run1.txt') as run:
    nums = [int(num) for num in run]

def main():
    try:
        tello = Tello()
        tello.connect()
        tello.takeoff()
        time.sleep(1)
        img = pic(tello)
        corners, ids, rejected = cv2.aruco.detectMarkers(img, dictionary, parameters=params)
        positions = []
        for i in ids:
            for j in locations[i[0]]:
                try:
                    positions.append(j)
                except:
                    pass
        positions = [[i[0]-3.5,i[1]] for i in positions]
        positions.sort(key=distance)
        popBalloon(positions, tello)
        tello.land()
    except KeyboardInterrupt:
        tello.land()

main()