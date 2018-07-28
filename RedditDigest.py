# Send the top posts of the past day from selected subreddits

import praw

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

submissions = []
reddit = praw.Reddit(client_id='UFc9vhBQpf3ZgA',
                     client_secret='mHkj6yxCi-JMFQUjC8fS748Jdt4',
                     password="G8t0inSwe0RZcr7k",
                     username='Wallfacer42',
                     user_agent='RedditDigest')

# How many posts to send from each subreddit
subredditLimit = 2

# Selected subreddits
subreddits = ['Toronto', 'News', 'WorldNews', 'Technology', 'Science', 'TodayILearned', 'Philosophy']
# Include link to post
# 'Videos', 'WritingPrompts', 'Pics', 'MostBeautiful', 'EarthPorn', 'InterestingAsFuck' (Filter for only photos)

subreddit = reddit.subreddit('EDM')
for SR in subreddits:
    count = 1
    subreddit = reddit.subreddit(SR)
    submissions.append(("<h2>{}</h2>").format(SR))
    for submission in subreddit.top(time_filter='day', limit=subredditLimit):
        # Only print submissions that are for songs
        print(submission.title)
        submissions.append(("<p>{}</p>").format(submission.title))

# Email results to self
fromaddr = "liam.hinzman@gmail.com"
toaddr = "liam.hinzman@gmail.com"

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
server.login(fromaddr, "Atwummt3Tihhb1Bdnf4Swb1Icnfty5")
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
