from rlv.core.component import Component
from rlv.core.engine import Engine
from rlv.core.event import Event

class Timer(Component):
    def __init__(self, name, parent, delay):
        super().__init__(name, parent)
        self.delay = delay
        self.dt = 0

    def on_update(self, dt):
        self.dt += dt
        if self.dt >= self.delay:
            Engine.get().emit(Event("timeout", source=self.entity))
            self.dt = 0

