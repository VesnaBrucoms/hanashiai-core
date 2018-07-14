import unittest
from unittest import mock

from hanashiai.core.interfaces import Subreddit


class TestInterfaces(unittest.TestCase):

    def setup_method(self, method):
        self._subreddit = Subreddit(subreddit_name='test',
                                    app_name='Test App',
                                    app_version='0.0.1',
                                    app_author='Tester')

    def teardown_method(self, method):
        pass

    def test_filter_submissions(self):
        mock_sub_one = mock.Mock()
        mock_sub_one.title = '[SPOILERS] Test discussion'
        mock_sub_two = mock.Mock()
        mock_sub_two.title = '[Rewatch] Test rewatch'
        mock_sub_three = mock.Mock()
        mock_sub_three.title = 'Not what we are looking for'
        subs = [mock_sub_one, mock_sub_two, mock_sub_three]
        filtered_submissions = self._subreddit._filter_submissions(subs)

        expected_submissions = [mock_sub_one,
                                mock_sub_two]
        self.assertEqual(expected_submissions, filtered_submissions)

    def test_sort_submissions(self):
        mock_sub_one = mock.Mock()
        mock_sub_one.title = '[SPOILERS] Test discussion'
        mock_sub_two = mock.Mock()
        mock_sub_two.title = '[Rewatch] Test rewatch'
        subs = [mock_sub_one, mock_sub_two]
        sorted_submissions = self._subreddit._sort_submissions(subs)

        expected_submissions = {'discussions': [mock_sub_one],
                                'rewatches': [mock_sub_two]}
        self.assertEqual(expected_submissions, sorted_submissions)

    def test_get_cached_submission(self):
        mock_sub_one = mock.Mock()
        mock_sub_one.id = '123ab'
        mock_sub_two = mock.Mock()
        mock_sub_two.id = '456cd'
        self._subreddit._last_search_cache = [mock_sub_one, mock_sub_two]
        returned_sub = self._subreddit._get_cached_submission('456cd')

        self.assertEqual(mock_sub_two, returned_sub)

    def test_get_cached_submission_failure(self):
        mock_sub_one = mock.Mock()
        mock_sub_one.id = '123ab'
        mock_sub_two = mock.Mock()
        mock_sub_two.id = '456cd'
        self._subreddit._last_search_cache = [mock_sub_one, mock_sub_two]
        returned_sub = self._subreddit._get_cached_submission('test')

        self.assertEqual(None, returned_sub)
