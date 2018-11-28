from rlv.core.entity import Entity
from rlv.core.engine import Engine
from rlv.core.event import Event
from rlv.core.image import Image
from rlv.core.label import Label


class UiBoard(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)

        self.add(Engine.get().image("ui/0", self))

        self.text = Entity("text-border", (position[0] + 15, position[1] + 35, position[2]))
        self.text.add(Engine.get().text("", 20, self.text))

        self.components["text"] = self.text.get("text")

