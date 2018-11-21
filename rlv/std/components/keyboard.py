from rlv.core.component import Component

class Keyboard(Component):
    def __init__(self, name, parent, speed):
        super().__init__(name, parent)
        self.speed = speed

    def on_up(self, dt):
        (x, y) = self.entity.get_position()
        self.entity.set_position((x, y - dt * self.speed))
        return True

    def on_down(self, dt):
        (x, y) = self.entity.get_position()
        self.entity.set_position((x, y + dt * self.speed))
        return True
