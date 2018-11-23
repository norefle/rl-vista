"""
Entity class, has default properties valid for all other entities
and basic support for components.
"""

class Entity(object):
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.position = position
        self.components = {}

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_name(self):
        return self.name

    def get(self, name):
        return self.components.get(name)

    def add(self, component):
        self.components[component.get_name()] = component

    def remove(self, name):
        if self.components.get(name) is not None:
            self.components[name].kill()
            del self.components[name]

