"""
System, provides functionality to create, register, and remove components.
"""

from rlv.core.component import Component


class System(object):
    def __init__(self, name):
        self.name = name
        self.factories = {}
        self.components = []
        self.events = []

    def register(self, name, factory):
        self.factories[name] = factory

    def create(self, name, **kargs):
        if self.factories.get(name) is not None:
            component = self.factories[name](name=name, **kargs)
            self.components.append(component)

            return component
        else:
            raise NameError("Invalid component %s" % name)

    def emit(self, event):
        self.events.append(event)

    def pump(self, dt):
        self.components = [item for item in self.components if item.is_alive()]

        events = self.events
        self.events = []

        for event in events:
            for component in self.components:
                if self._process(dt, component, event):
                    break

    @staticmethod
    def _process(dt, component, event):
        handle = getattr(component, "on_" + event.get_name(), None)
        if callable(handle):
            return handle(dt=dt, **event.get_data())

        return False

