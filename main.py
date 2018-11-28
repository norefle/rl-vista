import random

from rlv.core.engine import Engine
from rlv.core.component import Component

from rlv.core.entity import Entity
from rlv.core.event import Event

from app.application import Application

from app.actor import Actor
from app.goal import Goal
from app.uiboard import UiBoard

class State(object):
    def __init__(self):
        self.all = ["INIT"]

    def on_done(self, source, action):
        last = "%s:%s" % (source.get_name(), action)
        self.all.append(last)


if __name__ == "__main__":
    # Create application with the size of the screen to render to
    width = 20
    height = 15

    state = State()
    app = Application(
        width=width
        , height=height
        , done_callback=lambda source, action: state.on_done(source, action)
    )

    app.set_map(
        width=width
        , height=height
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

    app.add_actor(Actor("Alice", x=0, y=0, style="actor/0"))
    app.add_actor(Actor("Bob", x=3, y=3, style="actor/2"))

    app.add_target(Goal("tree-1", x=10, y=10, style="entity/10"))
    app.add_target(Goal("tree-2", x=5, y=14, style="entity/10"))
    app.add_target(Goal("tree-3", x=18, y=2, style="entity/10"))
    app.add_target(Goal("tree-4", x=1, y=6, style="entity/10"))
    app.add_target(Goal("tree-5", x=7, y=3, style="entity/10"))

    msg = UiBoard("Chat", 0, 13)

    clock = Entity("BobClock", (0, 0, 0))
    clock.add(Engine.get().component("timer", delay=5000, parent=clock)) # 5 seconds
    goal_clock = Entity("GoalClock", (0, 0, 0))
    goal_clock.add(Engine.get().component("timer", delay=1000, parent=goal_clock))

    i = 0
    for _ in app:
        (ax, ay) = (random.randint(0, width - 1), random.randint(0, height - 1))
        (bx, by) = (random.randint(0, width - 1), random.randint(0, height - 1))
        for last in state.all:
            if last == "INIT":
                i += 1
                msg.add_message("%d Alice: going to (%d, %d)" % (i, ax, ay))
                app.get_actor("Alice").move_to(x=ax, y=ay)
                i += 1
                msg.add_message("%d Bob: jumping to (%d, %d)" % (i, bx, by))
                app.get_actor("Bob").jump_to(x=bx, y=by)
            if last == "Alice:move":
                i += 1
                msg.add_message("%d Alice: moving to (%d, %d)" % (i, ax, ay))
                app.get_actor("Alice").move_to(x=ax, y=ay)
            elif last == "BobClock:timeout":
                i += 1
                msg.add_message("%d Bob: jumping to (%d, %d)" % (i, bx, by))
                app.get_actor("Bob").jump_to(x=bx, y=by)
            elif last == "GoalClock:timeout":
                app.drop_target("random")
                app.add_target(Goal(
                    "random"
                    , x=random.randint(0, width - 1)
                    , y=random.randint(0, height -1)
                    , style="entity/%d" % random.randint(0, 11)
                ))

        state.last = None
        state.all = []

    print("Done")

