# Reddit Comment Bot

This Reddit Comment Bot is a Python-based auto-responder.

- Pick a subreddit to scan.
- Designate a specific comment to search for.
- Set your bot's reply.

### Requirements
- [Python](https://www.python.org/downloads/)
- [Praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html)
- A Reddit Account

### Setup

**Reddit App:**
1. [Navigate to the Apps page](https://www.reddit.com/prefs/apps/)
2. Click *create an app*
3. **name:** Set a name for your app
4. **type:** Script
5. **description:** Optional
6. **about url:** Optional
7. **redirect uri:** http://localhost:8080
8. Note the outputted *client id* and *secret*

**config.py:**
1. **REDDIT_USERNAME:** your Reddit username
2. **REDDIT_PASSWORD:** your Reddit password
3. **REDDIT_CLIENT_ID:** the outputted client id
4. **REDDIT_CLIENT_SECRET:** the outputted secret
5. **REDDIT_USER_AGENT:** a unique identifier for your bot
6. **TARGET_SUBREDDIT:** the subreddit to scan (default = "test")
7. **TARGET_STRING:** the comment search criteria (default = "sample user comment")
8. **REPLY_MESSAGE:** your bot's comment reply (default = "Hey, I like your comment!")
9. **SLEEP_DURATION:** sleep duration between bot runs in seconds (default = 10)

### Usage

- Navigate into the bot directory.
- Run your bot:
```sh
$ python reddit_bot.py
```