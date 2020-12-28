#!/usr/bin/env python3
"""This is mydemo.py, a test for turtle.py"""

from turtle import *


def reg_shape_plane(color, shape_name):
    s = Shape("compound")
    poly1 = ((0, -2), (10, -5), (0, 10), (-10, -5))
    s.addcomponent(poly1, color, color)
    poly2 = ((0, -2), (5, -8), (-5, -8))
    s.addcomponent(poly2, color, color)
    register_shape(shape_name, s)

def p1_fire():
    blt = Turtle(visible=False)
    tracer(2)
    blt.up()
    #blt.shape("")
    blt.shapesize(0.2, 0.2)
    #blt.fillcolor("black")
    blt.setpos(p1.xcor(), p1.ycor())
    blt.showturtle()
    tracer(1)
    #bs.append(blt)
def p2_fire():
    blt = Turtle()
def p1_turn_left():
    p1.left(10)

def p1_turn_right():
    p1.right(10)

def p2_turn_left():
    p2.left(10)

def p2_turn_right():
    p2.right(10)

def plane_move():
    global running
    running = True
    if running:

        if p1.xcor() >= window_width()/2 or p1.xcor() <= -window_width()/2:
            tracer(2)
            p1.setx(-p1.xcor())
            tracer(1)
            update()
        if p1.ycor() >= window_height()/2 or p1.ycor() <= -window_height()/2:
            tracer(2)
            p1.sety(-p1.ycor())
            tracer(1)
            update()
        p1.fd(3)


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
        p2.fd(3)
        ontimer(plane_move, 25)

def main():
    reg_shape_plane("blue", "b_plane_shape")
    reg_shape_plane("green", "g_plane_shape")
    global p1, p2
    global bs

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
    plane_move()

    return "EVENTLOOP"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()