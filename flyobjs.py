#!/usr/bin/env python3
"""A game with flying objects"""

from turtle import *
import random
import math
import time
import platform

PLANE_SPEED = 4
TURBO_SPEED = PLANE_SPEED * 2
BLT_SPEED = PLANE_SPEED * 4
MSLE_SPEED = PLANE_SPEED * 2
MSLE_LIFE = 8
MSLE_TURN = 2.5 # missile turn degree
HIT_RANGE = 15

team_color = {1: "blue", 2: "green", 3: "Orange"}


class Flyobj(Turtle):
    """ flying turtle class """
    def __init__(self, team_id):
        Turtle.__init__(self)
        self.state = 0  # READY:0, BORN:1, FLY:2, EXPLODE:3, TURBO:4
        self.state_start = None  # start time of the state
        self.team_id = team_id
        self.shapes = {}  # shape dict
        if team_id == 1:
            self.shape("turtle")
        else:
            self.shape("circle")
        self.up()

    def reg_shape(self, state, pic_prefix):
        """shape is string in dict, register all shapes used by this obj"""
        pass

    def get_shape(self, state, st_time):
        """get shape name from dict"""
        pass

    def do_myjob(self):
        """Move, change shape, check collision, switch state"""
        if self.team_id == 1:
            self.fd(5)
        else:
            self.fd(8)


class Plane(Flyobj):
    """ Plane can turbo speed, has clone count, has life limit"""
    states = ["FLYING", "TURBO", "RESTORE", "EXPLODE" ]
    def __init__(self, team_id):
        self.clone = 5
        self.life = 100  # 0 ~ 100 percent
        up()

    def do_myjob(self):
        """
        FLYING/TURBO/RESTORE-> Get keypad input,
        EXPLODE-> Change shape
        """
        #print(self.do_myjob.__doc__)
        fd(PLANE_SPEED)

class Missile(Flyobj):
    states = ["FLYING", "EXPLODE" ]
    def __init__(self, team_id, target_id):
        self.launch_time=0
        up()
        shapesize(5)
        fillcolor("red")
        shape("turtle")

    def do_myjob(self):
        """
        FLYING-> Turn to target, check hit,
        EXPLODE-> Change shape
        """
        fd(MSLE_SPEED)

class Bullet(Flyobj):
    states = ["FLYING"]
    def __init__(self):
        self.fire_time=0
        up()
        shapesize(0.15)
        fillcolor("black")
        shape("circle")
    def do_myjob(self):
        """FLYING-> check hit to all planes, missiles"""
        fd(BLT_SPEED)

def run():
    #p1.do_myjob()
    #b1.do_myjob()
    #m2.do_myjob()
    f1.do_myjob()
    f2.do_myjob()

    update()
    ontimer(run, 300) # 33.3 frame per second

def main():
    global p1, m2, b1, f1, f2
    tracer(False)
    #p1 = Plane(1)
    #m2 = Missile(2,1)
    #b1 = Bullet()
    f1 = Flyobj(1)
    f2 = Flyobj(2)


    run()
    return "EVENTLOOP"

if __name__ == '__main__':
    main()
    mainloop()