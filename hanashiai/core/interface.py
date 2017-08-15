import logging
import os
import platform

import praw
from prawcore.exceptions import ResponseException


class RedditPort():

    def __init__(self, name, version, author):
        self._client_id = os.environ.get('CLIENT_ID', None)
        self._client_secret = os.environ.get('CLIENT_SECRET', None)
        self._user_agent = '{}:{}:{} (by /u/{})'.format(platform.system().lower(),
                                                        name,
                                                        version,
                                                        author)

        self._reddit = None
        self._subreddit = None

        logging.basicConfig(level=logging.INFO)

    def connect(self, subreddit):
        """Connect to reddit and retreive subreddit.

        Args:
            subreddit (str): Name of the subreddit to retreive
        """
        try:
            self._reddit = praw.Reddit(client_id=self._client_id,
                                       client_secret=self._client_secret,
                                       user_agent=self._user_agent)
            logging.info('Connected to reddit with user agent: %s',
                         self._user_agent)

            self._subreddit = self._reddit.subreddit(subreddit)
            logging.info('Retreived subreddit: %s', subreddit)
        except ResponseException as exception:
            logging.error('When connecting returned HTTP response: %s',
                          exception.response)

    def search(self, query):
        """Search the subreddit with the query.

        Args:
            query (str): Search query
        """
        submissions = []
        for result in self._subreddit.search(query):
            submissions.append(result)

        filtered_subs = self._filter_submissions(submissions)
        sorted_subs = self._sort_submissions(filtered_subs)

        return sorted_subs

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
                logging.info('Filtered submission: %s', sub.title)

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
