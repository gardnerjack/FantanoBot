import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bmemcached
from re import search
import time
import os

sheet_url = 'https://docs.google.com/spreadsheets/d/1GbGyWVtePH8RZCZd7N3RPDh8m-K6hgO6AyKsAHZpbeQ/edit?usp=sharing'
service_account = 'fantanobot@fantanobot.iam.gserviceaccount.com'

print('INITIALISING ...')
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_p12_keyfile(service_account, 'securecert.p12', os.environ['CERT_PASS'], scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url(sheet_url).worksheet('All Reviews')

mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
     os.environ.get('MEMCACHEDCLOUD_USERNAME'),
     os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

footer = "\n\nAll scores sourced from [here](https://docs.google.com/spreadsheets/d/1GbGyWVtePH8RZCZd7N3RPDh8m-K6hgO6AyKsAHZpbeQ/edit#gid=0).\n\n---\n^(I am a bot and this action was performed automatically)  \n^(Send me a PM to provide feedback)"

def retrieve_album(album_name):
    album_name = album_name.strip()
    print('retrieving album', album_name, '...')
    try:
        cell = sheet.find(album_name)
        assert(cell.col == 2)
        values = sheet.row_values(cell.row)
        print('success')
        return "Artist: *{0}*  \nAlbum: {1}  \nScore: **{2}**".format(values[0], values[1], values[2])
    except:
        print('fail')
        return None

def retrieve_artist(artist_name):
    artist_name = artist_name.strip()
    print('retrieving artist', artist_name, '...')
    try:
        albums = []
        for cell in sheet.findall(artist_name):
            if cell.col != 1:
                continue
            values = sheet.row_values(cell.row)
            albums.append('{0} - **{1}**'.format(values[1], values[2]))
        assert(len(albums) > 0)
        print('success')
        return "Fantano's album scores for *{0}*:\n\n{1}".format(artist_name, '  \n'.join(albums))
    except:
        print('fail')
        return None

def login():
    print('logging in ...')
    client = praw.Reddit(username=os.environ['REDDIT_USER'],
                         password=os.environ['REDDIT_PASS'],
                         client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'],
                         user_agent='FantanoBot responder')
    return client

def run(client):
    for comment in client.subreddit('fantanoforever+hiphopheads').comments(limit=None):
        if mc.get(str(comment.id)) is not None:
            print(comment.id)
            print(comment.body)
            print()
        if mc.get(str(comment.id)) is not None or comment.author == client.user.me():
            continue

        find = search('!fantanobot (.*)', comment.body)
        if find is not None:
            print('found comment:', find.group(1))
            print(comment.id)
            term = find.group(1)
            response = retrieve_album(term)
            if response is None:
                response = retrieve_artist(term)

            if response is not None:
                print(response)
                # comment.reply(response + footer)
                # mc.set(str(comment.id), "True")

client = login()
run(client)

# mc.set("e24et4b", "True")
# mc.set("e24obb0", "True")
# mc.set("e24oxj3", "True")
# mc.set("e24rvj6", "True")
# mc.set("e24z0lj", "True")
# mc.set("e253jqt", "True")
# mc.set("e24nww6", "True")
# mc.set("e24nww6", "True")
# mc.set("e24s0ng", "True")
# mc.set("e24u4ch", "True")
# mc.set("e24wbuc", "True")
# mc.set("e257ctj", "True")
# mc.set("e25f953", "True")
# mc.set("e25k48j", "True")