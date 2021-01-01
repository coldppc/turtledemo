#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *
import random
import math
import time
from evdev import list_devices, InputDevice, ecodes

PLANE_SPEED = 4
TURBO_SPEED = PLANE_SPEED * 2
BLT_SPEED = PLANE_SPEED * 4
MSLE_SPEED = PLANE_SPEED * 2
MSLE_TURN = 2 # missile turn degree
HIT_RANGE = 15

def reg_shape_plane(color, shape_name):
    s = Shape("compound")
    poly1 = ((0, 20), (-4, -8), (0, -6), (4, -8))
    s.addcomponent(poly1, color, color)
    poly2 = ((0, 16), (-12, -2), (12, -2))
    s.addcomponent(poly2, color, color)
    register_shape(shape_name, s)

def reg_shape_missle(color, shape_name):
    s = Shape("compound")
    poly = ((-1, 0), (0, 12), (1, 0))
    s.addcomponent(poly, color)
    register_shape(shape_name, s)

def new_bullet(blt_list, plane):
    if len(blt_list) < 2:
        b = Turtle(visible=False)
        b.up()
        b.shapesize(0.15)
        b.fillcolor("black")
        b.shape("circle")
    else:
        # re-use bullet 0
        b = blt_list.pop(0)
        b.hideturtle()
    b.setpos(plane.xcor(), plane.ycor())
    b.setheading(plane.heading())
    b.showturtle()
    blt_list.append(b)

def new_missle(misl_list, plane):
    if len(misl_list) < 2:
        m = Turtle(visible=False)
        if plane.shape() == "g_plane_shape":
            m.shape("g_missile")
        else:
            m.shape("b_missile")
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
            return

        m.hideturtle()

    m.setpos(plane.xcor(), plane.ycor())
    m.setheading(plane.heading())
    m.showturtle()
    misl_list.append(m)



def p1_shoot():
    new_bullet(blt_list1, p1)

def p2_shoot():
    new_bullet(blt_list2, p2)

def p1_fire():
    global last_fire_time1
    t = time.time()
    if t - last_fire_time1 > 0.5:
        new_missle(misl_list1, p1)
        last_fire_time1 = t

def p2_fire():
    global last_fire_time2
    t = time.time()
    if t - last_fire_time2 > 0.5:
        new_missle(misl_list2, p2)
        last_fire_time2 = t

def p1_turn_left():
    p1.left(10)

def p1_turn_right():
    p1.right(10)

def p2_turn_left():
    p2.left(10)

def p2_turn_right():
    p2.right(10)

def p1_turbo():
    global p1_state
    if p1_state == 0:
        p1_state = 1
        ontimer(p1_turbo, 1000)
        onkey(None, "w")
    elif p1_state == 1:
        p1_state = 2
        ontimer (p1_turbo, 4000)
    elif p1_state == 2:
        p1_state = 0
        onkey(p1_turbo, "w")

def p2_turbo():
    global p2_state
    if p2_state == 0:
        p2_state = 1
        ontimer(p2_turbo, 1000)
        onkey(None, "Return")
    elif p2_state == 1:
        p2_state = 2
        ontimer (p2_turbo, 4000)
    elif p2_state == 2:
        p2_state = 0
        onkey(p2_turbo, "Return")

"""
my pos (x, y), center (cx,cy), delta x and delta y (dx,dy)
"""
def in_range(x, cx, dx):
    if (x <= cx - dx) or (x >= cx + dx):
        return False
    else:
        return True

