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

teams = {"black", "blue", "green", "orange"}
states = {"READY": "static", "BORN": "dynamic", "FLY": "static", "EXPLODE": "dynamic", "TURBO": "static"}

FPS = 50   # 50 FPS per second
ticks = 0  # screen updating ticks, there is FPS ticks every second.

class Flyobj(Turtle):
    """ flying turtle class """
    def __init__(self, team):
        super().__init__()
        self.state = "READY"  # READY:0, BORN:1, FLY:2, EXPLODE:3, TURBO:4
        self.state_start = 0   # start tick of the state
        self.team = team
        self.fillcolor(self.team)
        self.shapes = []  # shape set
        self.paces = dict()  # state:speed dict
        self.up()

    def reg_static_shape(self, state, polys):
        s = Shape("compound")
        c = self.team
        for poly in polys:
            s.addcomponent(poly, c, c)
        shape_id = self.team + state
        register_shape(shape_id, s)
        self.shapes.insert(0, shape_id)

    def reg_dynamic_shape(self, state, prefix, cnt):
        """pics/plane_explode_01.gif"""
        for i in range(cnt):
            image = "pics/%s_%s_%02d.gif" % (prefix, state.lower(), i)
            if image not in self.shapes:  # other plane may reg it already
                print("reg image:" + image)
                register_shape(image)
                self.shapes.append(image)

    def get_shape(self, state, st_ticks):
        """get shape from list"""
        shape_id = self.team + state
        if shape_id in self.shapes:
            return shape_id
        for s in self.shapes:
            image = "%s_%02d.gif" % (state.lower(), st_ticks % 10)
            if s.endswith(image):
                return s
        return "triangle"  # fall back shape

    def switch_state(self, state):
        if state == self.state:
            return
        self.state = state
        self.state_start = ticks
        if self.state == "READY":
            self.hideturtle()
            return
        # change shape now
        self.shape(self.get_shape(self.state, ticks - self.state_start))

    def do_job(self):
        """Move, change shape, check collision, switch state"""
        if self.state != "READY":
            self.fd(self.paces[self.state])
        if self.state == "EXPLODE":
            self.shape(self.get_shape(self.state, ticks - self.state_start))


class Plane(Flyobj):
    """
    Plane can turbo speed, has clone count, has life limit
    states = ["READY", "FLY", "TURBO", "EXPLODE" ]
    """""
    def __init__(self, team):
        super().__init__(team)
        self.clone = 5
        self.life = 100  # 0 ~ 100 percent
        #self.state = "FLY"
        #self.shape("turtle")
        self.paces = {"READY": 0, "BORN": 0, "FLY": PLANE_SPEED, "TURBO": TURBO_SPEED, "EXPLODE": PLANE_SPEED}
        self.reg_static_shape("FLY", [((0, 20), (-4, -8), (0, -6), (4, -8)), ((0, 16), (-12, -2), (12, -2))])
        self.reg_static_shape("TURBO", [((0, 20), (-4, -8), (0, -6), (4, -8)), ((0, 16), (-12, -2), (12, -2))])
        self.reg_dynamic_shape("EXPLODE", "", 10)

        print(self.shapes)

    def do_job(self):
        """
        FLYING/TURBO/RESTORE-> Get keypad input,
        EXPLODE-> Change shape
        """
        if (ticks / FPS) < 3:
            self.switch_state("TURBO")
        elif (ticks / FPS) < 6:
            self.switch_state("FLY")
        else:
            self.switch_state("EXPLODE")
        super().do_job()


class Missile(Flyobj):
    """states = ["FLY", "EXPLODE" ]"""
    def __init__(self, team, target_team):
        super().__init__(team)
        self.state = "FLY"
        self.reg_static_shape("FLY", [((-1, 0), (0, 12), (1, 0))])
        self.reg_dynamic_shape("EXPLODE", "", 10)
        self.paces = {"READY": 0, "BORN": 0, "FLY": MSLE_SPEED, "EXPLODE": MSLE_SPEED}

    def do_job(self):
        """
        FLYING-> Turn to target, check hit,
        EXPLODE-> Change shape
        """
        if (ticks / FPS) < 5:
            self.switch_state("FLY")
        elif (ticks / FPS) < 6:
            self.switch_state("EXPLODE")
        else:
            self.switch_state("READY")

        #  let's Flyobj do_job
        super().do_job()


class Bullet(Flyobj):
    """states = ["FLY"]"""
    def __init__(self):
        super().__init__("black")
        self.state = "FLY"
        self.fire_time=0
        self.shape("circle")
        self.paces = {"READY": 0, "BORN": 0, "FLY": BLT_SPEED}

    def do_job(self):
        """FLYING-> check hit to all planes, missiles"""
        super().do_job()


def run():
    global ticks
    for p in planes:
        p.left(3)
        p.do_job()
    for m in missiles:
        m.right(3)
        m.do_job()
    for b in bullets:
        b.do_job()

    update()
    ticks = ticks + 1
    ontimer(run, int(1000/FPS))  # FPS frame per second


def main():
    global planes, missiles, bullets
    planes = []
    missiles = []
    bullets = []
    tracer(False)
    for i in range(10):
        p = Plane("blue")
        p.setheading(i * 30)
        planes.append(p)
    for i in range(10):
        m = Missile("green", "blue")
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