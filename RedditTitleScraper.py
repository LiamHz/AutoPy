# Email the titles of the top 25 posts from a specified subreddit

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

submissions = []
reddit = praw.Reddit(client_id=API_USERNAME,
                     client_secret=API_PASSWORD,
                     password=REDDIT_PASSWORD,
                     username=REDDIT_USERNAME,
                     user_agent='RedditDigest')

subreddit = reddit.subreddit('OneGoodSentence')

for submission in subreddit.top('all'):
    submissions.append(submission.title)
    if len(submissions) >= 25:
        break

s = '\n\n'
formatted_submissions = s.join(submissions)#.encode('utf-8').strip()

print(formatted_submissions)

# Email results to self
fromaddr = EMAIL_USERNAME
toaddr = EMAIL_USERNAME
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Top posts of r/{}".format(subreddit)

body = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')
msg.attach(body)


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, EMAIL_PASSWORD)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
