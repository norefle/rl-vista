"""
Event
"""


class Event(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.data = kwargs

    def get_name(self):
        return self.name

    def get_data(self):
        return self.data

