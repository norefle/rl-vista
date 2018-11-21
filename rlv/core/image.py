from rlv.core.engine import Engine
from rlv.core.component import Component


class Image(Component):
    def __init__(self, name, parent, data, surface):
        super().__init__(name, parent)

        self.image = data
        self.screen = surface

    def on_render(self, dt):
        (x, y) = self.entity.get_position()
        self.screen.blit(self.image, (x, y))
        return False # Do not prevent other components from rendering
