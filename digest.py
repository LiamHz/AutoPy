# Print the top 10 new songs of the week in the EDM subreddit

import praw
match = 0

reddit = praw.Reddit(client_id='UFc9vhBQpf3ZgA',
                     client_secret='mHkj6yxCi-JMFQUjC8fS748Jdt4',
                     password="G8t0inSwe0RZcr7k",
                     username='Wallfacer42',
                     user_agent='RedditDigest')

subreddit = reddit.subreddit('EDM')

for submission in subreddit.search('flair:New', sort='top', time_filter='week'):
    # Only print submissions that are for songs
    if submission.link_flair_text == 'New':
        print(submission.title)
        match += 1
    if match >= 10:
        break
