"""Hanashiai - Core model module."""


class Comment():
    """Reddit comment object.

    Args:
        body (str): Comment text
        level (int): How deep in the comment tree the comment resides
        body_html (str): Comment text with HTML tags
        author (str): Comment author
        created_utc (str): Creation datetime
    """

    def __init__(self, body, level=0, body_html='', author='', created_utc=''):
        self.body = body
        self.level = level
        self.body_html = body_html
        self.author = author
        self.created_utc = created_utc
