"""Hanashiai - Core interfaces module.

This module contains classes to easily interface with key elements
of Reddit, such as a subreddit.
"""
import logging
import os
import platform
import re
from datetime import datetime

import praw
from prawcore.exceptions import ResponseException

from .exceptions import RedditResponseError
from .models import Comment


class Subreddit():
    """Provides an interface to a specfied subreddit.

    Allows easy access to common tasks such as searching and retreiving
    a submission's comments.

    Args:
        subreddit_name (str): Name of the subreddit to interact with.
        app_name (str): Name of the app as specified on Reddit.
        app_version (str): App released version.
        app_author (str): Reddit username app was created with.
    """

    def __init__(self, subreddit_name, app_name, app_version, app_author):
        self._subreddit_name = subreddit_name
        self._client_id = os.environ.get('CLIENT_ID', None)
        self._client_secret = os.environ.get('CLIENT_SECRET', None)
        platform_name = platform.system().lower()
        self._user_agent = '{}:{}:{} (by /u/{})'.format(platform_name,
                                                        app_name,
                                                        app_version,
                                                        app_author)

        self._reddit = None
        self._subreddit = None

        logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(name='hanashiai-core')

    def connect(self):
        """Create reddit and subreddit instances."""
        self._reddit = praw.Reddit(client_id=self._client_id,
                                   client_secret=self._client_secret,
                                   user_agent=self._user_agent)
        self._logger.info('Created reddit instance with user agent: %s',
                          self._user_agent)

        self._subreddit = self._reddit.subreddit(self._subreddit_name)
        self._logger.info('Subreddit set to "/r/%s"', self._subreddit_name)

    def search(self, query):
        """Search the subreddit with the passed query.

        Searches the subreddit with the query, and then filters,
        orders, and sorts the results before returning to the caller.

        Args:
            query (str): Search query

        Returns:
            sorted_subs (dict): Dictionary of two lists. One with "discussions"
                                as the key, and the other with "rewatches".
        """
        submissions = []
        try:
            self._logger.info('Searching %s with query "%s"...',
                              self._subreddit.name,
                              query)
            for result in self._subreddit.search(query, limit=300):
                submissions.append(result)

            self._logger.info('Returned %i results', len(submissions))
        except ResponseException as exception:
            http_code = exception.response.status_code
            error_msg = 'Search with query "{}" returned HTTP {}' \
                        .format(query, http_code)
            if http_code == 401:
                self._logger.error('%s, you are unauthorised to connect to'
                                   ' reddit, are you using the correct ID'
                                   ' and secret?', error_msg)
            elif http_code == 302:
                self._logger.error('%s, subreddit may not exist', error_msg)
            else:
                self._logger.error(error_msg)

            raise RedditResponseError(error_msg)

        filtered_subs = self._filter_submissions(submissions)
        filtered_subs.sort(key=_get_order_key)
        sorted_subs = self._sort_submissions(filtered_subs)

        return sorted_subs

    def get_submission_comments(self, sub_id, replace_limit=0):
        """Get the comments for passed submission.

        Returns the comments and their replies from the submission
        specified via the submission's ID.

        Args:
            sub_id (str): the submission's ID

        Kwargs:
            replace_limit (int): the number of "More comments" objects to
                                 replace, defaults to 0

        Returns:
            comments (Comment list): list of Hanashiai - Core Comment
                                     objects
        """
        submission = self._reddit.submission(id=sub_id)
        try:
            submission.comments.replace_more(limit=replace_limit)
        except ResponseException as exception:
            http_code = exception.response.status_code
            error_msg = 'Attempt to retreive submission "{}" returned ' \
                        'HTTP {}'.format(sub_id, http_code)
            self._logger.error(error_msg)
            raise RedditResponseError(error_msg)

        comments = []
        for comment in submission.comments:
            created_utc = datetime.fromtimestamp(comment.created_utc)
            comments.append(Comment(comment.body,
                                    body_html=comment.body_html,
                                    author=str(comment.author),
                                    created_utc=created_utc))
            if len(comment.replies) > 0:
                comments.extend(self._add_replies(comment, 1))

        return comments

    def _filter_submissions(self, submissions):
        filtered_subs = []
        for sub in submissions:
            normalised_title = sub.title.lower()
            checklist = []
            checklist.append(normalised_title.find('[spoilers]'))
            checklist.append(normalised_title.find('[rewatch]'))
            filtered = True
            for check in checklist:
                if check > -1:
                    filtered_subs.append(sub)
                    filtered = False
                    break

            if filtered:
                self._logger.info('Filtered submission: %s', sub.title)

        return filtered_subs

    def _sort_submissions(self, submissions):
        sorted_subs = {'discussions': [], 'rewatches': []}
        for sub in submissions:
            normalised_title = sub.title.lower()
            if normalised_title.find('[rewatch]') > -1:
                sorted_subs['rewatches'].append(sub)
            else:
                sorted_subs['discussions'].append(sub)

        return sorted_subs

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


def _get_order_key(value):
    regex = r'(((E|e)pisode|(E|e)p|OVA|ova)\s)([0-9]{1,4})(\s(D|d)iscussion)*'
    match_groups = re.search(regex, value.title)

    order_key = 0
    if match_groups is None:
        order_key = 5000
    else:
        order_key = int(match_groups.groups()[4])
        if match_groups.groups()[1].lower() == 'ova':
            order_key = order_key + 1000

    return order_key
