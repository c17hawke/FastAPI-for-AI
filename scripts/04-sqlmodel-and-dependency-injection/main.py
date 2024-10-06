from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel import Field as SQLField

DATABASE_URL = "sqlite:///./trial.db"
engine = create_engine(DATABASE_URL)


class TweetBase(SQLModel):
    tweet: str = SQLField(..., min_length=1, max_length=280)

class Tweet(TweetBase, table=True):
    timestamp: str = SQLField(..., primary_key=True, index=True, regex=r"^\d{14}$")
    user_name: str = SQLField(index=True)
    edited_timestamp: Optional[str] = SQLField(regex=r"^\d{14}$")

class TweetCreate(TweetBase):
    pass

def get_utc_timestamp() -> str:
    """returns timestamp in format YYYYMMDDHHMMSS in UTC"""
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

def get_session():
    with Session(engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI(on_startup=[create_db])

@app.get("/home", response_model=list[Tweet])
async def twitter_timeline(session: Session = Depends(get_session)):
    # SELECT * FROM tweet;
    tweets = session.exec(select(Tweet)).all()
    if not tweets:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No tweets present!")
    return tweets

@app.get("/{user_name}", response_model=list[Tweet])
async def user_timeline(user_name: str, session: Session = Depends(get_session)):
    user_tweets = session.exec(select(Tweet).where(Tweet.user_name == user_name)).all()
    if not user_tweets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user: {user_name} not found!")
    return user_tweets

@app.post("/{user_name}", response_model=Tweet)
async def post_tweet(user_name: str, tweet: TweetCreate, session: Session = Depends(get_session)):
    new_tweet = Tweet(timestamp=get_utc_timestamp(), tweet=tweet.tweet, user_name=user_name)
    session.add(new_tweet)
    session.commit()
    session.refresh(new_tweet)
    return new_tweet

@app.put("/{user_name}/{timestamp}")
async def update_tweet(user_name: str, timestamp: str, tweet: TweetCreate, session: Session = Depends(get_session)) -> JSONResponse:
    tweet_to_update = session.get(Tweet, timestamp)
    if not tweet_to_update or tweet_to_update.user_name != user_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found")
    tweet_to_update.tweet= tweet.tweet
    tweet_to_update.edited_timestamp = get_utc_timestamp()
    session.commit()
    session.refresh(tweet_to_update)
    return JSONResponse(
        content=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} is updated!",
        status_code=status.HTTP_202_ACCEPTED
    )


@app.delete("/{user_name}/{timestamp}")
async def delete_tweet(user_name: str, timestamp: str, session: Session = Depends(get_session)) -> JSONResponse:
    tweet_to_delete = session.get(Tweet, timestamp)
    if not tweet_to_delete or tweet_to_delete.user_name != user_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} not found")
    session.delete(tweet_to_delete)
    session.commit()
    return JSONResponse(
        content=f"Tweet with timestamp: {timestamp}, and user_name: {user_name} is deleted!",
        status_code=status.HTTP_202_ACCEPTED
    )
