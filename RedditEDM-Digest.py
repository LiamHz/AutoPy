# Email the titles of the top 10 new songs from r/EDM

import praw

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Print the top 10 new songs of the week in the EDM subreddit
submissions = []
reddit = praw.Reddit(client_id='UFc9vhBQpf3ZgA',
                     client_secret='mHkj6yxCi-JMFQUjC8fS748Jdt4',
                     password="G8t0inSwe0RZcr7k",
                     username='Wallfacer42',
                     user_agent='RedditDigest')

subreddit = reddit.subreddit('EDM')

for submission in subreddit.search('flair:New', sort='top', time_filter='week'):
    # Only print submissions that are for songs
    print(submission.title)
    submissions.append(submission.title)
    if len(submissions) >= 10:
        break

s = '\n'
formatted_submissions = s.join(submissions)

# Email results to self
fromaddr = "liam.hinzman@gmail.com"
toaddr = "liam.hinzman@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Reddit Digest: New EDM Tracks"

# Allow Unicode characters to be emailed
text = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')

msg.attach(text)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Atwummt3Tihhb1Bdnf4Swb1Icnfty5")
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
