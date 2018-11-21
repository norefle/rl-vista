"""
Base class for all components
"""

class Component(object):
    def __init__(self, name, parent):
        self.name = name
        self.entity = parent
        self.alive = True

    def get_name(self):
        return self.name

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

