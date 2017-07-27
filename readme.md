# Reddit Comment Bot
This Reddit Comment Bot is a python-based auto-responder.
  - Pick a subreddit to scan
  - Designate a specific comment to search for
  - Set your bot's reply

### Requirements
  - [Python](https://www.python.org/downloads/)
  - [Praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html)
  - A Reddit Account

### Setup
###### Reddit App:
1. [Navigate to the Apps page ](https://www.reddit.com/prefs/apps/)
2. Click *create an app*
3. **name:** Set a name for your app
4. **type:** Script
5. **description:** Optional
6. **about url:** Optional
7. **redirect uri:** http://localhost:8080
8. Note the outputted *client id* and *secret*

###### config.py:
1. **username:** your Reddit username
2. **password:** your Reddit password
3. **client_id:** the outputted client id
4. **client_secret:** the outputted secret

###### reddit_bot.py:

Set the subreddit to search (default = "r/test"):
```python
r.subreddit('test')
```
Comment search criteria (default = "sample user content"):
```python
if "sample user comment"
```
Bot's comment reply (default = "Hey, I like your comment!"):
```python
comment.reply("Hey, I like your comment!")
```

### Usage

Navigate into the bot directory.
Run your bot:
```sh
$ python reddit_bot.py
```