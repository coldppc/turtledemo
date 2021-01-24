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

team_color = {0: "black", 1: "blue", 2: "green", 3: "Orange"}
ST_READY = 0
ST_BORN = 1
ST_FLY = 2
ST_EXPLODE = 3
ST_TURBO = 4

class Flyobj(Turtle):
    """ flying turtle class """
    def __init__(self, team_id):
        super().__init__()
        self.state = ST_READY  # READY:0, BORN:1, FLY:2, EXPLODE:3, TURBO:4
        self.state_start = None  # start time of the state
        self.team_id = team_id
        self.fillcolor(team_color[self.team_id])
        self.shapes = {}  # shape dict
        self.speeds = {}  # state:speed dict
        self.up()

    def reg_shape(self, state, pic_prefix):
        """shape is string in dict, register all shapes used by this obj"""
        pass

    def get_shape(self, state, st_time):
        """get shape name from dict"""
        pass

    def do_job(self):
        """Move, change shape, check collision, switch state"""
        if self.state != ST_READY:
            self.fd(self.speeds[self.state])
        else:
            self.hideturtle()


class Plane(Flyobj):
    """
    Plane can turbo speed, has clone count, has life limit
    states = ["READY", "FLYING", "TURBO", "EXPLODE" ]
    """""
    def __init__(self, team_id):
        super().__init__(team_id)
        self.clone = 5
        self.life = 100  # 0 ~ 100 percent
        self.state = ST_FLY
        self.shape("turtle")
        self.speeds = {ST_READY: 0, ST_BORN: 0, ST_FLY: PLANE_SPEED, ST_TURBO: TURBO_SPEED, ST_EXPLODE: PLANE_SPEED}

    def do_job(self):
        """
        FLYING/TURBO/RESTORE-> Get keypad input,
        EXPLODE-> Change shape
        """
        super().do_job()


class Missile(Flyobj):
    """states = ["FLYING", "EXPLODE" ]"""
    def __init__(self, team_id, target_id):
        super().__init__(team_id)
        self.state = ST_FLY
        self.launch_time=0
        self.shape("circle")
        self.speeds = {ST_READY: 0, ST_BORN: 0, ST_FLY: MSLE_SPEED, ST_EXPLODE: MSLE_SPEED}

    def do_job(self):
        """
        FLYING-> Turn to target, check hit,
        EXPLODE-> Change shape
        """
        #  let's Flyobj do_job
        super().do_job()


class Bullet(Flyobj):
    """states = ["FLYING"]"""
    def __init__(self):
        super().__init__(0)
        self.state = ST_FLY
        self.fire_time=0
        self.shape("circle")
        self.speeds = {ST_READY: 0, ST_BORN: 0, ST_FLY: BLT_SPEED}

    def do_job(self):
        """FLYING-> check hit to all planes, missiles"""
        super().do_job()


def run():
    for p in planes:
        p.left(3)
        p.do_job()
    for m in missiles:
        m.right(3)
        m.do_job()
    for b in bullets:
        b.do_job()

    update()
    ontimer(run, 30) # 33.3 frame per second

def main():
    global planes, missiles, bullets
    planes = []
    missiles = []
    bullets = []
    tracer(False)
    for i in range(10):
        p = Plane(1)
        p.setheading(i * 30)
        planes.append(p)
    for i in range(10):
        m = Missile(2, 1)
        m.setheading(i * 20)
        missiles.append(m)
    for i in range(10):
        b = Bullet()
        b.setheading(i * 30)
        bullets.append(b)

    run()
    return "EVENTLOOP"


if __name__ == '__main__':
    main()
    mainloop()