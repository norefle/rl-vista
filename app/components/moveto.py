from rlv.core.component import Component


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

            (x, y, z) = self.entity.get_position()
            (tx, ty, _) = self.target
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
                self.notify(self.target)

            self.entity.set_position(position=(x, y, z))

            return True
        else:
            return False # Continue

