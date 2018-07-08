import time

from hanashiai.core import library_details
from hanashiai.core.interfaces import Subreddit


sr_anime = Subreddit(subreddit_name='anime',
                     app_name='Hanashiai',
                     app_version='core-{}'.format(library_details['version']),
                     app_author='HanashiaiDev')
sr_anime.connect()

results = sr_anime.search('knights of sidonia discussion')
print('\nDiscussions:')
for dis in results['discussions']:
    print(dis.title)

print('\nRewatches:')
for rew in results['rewatches']:
    print(rew.title)

comments = sr_anime.get_submission_comments(results['discussions'][0])
print(results['discussions'][0].title)
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
