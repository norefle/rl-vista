import pygame
from rlv.core.component import Component


class Label(Component):
    def __init__(self, name, parent, text, size, surface):
        super().__init__(name, parent)

        self.font = pygame.font.SysFont("Roboto", size)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.screen = surface
    
    def on_settext(self, dt, text, target):
        if target == self:
            self.text = self.font.render(text, True, (0, 0, 0))
            return True
        else:
            return False

    def on_render(self, dt):
        (x, y, z) = self.entity.get_position()
        self.screen.blit(self.text, (x, y))
        return False # Do not prevent other components from rendering
