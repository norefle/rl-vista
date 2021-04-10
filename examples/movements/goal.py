from rlv.core.engine import Engine
from rlv.core.entity import Entity
from rlv.core.image import Image
from config import config as cf


class Goal(Entity):
    def __init__(self, name, x, y, style):
        scale = cf["tile-size"]
        super().__init__(name, (x * scale, y * scale, cf["z-order"]["target"]))
        self.add(Engine.get().image(style=style, entity=self))

    def destroy(self):
        self.remove("image")