def check_life( b, plane, life_list):
    if in_range(b.xcor(), plane.xcor(), HIT_RANGE) and \
        in_range(b.ycor(), plane.ycor(), HIT_RANGE):
        b.hideturtle()
        s = plane.shape()
        tracer(1, 30)
        for x in range(1, 11):
            pic = "pics/expo-%d.gif" % x
            plane.shape(pic)
            update()
        tracer(False)
        plane.shape(s)
        plane.hideturtle()
        if len(life_list) == 0:
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
        p1.setx(-p1.xcor())
    if not in_range(p1.ycor(), 0, window_height() / 2):
        p1.sety(-p1.ycor())
    if p1_state == 1:
       p1.fd(TURBO_SPEED)
    else:
        p1.fd(PLANE_SPEED)

    if p2.xcor() >= window_width() / 2 or p2.xcor() <= -window_width() / 2:
        p2.setx(-p2.xcor())
    if p2.ycor() >= window_height() / 2 or p2.ycor() <= -window_height() / 2:
        p2.sety(-p2.ycor())
    if p2_state == 1:
        p2.fd(TURBO_SPEED)
    else:
        p2.fd(PLANE_SPEED)

    for wpn in blt_list1 + misl_list1:
        if not wpn.isvisible():
            pass
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
        if not wpn.isvisible():
            pass
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

    update()
    ontimer(objects_move, 30) # 33.3 frame per second

def find_gamepad():
    global gamepads
    gamepads = []
    for path in list_devices():
#   for path in ['/dev/input/event7', '/dev/input/event8']:
        dev = InputDevice(path)
        if dev.name == "USB Gamepad ":
            print(dev.path, dev.name, dev.phys)
            gamepads.append(dev)
    return gamepads

def do_gamepad():
    global gamepads
    global p1_state, p2_state # 0:Normal / 1:Turbo / 2:Restore
    for d in gamepads:
        keys = d.active_keys()
	for key in keys:
            if key == ecodes.BTN_THUMB: #"A"
                if d is gamepads[0]: p1_shoot()
                else: p2_shoot()
            elif key == ecodes.BTN_THUMB2: #"B"
		if d is gamepads[0]: p1_fire()
                else: p2_fire()
            elif key == ecodes.BTN_PINKIE: #"R-TRIG"
                if d is gamepads[0]:
                    if p1_state == 0: p1_turbo()
                else:
                    if p2_state == 0: p2_turbo()
        pad = d.absinfo(ecodes.ABS_X)
        if pad.value == 0:
            if d is gamepads[0]: p1_turn_left()
            else: p2_turn_left()
        elif pad.value == 255:
            if d is gamepads[0]: p1_turn_right()
            else: p2_turn_right()
    # schedule for next checking
    ontimer(do_gamepad, 100)

def main():
    reg_shape_plane("blue", "b_plane_shape")
    reg_shape_plane("green", "g_plane_shape")
    reg_shape_missle("blue", "b_missile")
    reg_shape_missle("green", "g_missile")
    for x in range(1, 11):
        pic = "pics/expo-%d.gif" % x
        register_shape(pic)
    global p1, p2, p1_state, p2_state
    global blt_list1, blt_list2, misl_list1, misl_list2
    global life_list1, life_list2
    global gamepads
    global last_fire_time1, last_fire_time2
    last_fire_time1 = last_fire_time2 = 0
    p1_state = 0
    p2_state = 0
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
    for i in range(4):
        s_id = p1.stamp()
        life_list1.append(s_id)
        p1.fd(30)
    p1.setheading(270)
    p1.showturtle()

    p2 = Turtle(visible=False)
    p2.shape("g_plane_shape")
    p2.up()
    p2.goto(window_width() / 2 - 30, window_height() / 2 - 30)
    p2.setheading(180)
    for i in range(4):
        id = p2.stamp()
        life_list2.append(id)
        p2.fd(30)
    p2.setheading(270)
    p2.showturtle()

    onkey(p1_turn_left, "a")
    onkey(p1_turn_right, "d")
    onkey(p1_shoot, "space")
    onkey(p1_fire, "s")
    onkey(p1_turbo, "w")

    onkey(p2_turn_left, "Left")
    onkey(p2_turn_right, "Right")
    onkey(p2_shoot, "Up")
    onkey(p2_fire, "Down")
    onkey(p2_turbo, "Return")
    listen()

    gamepads = find_gamepad()
    if len(gamepads):
	do_gamepad()

    objects_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
