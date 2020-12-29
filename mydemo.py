#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *
import os

PLANE_SPEED = 5
BLT_SPEED = 30

def reg_shape_plane(color, shape_name):
    s = Shape("compound")
    poly1 = ((0, -2), (10, -5), (0, 10), (-10, -5))
    s.addcomponent(poly1, color, color)
    poly2 = ((0, -2), (5, -8), (-5, -8))
    s.addcomponent(poly2, color, color)
    register_shape(shape_name, s)

def new_bullet(blt_list, plane):
    tracer(2)
    if len(blt_list) < 2:
        b = Turtle(visible=False)
        b.up()
        b.shapesize(0.2, 0.2)
    else:
        # re-use bullet 0
        b = blt_list.pop(0)
        b.hideturtle()
    b.setpos(plane.xcor(), plane.ycor())
    b.setheading(plane.heading())
    b.showturtle()
    blt_list.append(b)
    tracer(1)

def p1_fire():
    new_bullet(blt_list1, p1)

def p2_fire():
    new_bullet(blt_list2, p2)

def p1_turn_left():
    p1.left(10)

def p1_turn_right():
    p1.right(10)

def p2_turn_left():
    p2.left(10)

def p2_turn_right():
    p2.right(10)

"""
my pos (x, y), center (cx,cy), delta x and delta y (dx,dy)
"""
def in_range(x, cx, dx):
    if (x <= cx - dx) or (x >= cx + dx):
        return False
    else:
        return True

def check_life(b, plane, life_list):
    if in_range(b.xcor(), plane.xcor(), 15) and \
        in_range(b.ycor(), plane.ycor(), 15):
        for x in range(6):
            plane.showturtle()
            plane.right(60)
            plane.hideturtle()
        if len(life_list) == 0:
            print("Game Over !")
            return False
        id = life_list.pop(0)
        plane.clearstamp(id)
        plane.home()
        plane.showturtle()
    return True

def objects_move():
    global running
    running = True
    if not running:
        return
    if not in_range(p1.xcor(), 0, window_width()/2):
        tracer(2)
        p1.setx(-p1.xcor())
        tracer(1)
        update()
    if not in_range(p1.ycor(), 0, window_height()/2):
        tracer(2)
        p1.sety(-p1.ycor())
        tracer(1)
        update()
    p1.fd(PLANE_SPEED)
    if p2.xcor() >= window_width()/2 or p2.xcor() <= -window_width()/2:
        tracer(2, 100)
        p2.setx(-p2.xcor())
        tracer(1,10)
        update()
    if p2.ycor() >= window_height()/2 or p2.ycor() <= -window_height()/2:
        tracer(2, 100)
        p2.sety(-p2.ycor())
        tracer(1,10)
        update()
    p2.fd(PLANE_SPEED)
    for b in blt_list1:
        if check_life(b, p2, life_list2) == False:
            return
        if not in_range(b.xcor(), 0, window_width()/2) or \
            not in_range(b.ycor(), 0, window_height()/2):
            b.hideturtle()
        else:
            b.fd(BLT_SPEED)
    for b in blt_list2:
        if check_life(b, p1, life_list1) == False:
            return
        if not in_range(b.xcor(), 0, window_width()/2) or \
            not in_range(b.ycor(), 0, window_height()/2):
            b.hideturtle()
        else:
            b.fd(BLT_SPEED)
    # repeat moving
    ontimer(objects_move, 20)

def main():
    reg_shape_plane("blue", "b_plane_shape")
    reg_shape_plane("green", "g_plane_shape")
    global p1, p2
    global blt_list1, blt_list2
    global life_list1, life_list2
    blt_list1 = []
    blt_list2 = []
    life_list1 = []
    life_list2 = []
    p1 = Turtle(visible=False)
    p1.shape("b_plane_shape")
    p1.up()
    p1.goto(-window_width()/2 + 30, window_height()/2 - 30)
    for i in range(3):
        s_id = p1.stamp()
        life_list1.append(s_id)
        p1.fd(20)
    p1.setheading(270)
    p1.showturtle()

    p2 = Turtle(visible=False)
    p2.shape("g_plane_shape")
    p2.up()
    p2.goto(window_width()/2 - 90, window_height()/2 - 30)
    for i in range(3):
        id = p2.stamp()
        life_list2.append(id)
        p2.fd(20)
    p2.setheading(270)
    p2.showturtle()

    onkeyrelease(p1_fire, "space")
    onkeyrelease(p1_turn_left, "a")
    onkeyrelease(p1_turn_right, "d")

    onkeyrelease(p2_fire, "Return")
    onkeyrelease(p2_turn_left, "Left")
    onkeyrelease(p2_turn_right, "Right")
    listen()
    p1.up()
    p2.up()
    objects_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()