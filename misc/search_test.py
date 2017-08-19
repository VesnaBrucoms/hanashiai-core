import time
from hanashiai.core.interface import RedditPort


reddit = RedditPort(name='Hanashiai',
                    version='0.0.1',
                    author='HanashiaiDev')

reddit.connect('anime')
results = reddit.search('knights of sidonia discussion')
print('\nDiscussions:')
for dis in results['discussions']:
    print(dis.title)

print('\nRewatches:')
for dis in results['rewatches']:
    print(dis.title)

comments = reddit.get_submission_comments(results['discussions'][0])
print(results['discussions'][0].title)
count = 0
for comment in comments:
    print(comment.body)
    count = count + 1
    if count == 10:
        break
