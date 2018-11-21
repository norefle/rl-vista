import pytest

from rlv.core.system import System
from rlv.core.component import Component
from rlv.core.event import Event


class MockComponent(Component):
    def __init__(self, name, value):
        super().__init__(name, None)
        self.value = value

    def on_update(self, df, key, value):
        self.value = "%s -> %s" % (key, value)
        return True


def test_create_should_throw_on_invalid_name():
    system = System(name="Test")
    with pytest.raises(NameError) as e:
        system.create("test", value="111")


def test_create_should_return_registered_component():
    system = System(name="Test")
    system.register("mock", MockComponent)

    actual = system.create("mock", value="What if?!")

    assert actual.value == "What if?!"


def test_pump_should_remove_dead_components():
    system = System(name="Test")
    system.register("dead", MockComponent)

    dead = system.create("dead", value="I'm dead")
    dead.kill()

    assert len(system.components) == 1

    system.pump(0)

    assert len(system.components) == 0


def test_pump_should_pass_event_to_component():
    system = System(name="Test")
    system.register("mock", MockComponent)

    actual = system.create("mock", value="")
    event = Event("update", key="ABC", value="DEF")

    system.emit(event)
    system.pump(0)

    assert actual.value == "ABC -> DEF"

