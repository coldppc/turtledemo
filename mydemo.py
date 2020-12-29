#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *

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
        # reuse bullet 0
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
        if not in_range(b.xcor(), 0, window_width()/2) or \
            not in_range(b.ycor(), 0, window_height()/2):
            b.hideturtle()
        else:
            b.fd(BLT_SPEED)
    for b in blt_list2:
        if not in_range(b.xcor(), 0, window_width()/2) or \
            not in_range(b.ycor(), 0, window_height()/2):
            b.hideturtle()
        else:
            b.fd(BLT_SPEED)
    ontimer(objects_move, 20)

def main():
    reg_shape_plane("blue", "b_plane_shape")
    reg_shape_plane("green", "g_plane_shape")
    global p1, p2
    global blt_list1, blt_list2
    blt_list1 = []
    blt_list2 = []
    p1 = Turtle()
    p1.shape("b_plane_shape")
    p2 = Turtle()
    p2.shape("g_plane_shape")
    onkeyrelease(p1_fire, "Up")
    onkeyrelease(p2_fire, "w")
    onkeyrelease(p1_turn_left, "Left")
    onkeyrelease(p1_turn_right, "Right")

    onkeyrelease(p2_turn_left, "a")
    onkeyrelease(p2_turn_right, "d")
    listen()
    p1.up()
    p2.up()
    objects_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()