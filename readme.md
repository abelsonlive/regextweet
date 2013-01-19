### RegexTweet ###
RTs via RE's

To use `regextweet`, simple create an account, register an app, and copy these the keys found on [http://dev.twitter.com/apps](http://dev.twitter.com/apps) into a text file named `api.txt` in the project's root directory, i.e:
```
consumer_key
consumer_secret
access_token
access_token_secret
```

With `regextweet` we can quickly follow a list, filter information of interest, and retweet it. Here's the usage template:

```
python regextweet.py --u user_name --l list_name --o list_owner --r "regex" --a api.txt --h handles.txt
```

where:

* `--u` defines the user name of the retweetbot
* `--l` defines the name of the list to follow and filter,
* `--r` is the regular expression to query the text with.
* `--o` is the user name of the person who owns the list (optional; see below)
* `--a` is the filepath to the textfile with your api credentials (default = "api.txt")

* `--h` is the filepath to the textfile with the list of twitter users to follow (optional; regextweet will not bother with this if `--o` is provided, and will just follow the list `--l` owned by user `--o`.  If neither`--o` nor `--h` are provided, `--h` defaults to "header.txt" . If this is the case and "header.txt" does not exist, the program will break')


So for [RepsGunTweets](http://twitter.com/RepsGunTweets), where we retweeted from a the list named "members-of-congress" under [CSPAN's](http://www.twitter.com/cspan) account, we simply typed:

```
python regextweet.py --u repsguntweets --l members-of-congress --o cspan --r "(gun)"
```


### Make your own tweetbot

If you want to try out `regextweet.py` simply download the repository,  navigate to the extracted folder and customize `api.txt` and `handles.txt` according to your preferences.  Before running `regextweet.py`, make sure to run:

```
  sudo pip install tweepy oauth2 requests
```

which should cover the necessary dependencies.

Now you can create an account called "biebergoestowashington" and retweet every time a representative mentions justin bieber by simply typing:

```
python regextweet.py --u biebergoestowashington --l members-of-congress --o cspan --r "(bieber)"
```

## TODO

While `regextweet.py` only works for twitter feeds, the same idea could scale to facebook pages, rss feeds, and even CSPAN by using [opened-captions](https://github.com/slifty/opened-captions). Help me build something better!

