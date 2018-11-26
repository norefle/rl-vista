import datetime

from rlv.core.engine import Engine
from rlv.core.component import Component
from rlv.std.components.keyboard import Keyboard
from rlv.std.components.timer import Timer
from app.components.collider import Collider
from app.components.moveto import MoveTo

import assets.sample.config as cf


class Application(Component):
    def __init__(self, width, height):
        super().__init__("app", None)

        self.width = width
        self.height = height

        self.engine = Engine(
            width=self.width
            , height=self.height
            , styles=cf.styles
            , config=cf.config
        )

        self.done = False
        self.last = 0
        self.dt = 0

        self.engine.register("input", Keyboard)
        self.engine.register("timer", Timer)
        self.engine.register("moveto", MoveTo)
        self.engine.register("collider", Collider)
        self.engine.listen(self)

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

