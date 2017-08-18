from hanashiai.core.interface import RedditPort


reddit = RedditPort(name='Hanashiai',
                    version='0.0.1',
                    author='HanashiaiDev')

reddit.connect('anime')
results = reddit.search('knights of sidonia discussion')
print('Discussions\n')
for dis in results['discussions']:
    print(dis.title)

print('Rewatches\n')
for dis in results['rewatches']:
    print(dis.title)
