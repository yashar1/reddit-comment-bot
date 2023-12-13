# Importing necessary libraries
from __future__ import print_function
import praw
import prawcore
import time
import os
import logging
from config import (
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    TARGET_SUBREDDIT,
    TARGET_STRING,
    REPLY_MESSAGE,
    SLEEP_DURATION,
)

# Configuring logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to handle rate limit with exponential backoff
def handle_rate_limit(api_exception, retry_attempts=3):
    for attempt in range(retry_attempts):
        retry_after = api_exception.response.headers.get('retry-after')
        if retry_after:
            logger.warning(f"Rate limited. Retrying after {retry_after} seconds. Attempt {attempt + 1}/{retry_attempts}")
            time.sleep(int(retry_after) + 1)
        else:
            logger.error(f"API Exception: {api_exception}")
            break
    else:
        logger.error("Exceeded retry attempts. Aborting.")
        raise

# Function to log in to Reddit
def bot_login():
    logger.info("Logging in...")
    
    try:
        reddit_instance = praw.Reddit(
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        logger.info("Logged in!")
        return reddit_instance
    except prawcore.exceptions.ResponseException as e:
        logger.error(f"Login failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during login: {e}")
        raise

# Function to run the bot
def run_bot(reddit_instance, comments_replied_to):
    logger.info(f"Searching last 1,000 comments in subreddit {TARGET_SUBREDDIT}")

    try:
        process_comments(reddit_instance, comments_replied_to)
    except praw.exceptions.APIException as api_exception:
        # Handle rate limits
        handle_rate_limit(api_exception)
    except Exception as e:
        # Log other exceptions
        logger.exception(f"An error occurred: {e}")

    logger.info(f"Sleeping for {SLEEP_DURATION} seconds...")
    time.sleep(int(SLEEP_DURATION))

# Function to process comments
def process_comments(reddit_instance, comments_replied_to):
    for comment in reddit_instance.subreddit(TARGET_SUBREDDIT).comments(limit=1000):
        try:
            process_single_comment(comment, comments_replied_to)
        except prawcore.exceptions.Forbidden as forbidden_error:
            logger.warning(f"Permission error for comment {comment.id}: {forbidden_error}. Skipping.")
        except Exception as error:
            logger.exception(f"Error processing comment {comment.id}: {error}")

    # Log when the search is completed
    logger.info("Search Completed.")
    # Log the count of comments replied to
    logger.info(f"Number of comments replied to: {len(comments_replied_to)}")

# Function to process a single comment
def process_single_comment(comment, comments_replied_to):
    if (
        TARGET_STRING in comment.body
        and comment.id not in comments_replied_to
        and comment.author != reddit_instance.user.me()
    ):
        # Log when the target string is found in a comment
        logger.info(f"String with '{TARGET_STRING}' found in comment {comment.id}")
        # Reply to the comment with the predefined message
        try:
            comment.reply(REPLY_MESSAGE)
            # Log that the bot has replied to the comment
            logger.info(f"Replied to comment {comment.id}")

            # Add the comment ID to the list of comments replied to
            comments_replied_to.append(comment.id)

            # Save the comment ID to the file
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
        except prawcore.exceptions.Forbidden as forbidden_error:
            logger.warning(f"Permission error for comment {comment.id}: {forbidden_error}. Skipping.")
        except Exception as reply_error:
            logger.exception(f"Error while replying to comment {comment.id}: {reply_error}")

# Function to get saved comments
def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        # If the file doesn't exist, initialize an empty list
        comments_replied_to = []
    else:
        # Read the file and create a list of comments (excluding empty lines)
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = [comment.strip() for comment in f.readlines() if comment.strip()]

    return comments_replied_to

# Main block to execute the bot
if __name__ == "__main__":
    # Log in to Reddit
    reddit_instance = bot_login()
    # Get the list of comments the bot has replied to from the file
    comments_replied_to = get_saved_comments()
    # Log the number of comments replied to
    logger.info(f"Number of comments replied to: {len(comments_replied_to)}")

    # Run the bot in an infinite loop
    while True:
        try:
            # Attempt to run the bot
            run_bot(reddit_instance, comments_replied_to)
        except Exception as e:
            # Log any general exceptions and sleep for the specified duration
            logger.exception(f"An error occurred: {e}")
            time.sleep(int(SLEEP_DURATION))  # Add a sleep after catching general exceptions
        except KeyboardInterrupt:
            logger.info("Bot terminated by user.")
            break
