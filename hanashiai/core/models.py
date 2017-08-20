"""Hanashiai - Core model module."""


class Comment():
    """Reddit comment object.
    """

    def __init__(self, body, level=0):
        self.body = body
        self.level = level
