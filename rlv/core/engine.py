import pygame

from rlv.core.component import Component
from rlv.core.event import Event
from rlv.core.entity import Entity
from rlv.core.system import System
from rlv.core.image import Image
from rlv.core.label import Label


class Engine(object):
    _instance = None

    @staticmethod
    def get():
        return Engine._instance

    def __init__(self, width, height, styles, config):
        Engine._instance = self

        self.dt = 0
        self.frames = 0

        self.tile_size = config["tile"]
        self.images = {}

        self.events = System("events")
        self.draws = System("draws")

        self.events.register("text", Label)
        self.draws.register("image", Image)

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((width, height))

        for k, v in styles.items():
            self.images[k] = pygame.image.load(v)

        self.fps = Entity("fps", (width - 100, 5, 15))

    def register(self, name, factory):
        self.events.register(name, factory)

    def listen(self, component):
        self.events.listen(component)

    def image(self, style, entity):
        result = self.draws.create(
            "image"
            , parent=entity
            , data=self.images[style]
            , surface=self.screen
        )

        # hack
        self.draws.components.sort(key=lambda el: el.entity.get_position()[2])

        return result

    def text(self, content, size, entity):
        result = self.component(
                "text"
                , parent=entity
                , text=content
                , size=size
                , surface=self.screen
        )
        self.draws.listen(result)
        # hack
        self.draws.components.sort(key=lambda el: el.entity.get_position()[2])

        return result

    def component(self, name, **kwargs):
        return self.events.create(name, **kwargs)

    def emit(self, event):
        return self.events.emit(event)

    def render(self, dt):
        self._update_fps(dt)
        self.draws.emit(Event("render"))
        self.draws.pump(dt)
        pygame.display.flip()

    def update(self, dt):
        for event in pygame.event.get():
            self._process_input(event)

        self.events.emit(Event("update"))
        self.events.pump(dt)

    def _process_input(self, event):
            if event.type == pygame.QUIT:
                self.events.emit(Event("exit"))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.events.emit(Event("up"))
                elif event.key == pygame.K_DOWN:
                    self.events.emit(Event("down"))
                elif event.key == pygame.K_ESCAPE:
                    self.events.emit(Event("exit"))


    def _update_fps(self, dt):
        self.dt += dt
        self.frames += 1
        if self.fps.get("text") is None:
            self.fps.add(self.text("FPS: %d" % self.frames, 20, self.fps))

        if self.dt >= 1000:
            self.events.emit(Event(
                "settext"
                , text="FPS: %d" % self.frames
                , target=self.fps.get("text")
            ))
            self.dt = 0
            self.frames = 0

