import pyautogui as pt
from time import sleep

while True:
    posXY = pt.position()                        # This will tell us the position of our mouse pointer
    print(posXY, pt.pixel(posXY[0], posXY[1]))   # pt.pixel will give the color of the pixel at the given x and y coordinates.
    sleep(1)

    if posXY[0] == 0:
        break
