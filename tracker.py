import os
import praw

def login():
    client = praw.Reddit(
        username      = os.environ.get('REDDIT_USER'),
        password      = os.environ.get('REDDIT_PASS'),
        client_id     = os.environ.get('CLIENT_ID'),
        client_secret = os.environ.get('CLIENT_SECRET'),
        user_agent    = 'FantanoBot tracker'
    )
    return client

def run(client):
    for comment in client.user.me().comments.new(limit=None):
        if comment.score < 0:
            msg = "**Score:** {score}\n**Comment:** {body}\n**Link:** {link}".format(
                score = comment.score,
                body  = comment.body,
                link  = 'https://reddit.com' + comment.permalink
            )
            client.user.me().message('Contentious Response', msg)
            print("Contentious score:\n\n" + msg)

client = login()
run(client)