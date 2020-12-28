#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *

plane_x = 0
def reg_shape_plane(color, shape_name):
    s = Shape("compound")
    poly1 = ((0, -2), (10, -5), (0, 10), (-10, -5))
    s.addcomponent(poly1, color, color)
    poly2 = ((0, -2), (5, -8), (-5, -8))
    s.addcomponent(poly2, color, color)
    register_shape(shape_name, s)

def turn_left():
    left(10)
    #print("Turn Left...")

def turn_right():
    right(10)
    #print("Turn Right...")

def plane_move():
    global running
    global plane_x
    running = True
    if running:
        fd(5)
        plane_x += 5
        if (plane_x >= 8000):
            running = False
            print ("stopped")
        else:
            ontimer(plane_move, 100)

def main():
    reg_shape_plane("blue", "b_plane_shape")
    #a = Turtle()
    shape("b_plane_shape")
    #up()
    onkeypress(turn_left, "Left")
    onkeypress(turn_right, "Right")
    listen()

    plane_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()