from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

app = FastAPI()

class Tweet(BaseModel):
    tweet: str = Field(..., min_length=1, max_length=280)

class TweetInDB(Tweet):
    timestamp: Annotated[str, StringConstraints(pattern=r"^\d{14}$")]
    user_name: str
    edited_timestamp: Annotated[str, StringConstraints(pattern=r"^\d{14}$")] | None = None

# in memory tweets
tweets_db = [
    TweetInDB(timestamp="20240929101921", tweet="Hello AI", user_name="c17hawke"),
    TweetInDB(timestamp="20240929101930", tweet="Hello world!", user_name="c17hawke"),
    TweetInDB(timestamp="20240929102013", tweet="Its an amazing day!", user_name="User1")
]

def get_utc_timestamp() -> str:
    """returns timestamp in format YYYYMMDDHHMMSS in UTC"""
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


@app.get("/home", response_model=list[TweetInDB])
async def twitter_timeline():
    if tweets_db:
        return tweets_db
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No tweets present!")

@app.get("/{user_name}", response_model=list[TweetInDB])
async def user_timeline(user_name: str):
    user_tweets = [tweet for tweet in tweets_db if tweet.user_name == user_name]
    if not user_tweets:
        return {"error": f"user: {user_name} not found"}
    return user_tweets

@app.post("/{user_name}", response_model=TweetInDB)
async def post_tweet(user_name: str, tweet: Tweet):
    new_tweet = TweetInDB(timestamp=get_utc_timestamp(), tweet=tweet.tweet, user_name=user_name)
    tweets_db.append(new_tweet)
    return new_tweet

@app.put("/{user_name}/{timestamp}")
async def update_tweet(user_name: str, timestamp: str, tweet: Tweet) -> JSONResponse:
    tweet_to_update = next((_tweet for _tweet in tweets_db if _tweet.timestamp==timestamp and _tweet.user_name == user_name), None)
    if not tweet_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found")
    tweet_to_update.tweet= tweet.tweet
    tweet_to_update.edited_timestamp = get_utc_timestamp()
    return JSONResponse(
        content=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} is updated!",
        status_code=status.HTTP_202_ACCEPTED
    )


@app.delete("/{user_name}/{timestamp}")
async def delete_tweet(user_name: str, timestamp: str) -> JSONResponse:
    tweet_to_delete = next((_tweet for _tweet in tweets_db if _tweet.timestamp==timestamp and _tweet.user_name == user_name), None)
    if not tweet_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found")
    tweets_db.remove(tweet_to_delete)
    return JSONResponse(
        content=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} is deleted!",
        status_code=status.HTTP_202_ACCEPTED
    )
