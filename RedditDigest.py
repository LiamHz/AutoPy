# Send the top posts of the past day from selected subreddits

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

# How many posts to send from each subreddit
subredditLimit = 2

# Selected subreddits
subreddits = ['Toronto', 'News', 'WorldNews', 'Technology', 'Science', 'TodayILearned', 'Philosophy', 'Videos']
              # 'Pics', 'MostBeautiful', 'EarthPorn']

subreddit = reddit.subreddit('EDM')
for SR in subreddits:
    count = 1
    subreddit = reddit.subreddit(SR)
    submissions.append(("<h2>{}</h2>").format(SR))
    for submission in subreddit.top(time_filter='day', limit=subredditLimit):
        submissions.append(("<a href='{}'>").format(submission.url))
        submissions.append(("<p>{}</p>").format(submission.title))
        submissions.append("</a>")
    submissions.append("<br>")

# Email results to self
fromaddr = EMAIL_USERNAME
toaddr = EMAIL_USERNAME

# Create message container
msg = MIMEMultipart('alternative')
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Reddit Digest"

# Plain text version of email
s = ''
formatted_submissions = s.join(submissions)

# HTML version of email
html = """\
<html>
  <head></head>
  <body>
    {}
  </body>
</html>
""".format(formatted_submissions)

# Allow Unicode characters to be emailed
plainText = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')
html = MIMEText(html, 'html')

msg.attach(plainText)
msg.attach(html)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, EMAIL_PASSWORD)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
