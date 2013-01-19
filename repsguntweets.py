import requests
import tweepy
import re
from datetime import datetime
import time

# # THIS IS WHAT YOU CUSTOMIZE
retweetbot = "repsguntweets"
list_name = "members-of-congress"
list_owner = "cspan"
handles = "handles.txt"
regex = "(gunsafety)|(firearm)|(assault weapon)|(guncontrol)|(gunviolence)|(gun)|(nra)|(guns)|(nowisthetime)|(cartridges)|(second ammendment)|(bear arms)"

# api credentials
consumer_key="xxxxxxxxxxxxx"
consumer_secret="xxxxxxxxxxxxx"
access_token="xxxxxxxxxxxxx"
access_token_secret="xxxxxxxxxxxxx"
# END OF CUSTOMIZATION

#COMMENT_OUT_THIS_CHUNK_IF_LIST_IS_ALREADY_CREATED___________________________#
# authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# create list to populate
user_names = open(handles)
follower_list = []
while 1:
    lines = user_names.readlines(100000)
    if not lines:
        break
    for line in lines:
        follower_list.append(line.encode('utf-8'))
print "adding " + str(len(follower_list)) + " followers to " + list_name + "..."
api.create_list(list_name)

# populate list
for person in follower_list:
    print "..." + person + "..."
    try:
        api.add_list_member(list_name, person)
    except:
        print "cannot find", person
#END_OF_CHUNK________________________________________________________________#

# THIS IS THE TWEET BOT
authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# determine owner from input
owner = retweetbot
if list_owner is not "":
    owner = list_owner
# generate list url
list_url = "http://api.twitter.com/1/lists/statuses.json?slug=%s&owner_screen_name=%s&per_page=100&page=1&include_entities=true" % (list_name, owner)

# initialize a list for logging what the bot has tweeted
tweeted = []

# retweet forever
print  "now following: " + list_name + " by " + owner
while 1:

    # download json file of recent tweets
    r = requests.get(list_url)
    list_tweets = r.json

    # extract relevant tweets
    filtered_tweets = []
    for lt in list_tweets:
        id_str = lt['id_str'].encode('utf-8')
        name = lt['user']['screen_name'].encode('utf-8')
        text = lt['text'].encode('utf-8')

        # apply the regular expression to the tweet text
        if re.search(regex, text.lower()):
            filtered_tweets.append([id_str, name, text])

    # if we found a tweet, continue
    if len(ft) > 0:
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
    else:
        print "no relevant tweets found"

    # wait 5 minutes before starting again
    time.sleep(300)
