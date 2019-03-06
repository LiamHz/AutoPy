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

num_submissions = 1

for submission in subreddit.search('flair:New', sort='top', time_filter='week'):
    # Only print submissions that are for songs
    print(submission.title)
    submissions.append("<div> \n")
    submissions.append(("<a href='{}'> \n").format(submission.url))
    submissions.append(("<p>{}</p> \n").format(submission.title))
    submissions.append("</a> \n")
    submissions.append("</div> \n")
    submissions.append("<br class='mobile'> \n")
    num_submissions += 1
    if num_submissions >= 10:
        break

s = '\n'
formatted_submissions = s.join(submissions)

# Read mailing list
searching = True
numUsers = 0
EMAIL_MAILING_LIST = []

f = open("EDM-DigestMailingList.txt", 'r')
lines = f.read().splitlines()

# Add users to mailing list
while searching:
    try:
        if lines[0 + numUsers] == "":
            searching = False
        else:
            EMAIL_MAILING_LIST.append(lines[0 + numUsers])
            numUsers += 1
    # If there are no more lines in the mailing list file
    # Then there are no more user to mail to
    except IndexError:
        searching = False

f.close()

# The current user being serviced
userIndex = 0

while userIndex < len(EMAIL_MAILING_LIST):
    # Email results to self
    fromaddr = EMAIL_USERNAME
    toaddr = EMAIL_MAILING_LIST[userIndex]

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "EDM Digest"

    # Plain text version of email
    s = ''
    formatted_submissions = s.join(submissions)

    # HTML version of email
    html = """\
    <html>
        <head>
            <style>
                @media only screen and (min-width:800px) {{
                    .mobile {{display: none !important;}}
                }}
            </style>
        </head>
        <body>
            {}
        </body>
    </html>
    """.format(formatted_submissions)

    # Allow Unicode characters to be emailed
    plainText = MIMEText(formatted_submissions.encode('utf-8'), 'plain', 'UTF-8')
    html = MIMEText(html, 'html')

    # msg.attach(plainText)
    msg.attach(html)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, EMAIL_PASSWORD)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

    userIndex += 1
