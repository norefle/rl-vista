import datetime

from rlv.core.engine import Engine
from rlv.core.component import Component
from rlv.std.components.keyboard import Keyboard
from rlv.std.components.timer import Timer
from components.collider import Collider
from components.movetotarget import MoveToTarget
from components.movetoxy import MoveToXY
from map import Map

import config as cf


class Application(Component):
    def __init__(self, width, height, screen_width, screen_height, done_callback):
        super().__init__("app", None)

        scale = cf.config["tile-size"]
        self.width = width * scale
        self.height = height * scale
        self.callback = done_callback
        self.map = None
        self.actors = {}
        self.targets = {}

        self.engine = Engine(
            width=self.width,
            height=self.height,
            viewport_width=screen_width,
            viewport_height=screen_height,
            styles=cf.styles,
        )

        self.done = False
        self.last = 0
        self.dt = 0

        self.engine.register("input", Keyboard)
        self.engine.register("timer", Timer)
        self.engine.register("moveto", MoveToTarget)
        self.engine.register("movetoxy", MoveToXY)
        self.engine.register("collider", Collider)
        self.engine.listen(self)

    def set_map(self, width, height, level):
        if self.map is not None:
            # Drop map here
            self.map = None

        self.map = Map(width=width, height=height, level=level)

    def add_actor(self, actor):
        self.actors[actor.get_name()] = actor

    def get_actor(self, name):
        return self.actors[name]

    def add_target(self, target):
        self.targets[target.get_name()] = target

    def get_target(self, name):
        return self.targets[name]

    def drop_target(self, name):
        target = self.targets.get(name)
        if target is not None:
            for key in target.components.keys():
                target.get(key).kill()
            del self.targets[name]

    def on_timeout(self, dt, source):
        self.on_done(dt, source, "timeout")
        return False

    def on_done(self, dt, source, action):
        self.callback(source=source, action=action)
        return True

    def on_exit(self, dt):
        self.done = True
        return True

    def __iter__(self):
        return self

    def __next__(self):
        if self.done:
            raise StopIteration

        ms = self.now()
        dt = ms - self.last
        self.last = ms

        self.dt += dt
        if self.dt > 16:
            Engine.get().update(self.dt)
            self.dt = 0

        Engine.get().render(dt)

        return True

    @staticmethod
    def now():
        return int(datetime.datetime.utcnow().timestamp() * 1000)
