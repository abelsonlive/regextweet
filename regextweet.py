import requests
import tweepy
import oauth2
import re
from datetime import datetime
import time
import sys

# # SETUP

# assign arguments to variables
arg_string = " ".join(sys.argv).encode("utf8")

# user: name of your tweetbot account
u = re.search("--u ([A-Za-z0-9-_]+)", arg_string)
if u is not None:
    retweetbot = u.group(1)
else :
    print "you must provide a user name for the retweetbot"

# determine owner of list
l = re.search('--l ([A-Za-z0-9-_]+)', arg_string)
if l is not None:
    list_name = l.group(1).strip()
else :
    print "you must provide a a name for the list to create / follow and filter"

# determine owner of list
o = re.search("--o ([A-Za-z0-9-_]+)", arg_string)
if o is not None:
    owner = o.group(1).strip()
else:
    owner = retweetbot

# regex
meta_regex = "--r (.*)"
r = re.search(meta_regex, arg_string)
if r is not None:
    regex = r.group(1).strip()
else:
    regex = "gun"

# api keys
a = re.search("--a ([A-Za-z0-9-_]+\.txt)", arg_string)
if a is not None:
    api_credentials = a.group(1).strip()
else:
    api_credentials = "api.txt"

# read in api credentials from api.txt
# api keys accessed from http://dev.twitter.com/apps
api_keys = open(api_credentials)
keys = []
while 1:
    lines = api_keys.readlines(5)
    if not lines:
        break
    for line in lines:
        keys.append(line.strip())

consumer_key = str(keys[0].strip())
consumer_secret = str(keys[1].strip())
access_token = str(keys[2].strip())
access_token_secret = str(keys[3].strip())

# authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# # IF LIST OWNER IS NOT PROVIDED, CREATE LIST

if o is None:

    # create list
    api.create_list(list_name)

    # opulate list
    # read in optional handle_path argument
    # defaults to "handles.txt" if this doesnt exist the program will break
    h = re.search("--h ([A-Za-z0-9-_]+)", arg_string)
    if h is not None:
        handle_path = h.group(1).strip()
    else:
        handle_path = "handles.txt"

    # read in textfile of handles
    user_names = open(handle_path)
    follower_list = []
    while 1:
        lines = user_names.readlines(100000)
        if not lines:
            break
        for line in lines:
            follower_list.append(line.encode('utf-8'))

    # populate list one at a time via api
    print "adding " + str(len(follower_list)) + " followers to " + list_name + "..."
    for person in follower_list:
        print "..." + person + "..."
        try:
            api.add_list_member(list_name, person)
        except:
            print "cannot find", person
    print "successfully added " + str(len(follower_list)) + " followers to " + list_name

# # RETWEET FOREVER # #

list_tweets = api.list_timeline(owner_screen_name = owner, slug =  list_name)
print  "now following: " + list_name + " by " + owner
# extract relevant tweets
filtered_tweets = []
for lt in list_tweets:
    id_str = lt.id_str.encode('utf-8')
    name = lt.user.screen_name.encode('utf-8')
    text = lt.text.encode('utf-8')

    # apply the regular expression to the tweet text
    if re.search(regex, text.lower()):
        filtered_tweets.append([id_str, name, text])

# if we found a tweet, continue
if len(filtered_tweets) == 0:
    print "no relevant tweets found @", datetime.now()
    
else:
    # retweet relevant tweets, reverse list to send out oldest messages first
    for ft in reversed(filtered_tweets):

        # extract the relvant tweet's id
        the_id = ft[0]

        # check if this id has not been tweeted yet - turns out twitter prevents this anyways.
        # i suppose this might save on api calls though
        if the_id not in tweeted:
            try:
                # print tweet to console
                print str(datetime.now()) + ", " + ft[1] + ": " + ft[2]

                # retweet via authenticated twitter handle
                api.retweet(the_id)

                # log the id of the tweet
                tweeted.append(the_id)

                # take a break
                time.sleep(1)

                # if anything goes wrong just move on.
                # rapid iterations should catch all relvant tweets
            except:
                pass
