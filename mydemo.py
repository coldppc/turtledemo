#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *
import random
import math

PLANE_SPEED = 4
BLT_SPEED = 16
MSLE_SPEED = 8
MSLE_TURN = 3 # missile turn degree

def reg_shape_plane(color, shape_name):
    s = Shape("compound")
    poly1 = ((0, -4), (20, -10), (0, 20), (-20, -10))
    s.addcomponent(poly1, color, color)
    poly2 = ((0, -4), (10, -16), (-10, -16))
    s.addcomponent(poly2, color, color)
    register_shape(shape_name, s)

def reg_shape_missle():
    s = Shape("compound")
    poly = ((-5, 0), (0, 15), (5, 0))
    s.addcomponent(poly, "red")
    register_shape("missle", s)

def new_bullet(blt_list, plane):
    #tracer(2)
    if len(blt_list) < 2:
        b = Turtle(visible=False)
        b.up()
        b.shapesize(0.5, 0.5)
    else:
        # re-use bullet 0
        b = blt_list.pop(0)
        b.hideturtle()
    b.setpos(plane.xcor(), plane.ycor())
    b.setheading(plane.heading())
    b.showturtle()
    blt_list.append(b)
    #tracer(1)

def new_missle(misl_list, plane):
    #tracer(2)
    if len(misl_list) < 2:
        m = Turtle(visible=False)
        m.shape("missle")
        m.up()
    else:
        found = False
        for m in misl_list:
            if not m.isvisible():
                found = True
                break
        if found:
            misl_list.remove(m)
        else:
            #tracer(1)
            return
        #   m = misl_list.pop(0)
        m.hideturtle()

    m.setpos(plane.xcor(), plane.ycor())
    m.setheading(plane.heading())
    m.showturtle()
    misl_list.append(m)
    #tracer(1)


def p1_shoot():
    new_bullet(blt_list1, p1)

def p2_shoot():
    new_bullet(blt_list2, p2)

def p1_fire():
    new_missle(misl_list1, p1)

def p2_fire():
    new_missle(misl_list2, p2)

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

def check_life( b, plane, life_list):
    if in_range(b.xcor(), plane.xcor(), 20) and \
            in_range(b.ycor(), plane.ycor(), 20):
        for x in range(6):
            plane.showturtle()
            plane.right(60)
            plane.hideturtle()
        if len(life_list) == 0:
            print("Game Over !")
            return False
        id = life_list.pop(0)
        plane.clearstamp(id)
        plane.setx(random.uniform(-window_width() / 2, window_width() / 2))
        plane.sety(random.uniform(-window_height() / 2, window_height() / 2))
        plane.showturtle()
    return True

"""Return True if should turn left"""
def left_or_right(m, p, log=False):
    beta = math.atan2(p.ycor() - m.ycor(), p.xcor() - m.xcor())
    beta = math.degrees(beta)
    turn_left_angle = 360 - m.heading() + beta
    if turn_left_angle > 360:
        turn_left_angle -= 360
    if turn_left_angle < 0:
        turn_left_angle += 360
    if log:
        print ("m(%d, %d) p(%d, %d) beta:%d mheading:%d TL_angle:%d" %
           (m.xcor(), m.ycor(), p.xcor(), p.ycor(), beta, m.heading(), turn_left_angle))
    if turn_left_angle < 180:
        return True
    else:
        return False

def objects_move():
    if not in_range(p1.xcor(), 0, window_width() / 2):
        #tracer(2)
        p1.setx(-p1.xcor())
        #tracer(1)
        #update()
    if not in_range(p1.ycor(), 0, window_height() / 2):
        #tracer(2)
        p1.sety(-p1.ycor())
        #tracer(1)
        #update()
    p1.fd(PLANE_SPEED)

    if p2.xcor() >= window_width() / 2 or p2.xcor() <= -window_width() / 2:
        #tracer(2, 100)
        p2.setx(-p2.xcor())
        #tracer(1, 10)
        #update()
    if p2.ycor() >= window_height() / 2 or p2.ycor() <= -window_height() / 2:
        #tracer(2, 100)
        p2.sety(-p2.ycor())
        #tracer(1, 10)
        #update()

    p2.fd(PLANE_SPEED)

    for wpn in blt_list1 + misl_list1:
        if check_life(wpn, p2, life_list2) == False:
            return
        if not in_range(wpn.xcor(), 0, window_width() / 2) or \
                not in_range(wpn.ycor(), 0, window_height() / 2):
            wpn.hideturtle()
        elif wpn in blt_list1:
            wpn.fd(BLT_SPEED)
        else: # wpn is missile
            if left_or_right(wpn, p2):
                wpn.left(MSLE_TURN)
            else:
                wpn.right(MSLE_TURN)
            wpn.fd(MSLE_SPEED)
    for wpn in blt_list2 + misl_list2:
        if check_life(wpn, p1, life_list1) == False:
            return
        if not in_range(wpn.xcor(), 0, window_width() / 2) or \
                not in_range(wpn.ycor(), 0, window_height() / 2):
            wpn.hideturtle()
        elif wpn in blt_list2:
            wpn.fd(BLT_SPEED)
        else: # wpn is missile
            if left_or_right(wpn, p1):
                wpn.left(MSLE_TURN)
            else:
                wpn.right(MSLE_TURN)
            wpn.fd(MSLE_SPEED)

    # repeat moving
    update()
    ontimer(objects_move, 30) # 33.3 frame per second

def main():
    reg_shape_plane("blue", "b_plane_shape")
    reg_shape_plane("green", "g_plane_shape")
    reg_shape_missle()
    global p1, p2
    global blt_list1, blt_list2, misl_list1, misl_list2
    global life_list1, life_list2
    blt_list1 = []
    blt_list2 = []
    misl_list1 = []
    misl_list2 = []
    life_list1 = []
    life_list2 = []

    tracer(False)

    p1 = Turtle(visible=False)
    p1.shape("b_plane_shape")
    p1.up()
    p1.goto(-window_width() / 2 + 30, window_height() / 2 - 30)
    for i in range(3):
        s_id = p1.stamp()
        life_list1.append(s_id)
        p1.fd(40)
    p1.setheading(270)
    p1.showturtle()

    p2 = Turtle(visible=False)
    p2.shape("g_plane_shape")
    p2.up()
    p2.goto(window_width() / 2 - 150, window_height() / 2 - 30)
    for i in range(3):
        id = p2.stamp()
        life_list2.append(id)
        p2.fd(40)
    p2.setheading(270)
    p2.showturtle()

    onkeyrelease(p1_turn_left, "a")
    onkeyrelease(p1_turn_right, "d")
    onkeyrelease(p1_shoot, "space")
    onkeyrelease(p1_fire, "s")
    onkeyrelease(p2_turn_left, "Left")
    onkeyrelease(p2_turn_right, "Right")
    onkeyrelease(p2_shoot, "Return")
    onkeyrelease(p2_fire, "Down")
    listen()

    objects_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
