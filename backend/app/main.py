from os import access
from services.bot_detection import get_bot_detection_service
from services.instagram import get_instagram_service
from services.redis import get_redis
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.settings import Settings, get_settings
from internal.models import ScoreUserRes, ScoreUsersReq, UserScore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def publish_message():
    get_bot_detection_service()


@app.get("/status")
async def root():
    return {"message": "OK"}


@app.post("/score")
async def asses_users(users: ScoreUsersReq):
    settings = get_settings()
    storage = get_redis(
        settings.redis_endpoint, settings.redis_password, settings.redis_port
    )

    bot = get_bot_detection_service()
    scores = {}

    for username in users.users:
        try:
            if not storage.has_user_data(username):
                # continue
                insta = get_instagram_service()
                # Fetch instagram data
                data = insta.get_data_by_username(username)
                data = bot.format_instagram_response(data)
                storage.store_user(username, data=data)
            else:
                data = storage.get_user_data(username)
            score = bot.score_users([data])
            scores[username] = UserScore(
                username=username,
                score_is_fake=score[0][1],
                score_is_not_fake=score[0][0],
            )
        except Exception as e:
            print(e)
            scores[username] = {"error": "error"}

    return scores


# @app.get("/{username}/score")
# async def user_score(username: str):
#     # insta = get_instagram_service()
#     bot = get_bot_detection_service()

#     # print(service.get_data_by_username(username))
#     return {"item_id": username, "is_fake": bot.score_user()}


@app.get("/{username}/info")
async def user_info(username: str):
    service = get_instagram_service()
    user = service.get_data_by_username(username)

    if not user:
        return {"message": "invalid user name"}
    account_data = user.dict()
    return {
        "user_media_count": account_data["media_count"],
        "user_follower_count": account_data["follower_count"],
        "user_following_count": account_data["following_count"],
        # "user_has_highlight_reels": account_data["userHasHighlighReels"],
        "user_has_external_url": bool(account_data["external_url"]),
        # "user_tags_count": account_data["userTagsCount"],
        "follower_following_ratio": account_data["follower_count"]
        / max(1, account_data["following_count"]),
        "user_biography_length": len(account_data["biography"]),
        "username_length": len(account_data["username"]),
        "username_digit_count": sum(c.isdigit() for c in account_data["username"]),
        "user_is_private": account_data["is_private"],
        # "media_comment_numbers": account_data["mediaCommentNumbers"],
        # "media_comments_are_disabled": account_data["mediaCommentNumbers"],
        # "media_has_location_info": account_data["mediaHasLocationInfo"],
        # "media_hashtag_numbers": account_data["mediaHashtagNumbers"],
        # "media_like_numbers": account_data["mediaLikeNumbers"],
        # "mediaUpload_times": account_data["mediaUploadTimes"],
        # "automated_behaviour": account_data["automatedBehaviour"]
    }
