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
from .models import Submission, Comment


class Subreddit():
    """Provides an interface to a specfied subreddit.

    Allows easy access to common tasks such as searching submissions.

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
        self._last_search_cache = []

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
        try:
            self._logger.info('Searching %s with query "%s"...',
                              self._subreddit.name,
                              query)
            submissions = []
            for result in self._subreddit.search(query, limit=300):
                new_submission = Submission(result)
                submissions.append(new_submission)

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
        self._last_search_cache = filtered_subs
        filtered_subs.sort(key=_get_order_key)
        sorted_subs = self._sort_submissions(filtered_subs)

        return sorted_subs

    def get_submission(self, submission_id):
        """Get single submission from subreddit.

        Args:
            submission_id (str): Submission's unique identifier.
        """
        self._logger.info('Getting submission with id %s', submission_id)
        submission = self._get_cached_submission(submission_id)
        if not submission:
            self._logger.debug('No cached submission with id %s, '
                               'performing search', submission_id)
            submission = self._search_single_submission(submission_id)

        return submission

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
                self._logger.debug('Filtered submission: %s', sub.title)

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

    def _get_cached_submission(self, submission_id):
        self._logger.debug('Getting cached submission with id %s',
                           submission_id)
        submission = None
        for cached_submission in self._last_search_cache:
            if submission_id == cached_submission.id:
                submission = cached_submission
                break

        return submission

    def _search_single_submission(self, submission_id):
        self._logger.debug('Searching for single submission with id %s',
                           submission_id)
        searched_submission = self._reddit.submission(id=submission_id)
        submission = Submission(searched_submission)

        return submission


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
