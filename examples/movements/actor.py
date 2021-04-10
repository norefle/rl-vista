from rlv.core.engine import Engine
from rlv.core.entity import Entity
from rlv.core.component import Component
from rlv.core.event import Event

from config import config as cf


class Actor(Entity, Component):
    def __init__(self, name, x, y, style):
        scale = cf["tile-size"]
        Entity.__init__(self, name, (x * scale, y * scale, cf["z-order"]["actor"]))
        Component.__init__(self, name, self)

        self.image = Engine.get().image(style=style, entity=self)

        Engine.get().listen(self)

    def move_to(self, x, y):
        scale = cf["tile-size"]
        self.add(
            Engine.get().component("timer", parent=self, delay=cf["actor"]["delay"])
        )
        self.add(
            Engine.get().component(
                "movetoxy",
                parent=self,
                x=x * scale,
                y=y * scale,
                speed=cf["actor"]["speed"],
            )
        )

    def jump_to(self, x, y):
        scale = cf["tile-size"]
        self.remove("timer")
        self.remove("movetoxy")

        (dx, dy, z) = self.get_position()
        self.set_position((x * scale, y * scale, z))

        Engine.get().emit(Event("done", source=self, action="jump"))

    def on_arrived_xy(self, dt, source, x, y):
        if source != self:
            return False

        self.remove("timer")
        self.remove("movetoxy")

        Engine.get().emit(Event("done", source=self, action="move"))

        return True
