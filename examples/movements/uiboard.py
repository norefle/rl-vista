from rlv.core.entity import Entity
from rlv.core.engine import Engine
from rlv.core.event import Event
from rlv.core.image import Image
from rlv.core.label import Label

from config import config as cf


class UiBoard(Entity):
    def __init__(self, name, x, y):
        scale = cf["tile-size"]
        z_order = cf["z-order"]["ui"]
        padding = 28

        super().__init__(name, (x * scale + padding, y * scale, z_order))

        self.boards = []
        self.messages = []

        # for i in range(0, 5):
        #    # scale by x is 100 as UI width is 100
        #    entity = Entity("board:%s" % i, ((x + i) * 100 + padding, y * scale, z_order))
        #    entity.add(Engine.get().image("ui/0", entity))
        #    self.boards.append(entity)

        self.line_1 = Entity(
            "line-1", (x * scale + padding + 15, y * scale + 15, z_order)
        )
        self.line_1.add(Engine.get().text("", 20, self.line_1))

        self.line_2 = Entity(
            "line-2", (x * scale + padding + 15, y * scale + 55, z_order)
        )
        self.line_2.add(Engine.get().text("", 20, self.line_2))

    def add_message(self, message):
        self.messages.append(message)

        if len(self.messages) > 0:
            Engine.get().emit(
                Event("settext", target=self.line_2, text=self.messages[-1])
            )
        if len(self.messages) > 1:
            Engine.get().emit(
                Event("settext", target=self.line_1, text=self.messages[-2])
            )
