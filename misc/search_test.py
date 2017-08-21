import time
from hanashiai.core.interface import Subreddit


sr_anime = Subreddit(subreddit='anime',
                   app_name='Hanashiai',
                   app_version='0.0.1',
                   app_author='HanashiaiDev')

results = sr_anime.search('knights of sidonia discussion')
print('\nDiscussions:')
for dis in results['discussions']:
    print(dis.title)

print('\nRewatches:')
for dis in results['rewatches']:
    print(dis.title)

comments = sr_anime.get_submission_comments(results['discussions'][0])
print(results['discussions'][0].title)
count = 0
for comment in comments:
    print('[COMMENT]')
    print(comment.body)
    print(comment.level)
    count = count + 1
    if count == 10:
        break
