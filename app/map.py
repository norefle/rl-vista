from rlv.core.engine import Engine
from rlv.core.entity import Entity


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

        z_level = 0 # background
        for y in range(0, self.height):
            for x in range(0, self.width):
                index = y * self.width + x
                style = self.styles[self.level[index]]

                entity = Entity("%d:%d:%d" % (x, y, z_level), position=(64 * x, 64 * y, z_level))
                entity.add(Engine.get().image(style, entity=entity))
                self.data.append(entity)

