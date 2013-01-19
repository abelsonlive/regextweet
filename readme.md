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
  python regextweet.py --u user_name --l list_name --o list_owner --r "regex to filter tweets"
```

where:

* `--u` defines the user name of the retweetbot
* `--l` defines the name of the list to follow and filter,
* `--r` is the regular expression to query the text with.
* `--o` is the user name of the person who owns the list (optional; see below)
* `--a` is the filepath to the textfile with your api credentials (default = "api.txt")

* `--h` is the filepath to the textfile with the list of twitter users to follow (optional; seeblowretweety will not bother with this if `--o` is provided, and will just read in the list `--l` owned by user `--o`.  In addtion `--h` defaults to "header.txt" if neither`--o` nor `--h` are provided. If this is the case, and "header.txt" still does not exist, the program will break')


So for [RepsGunTweets](http://twitter.com/RepsGunTweets), where we retweeted from a the list named "members-of-congress" under [CSPAN's](http://www.twitter.com/cspan) account, we simply typed:

```python retweety.py --u repsguntweets --l members-of-congress --o cspan --r "(gun)"```


### Make your own tweetbot

If you want to try out `retweety.py` simply go to the [github page](http://www.github.com/abelsonlive/retweety) and download the repository.  Navigate to the downloaded and extracted folder and customized `api.txt` and `handles.txt` according to your preferences.  Before running `retweety.py`, make sure to run:

```
  sudo pip install tweepy oauth2 requests
```

which should cover the necessary dependencies.

Now you can create an account called "biebergoestowashington" and retweet every time a congress man or woman mentions justin bieber by simply typing:

```python regextweet.py --u biebergoestowashington --l members-of-congress --o cspan --r "(bieber)"```

