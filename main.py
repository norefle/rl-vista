import random

from rlv.core.engine import Engine
from rlv.core.entity import Entity
from rlv.core.component import Component
from rlv.core.image import Image
from rlv.core.system import System
from rlv.std.actor import Actor
from rlv.std.components.keyboard import Keyboard
from rlv.std.components.timer import Timer

import assets.sample.config as cf

class Application(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.pipe = System("pipe")
        self.pipe.register("input", Keyboard)
        self.pipe.register("image", Image)
        self.pipe.register("game", Engine)
        self.pipe.register("timer", Timer)
        self.pipe.register("moveto", MoveTo)

        self.engine = self.pipe.create(
            "game"
            , pipe=self.pipe
            , width=self.width
            , height=self.height
            , styles=cf.styles
            , config=cf.config
        )

    def __iter__(self):
        return self.engine

class MoveTo(Component):
    def __init__(self, name, parent, target, speed, callback):
        super().__init__(name, parent)
        self.target = target
        self.speed = speed
        self.notify = callback

    def on_timeout(self, dt, source):
        if self.entity == source:
            if self.entity.get("timer") is None:
                return True

            (x, y) = self.entity.get_position()
            (tx, ty) = self.target
            delay = self.entity.get("timer").delay
            speed = self.speed
            if x < tx:
                x = min(tx, x + delay * speed)
            elif x > tx:
                x = max(tx, x - delay * speed)
            elif y < ty:
                y = min(ty, y + delay * speed)
            elif y > ty:
                y = max(ty, y - delay * speed)
            else:
                # Done, stop doing whatever we did
                self.entity.remove("timer")
                self.entity.remove("moveto")
                self.notify(self.target)

            self.entity.set_position(position=(x, y))

            return True
        else:
            return False # Continue

class Map(object):
    def __init__(self, level, width, height):
        self.styles = {
            0: "tile/0"
            , 1: "tile/1"
            , 2: "tile/2"
            , 3: "tile/3"
        }
        self.width = width
        self.height = height
        self.level = level
        self.data = []

        for y in range(0, self.height):
            for x in range(0, self.width):
                index = y * self.width + x
                style = self.styles[self.level[index]]
                
                entity = Entity("%d:%d" % (x, y), position=(64 * x, 64 * y))
                entity.add(Engine.get().image(style, entity=entity))
                self.data.append(entity)

def update(entity, actor, delay, speed):
    (x, y) = (random.randint(0, 19) * 64, random.randint(0, 14) * 64)
    style = "entity/%s" % random.randint(0, 11)

    entity.remove("image")
    entity.add(Engine.get().image(style=style, entity=entity))
    entity.set_position((x, y))

    actor.remove("timer")
    actor.remove("moveto")

    actor.add(Engine.get().component("timer", parent=actor, delay=delay))
    actor.add(Engine.get().component(
        "moveto"
        , parent=actor
        , target=(x, y)
        , speed=speed
        , callback=lambda target: update(entity, actor, delay, speed)
    ))


if __name__ == "__main__":
    # Create application with the size of the screen to render to
    app = Application(width=64 * 20, height=64 * 15)

    level = Map(
            width=20
            , height=15
            , level=
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3
            , 0, 2, 2, 1, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3
            , 0, 2, 2, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3
            , 0, 2, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2
            ]
    )

    # Obstacles, targets, whatever which is not background
    target_one = Entity(name="Box-1", position=(0, 0))
    target_two = Entity(name="Box-2", position=(0, 0))

    # Define actors here
    alice = Actor(
        name="Alice"
        , style="actor/0"
        , position=(0, 0)
        , speed=0.64
    )

    bob = Actor(
        name="Bob"
        , style="actor/2"
        , position=(10, 5)
        , speed=0.64
    )

    update(entity=target_one, actor=alice, delay=16, speed=0.2)
    update(entity=target_two, actor=bob, delay=20, speed=0.1)

    # Main loop, internally calls app.update(df) and then calls app.render()
    i = 0
    for _ in app:
        # Do model updates here
        i += 1

    print("Done")

