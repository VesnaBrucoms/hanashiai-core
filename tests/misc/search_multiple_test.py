import time

from hanashiai.core import library_details
from hanashiai.core.interfaces import Subreddit


sr_anime = Subreddit(subreddit_name='anime',
                     app_name='Hanashiai',
                     app_version='core-{}'.format(library_details['version']),
                     app_author='HanashiaiDev')
sr_anime.connect()

results = sr_anime.search_multiple(['knights of sidonia', 'sidonia no kishi'])
print('\nDiscussions:')
for dis in results['discussions']:
    print(dis.title)

print('\nRewatches:')
for rew in results['rewatches']:
    print(rew.title)

sub_id = '22r9gx'
sub = sr_anime.get_submission(sub_id)
comments = sub.get_comments()
print('\n')
print(sub.title)
print(sub.selftext)
count = 0
for comment in comments:
    print('[COMMENT]')
    print(comment.body)
    print(comment.level)
    print(comment.body_html)
    print(comment.author)
    print(comment.created_utc)
    count = count + 1
    if count == 10:
        break
