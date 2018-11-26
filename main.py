import random

from rlv.core.engine import Engine
from rlv.core.entity import Entity
from rlv.core.event import Event
from rlv.core.component import Component
from rlv.core.event import Event
from rlv.std.actor import Actor
from rlv.std.entities.uiboard import UiBoard

from app.application import Application
from app.map import Map

scores = {}
z_level_back = 0
z_level_targets = 5
z_level_actors = 10
z_level_ui = 15

def update(entity, actor, delay, speed):
    score = scores[actor.get_name()]
    score["score"] += 1
    if score["entity"].get("text") is None:
        score["entity"].add(Engine.get().text(
            content="%s: %d" % (actor.get_name(), score["score"])
            , size=20
            , entity=score["entity"]
        ))
    else:
        Engine.get().emit(Event(
            "settext"
            , text="%s: %d" % (actor.get_name(), score["score"])
            , target=score["entity"].get("text")
        ))

    (x, y, z) = (random.randint(0, 19) * 64, random.randint(0, 14) * 64, z_level_targets)
    style = "entity/%s" % random.randint(0, 11)

    entity.remove("image")
    entity.add(Engine.get().image(style=style, entity=entity))
    entity.set_position((x, y, z))

    actor.remove("timer")
    actor.remove("moveto")

    actor.add(Engine.get().component("timer", parent=actor, delay=delay))
    actor.add(Engine.get().component(
        "moveto"
        , parent=actor
        , target=entity
        , speed=speed
    ))


if __name__ == "__main__":
    # Create application with the size of the screen to render to
    width = 64 * 20
    height = 64 * 15
    app = Application(width=width, height=height)

    level = Map(
            width=20
            , height=15
            , level=
            [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3, 3, 3
            , 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3, 3, 3
            , 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 3, 3, 3
            , 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3, 1, 3, 3, 3, 3, 2, 2, 3
            , 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 3, 3, 3, 2, 2, 3, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 3, 2, 2, 2, 3, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3, 2, 2, 2, 2, 3
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2
            ]
    )

    # Obstacles, targets, whatever which is not background
    target_one = Entity(name="Box-1", position=(0, 0, z_level_targets))
    target_two = Entity(name="Box-2", position=(0, 0, z_level_targets))

    # Define actors here
    alice = Actor(
        name="Alice"
        , style="actor/0"
        , position=(0, 0, z_level_actors)
        , speed=0.64
    )

    bob = Actor(
        name="Bob"
        , style="actor/2"
        , position=(10, 5, z_level_actors)
        , speed=0.64
    )

    scores = {
        "Alice": {
            "score": 0
            , "entity": UiBoard("alice-score", (5, height - 105, z_level_ui))
        }
        , "Bob": {
            "score": 0
            , "entity": UiBoard("bob-score", (110, height - 105, z_level_ui))
        }
    }

    update(entity=target_one, actor=alice, delay=16, speed=0.2)
    update(entity=target_two, actor=bob, delay=16, speed=0.2)

    collider = Collider("collider")
    Engine.get().listen(collider)

    # Main loop, internally calls app.update(df) and then calls app.render()
    for _ in app:
        if len(collider.get_collisions()) > 0:
            for (source, target) in collider.get_collisions():
                update(entity=target, actor=source, delay=16, speed=0.2)
            collider.reset()

    print("Done")

