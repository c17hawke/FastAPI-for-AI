from fastapi import FastAPI
import time

app = FastAPI()


# in memory tweets
tweets = [
  {
    "timestamp": "20240929101921",
    "tweet": "Hello AI",
    "user_name": "c17hawke"
  },
  {
    "timestamp": "20240929101930",
    "tweet": "Hello world!",
    "user_name": "c17hawke"
  },
  {
    "timestamp": "20240929102013",
    "tweet": "Its an amazing day!",
    "user_name": "User1"
  }
]

def get_timestamp() -> str:
    """returns timestamp in format YYYYMMDDHHMMSS"""
    return time.strftime("%Y%m%d%H%M%S")


@app.get("/home")
async def twitter_timeline():
    return tweets


@app.get("/{user_name}")
async def user_timeline(user_name: str):
    user_tweets = [tweet for tweet in tweets if tweet["user_name"] == user_name]
    if not user_tweets:
        return {"error": f"user: {user_name} not found"}
    return user_tweets

@app.post("/{user_name}")
async def post_tweet(user_name: str, tweet: dict):
    new_tweet =   {
        "timestamp": get_timestamp(),
        "tweet": tweet["tweet"],
        "user_name": user_name
    }
    tweets.append(new_tweet)
    return new_tweet

@app.put("/{user_name}/{timestamp}")
async def update_tweet(user_name: str, timestamp: str, tweet: dict):
    tweet_to_update = next((_tweet for _tweet in tweets if _tweet["timestamp"]==timestamp and _tweet["user_name"] == user_name), None)

    if not tweet_to_update:
        return {
            "error": f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found"
        }
    tweet_to_update["tweet"] = tweet["tweet"]
    tweet_to_update["edited_timestamp"] = get_timestamp()
    return tweet_to_update

@app.delete("/{user_name}/{timestamp}")
async def delete_tweet(user_name: str, timestamp: str):
    tweet_to_delete = next((_tweet for _tweet in tweets if _tweet["timestamp"]==timestamp and _tweet["user_name"] == user_name), None)
    if not tweet_to_delete:
        return {
            "error": f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found"
        }
    tweets.remove(tweet_to_delete)
    return {
            "message": f"Tweet with timestamp: {timestamp}, and user_name: {user_name} is deleted!"
        }