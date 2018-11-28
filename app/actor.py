from rlv.core.engine import Engine
from rlv.core.entity import Entity
from rlv.std.components.keyboard import Keyboard

class Actor(Entity):
    def __init__(self, name, position, style, speed):
        super().__init__(name, position)

        self.add(Engine.get().component("input", parent=self, speed=speed))
        self.image = Engine.get().image(style=style, entity=self)
