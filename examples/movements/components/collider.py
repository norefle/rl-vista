from rlv.core.component import Component


class Collider(Component):
    def __init__(self, name):
        super().__init__(name, None)
        self.collisions = []

    def on_collide(self, dt, source, target):
        self.collisions.append((source, target))

    def get_collisions(self):
        return self.collisions

    def reset(self):
        self.collisions = []

