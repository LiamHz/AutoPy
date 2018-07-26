# Email the titles of the top 25 posts from a specified subreddit

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

subreddit = reddit.subreddit('OneGoodSentence')

for submission in subreddit.top('all'):
    submissions.append(submission.title)
    if len(submissions) >= 25:
        break

s = '\n\n'
formatted_submissions = s.join(submissions)#.encode('utf-8').strip()

print(formatted_submissions)

# Email results to self
fromaddr = "liam.hinzman@gmail.com"
toaddr = "liam.hinzman@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Top posts of r/{}".format(subreddit)

body = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')
msg.attach(body)


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Atwummt3Tihhb1Bdnf4Swb1Icnfty5")
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
