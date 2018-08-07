# Email the titles of the top 10 new songs from r/EDM

import praw

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read user credentials from external file
f = open("AuthenticationCredentials.txt","r")
lines = f.read().splitlines()
EMAIL_USERNAME = lines[1]
EMAIL_PASSWORD = lines[2]
REDDIT_USERNAME = lines[5]
REDDIT_PASSWORD = lines[6]
API_USERNAME = lines[9]
API_PASSWORD = lines[10]
f.close()

# Print the top 10 new songs of the week in the EDM subreddit
submissions = []
reddit = praw.Reddit(client_id=API_USERNAME,
                     client_secret=API_PASSWORD,
                     password=REDDIT_PASSWORD,
                     username=REDDIT_USERNAME,
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
fromaddr = EMAIL_USERNAME
toaddr = EMAIL_USERNAME
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "EDM Digest"

# Allow Unicode characters to be emailed
text = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')

msg.attach(text)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, EMAIL_PASSWORD)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
