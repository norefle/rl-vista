from rlv.core.engine import Engine
from rlv.core.event import Event
from rlv.core.component import Component


class MoveToXY(Component):
    def __init__(self, name, parent, x, y, speed):
        super().__init__(name, parent)
        self.target = (x, y)
        self.speed = speed

    def on_timeout(self, dt, source):
        if self.entity == source:
            if self.entity.get("timer") is None:
                return True

            (x, y, z) = self.entity.get_position()
            (tx, ty) = self.target
            speed = self.speed
            if x < tx:
                x = min(tx, x + dt * speed)
            elif x > tx:
                x = max(tx, x - dt * speed)
            if y < ty:
                y = min(ty, y + dt * speed)
            elif y > ty:
                y = max(ty, y - dt * speed)

            if x == tx and y == ty:
                # Done, stop doing whatever we did
                self.entity.remove("timer")
                self.entity.remove("movetoxy")
                Engine.get().emit(Event("arrived_xy", source=self.entity, x=x, y=y))

            self.entity.set_position(position=(x, y, z))

            return True
        else:
            return False

