from rlv.core.engine import Engine
from rlv.core.event import Event
from rlv.core.component import Component


class MoveToTarget(Component):
    def __init__(self, name, parent, target, speed):
        super().__init__(name, parent)
        self.target = target
        self.speed = speed

    def on_timeout(self, dt, source):
        if self.entity == source:
            if self.entity.get("timer") is None:
                return True

            (x, y, z) = self.entity.get_position()
            (tx, ty, _) = self.target.get_position()
            delay = self.entity.get("timer").delay
            speed = self.speed
            if x < tx:
                x = min(tx, x + delay * speed)
            elif x > tx:
                x = max(tx, x - delay * speed)
            if y < ty:
                y = min(ty, y + delay * speed)
            elif y > ty:
                y = max(ty, y - delay * speed)

            if x == tx and y == ty:
                # Done, stop doing whatever we did
                self.entity.remove("timer")
                self.entity.remove("moveto")
                Engine.get().emit(Event("collide", source=self.entity, target=self.target))

            self.entity.set_position(position=(x, y, z))

            return True
        else:
            return False # Continue

