import pygame
import datetime

from rlv.core.component import Component
from rlv.core.event import Event
from rlv.core.entity import Entity
from rlv.core.system import System

class Engine(Component):
    _instance = None

    @staticmethod
    def get():
        return Engine._instance

    def __init__(self, name, pipe, width, height, styles, config):
        super().__init__(name, None)

        self.dt = 0
        self.frames = 0

        Engine._instance = self

        self.tile_size = config["tile"]
        self.images = {}

        self.active = True
        self.pipe = pipe

        self.last = self._now_ms()

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((width, height))

        for k, v in styles.items():
            self.images[k] = pygame.image.load(v)

        self.fps = Entity("fps", (width - 100, 5))

    def image(self, style, entity):
        return self.component(
            "image"
            , parent=entity
            , data=self.images[style]
            , surface=self.screen
        )

    def text(self, content, size, entity):
        return self.component(
                "text"
                , parent=entity
                , text=content
                , size=size
                , surface=self.screen
        )

    def component(self, name, **kwargs):
        return self.pipe.create(name, **kwargs)

    def emit(self, event):
        return self.pipe.emit(event)

    def __next__(self):
        if not self.active:
            raise StopIteration()

        ms = self._now_ms()
        dt = ms - self.last
        self.last = ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.pipe.emit(Event("exit"))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.pipe.emit(Event("up"))
                elif event.key == pygame.K_DOWN:
                    self.pipe.emit(Event("down"))
                elif event.key == pygame.K_ESCAPE:
                    self.pipe.emit(Event("exit"))

        self.pipe.emit(Event("update"))
        self.pipe.emit(Event("render"))
        self.pipe.pump(dt)

        pygame.display.flip()

        self.dt += dt
        self.frames += 1
        if self.fps.get("text") is None:
            self.fps.add(self.text("FPS: %d" % self.frames, 20, self.fps))

        if self.dt >= 1000:
            self.emit(Event("settext", text="FPS: %d" % self.frames, target=self.fps.get("text")))
            self.dt = 0
            self.frames = 0

        return True

    def on_exit(self, dt):
        self.active = False

    @staticmethod
    def _now_ms():
        return int(datetime.datetime.utcnow().timestamp() * 1000)


