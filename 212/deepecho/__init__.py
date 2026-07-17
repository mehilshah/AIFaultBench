"""Lightweight test doubles for the external deepecho package."""


class PARModel:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
