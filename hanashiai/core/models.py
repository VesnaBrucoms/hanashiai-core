"""Hanashiai - Core model module."""
import logging
from datetime import datetime

from prawcore.exceptions import ResponseException

from .exceptions import RedditResponseError


class Submission():
    """Reddit submission object.
    """

    def __init__(self, praw_submission):
        self._praw_submission = praw_submission

        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(name='hanashiai-core')

    @property
    def id(self):
        return self._praw_submission.id

    @property
    def title(self):
        return self._praw_submission.title

    def get_comments(self, replace_limit=0):
        """Get submission comments.

        Returns the comments and their replies from the submission.

        Kwargs:
            replace_limit (int): the number of "More comments" objects to
                                 replace, defaults to 0

        Returns:
            comments (Comment list): list of Hanashiai - Core Comment
                                     objects
        """
        try:
            self._praw_submission.comments.replace_more(limit=replace_limit)
        except ResponseException as exception:
            http_code = exception.response.status_code
            error_msg = 'Attempt to retreive submission "{}" returned ' \
                        'HTTP {}'.format(self._praw_submission, http_code)
            self._logger.error(error_msg)
            raise RedditResponseError(error_msg)

        comments = []
        for comment in self._praw_submission.comments:
            created_utc = datetime.fromtimestamp(comment.created_utc)
            new_comment = Comment(comment.body,
                                  body_html=comment.body_html,
                                  author=str(comment.author),
                                  created_utc=created_utc)
            comments.append(new_comment)
            if len(comment.replies) > 0:
                comments.extend(self._add_replies(comment, 1))

        return comments

    def _add_replies(self, parent_comment, level, limit=3):
        comments = []
        for reply in parent_comment.replies:
            created_utc = datetime.fromtimestamp(reply.created_utc)
            comments.append(Comment(reply.body,
                                    level=level,
                                    body_html=reply.body_html,
                                    author=str(reply.author),
                                    created_utc=created_utc))
            next_level = level + 1
            if len(reply.replies) > 0 and next_level <= limit:
                comments.extend(self._add_replies(reply, next_level))

        return comments


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
