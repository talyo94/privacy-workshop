from os import access
from services.bot_detection import get_bot_detection_service
from services.instagram import get_instagram_service
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.settings import Settings, get_settings
from internal.models import ScoreUserRes, ScoreUsersReq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def root():
    return {"message": "OK"}


# @app.get("/info")
# async def info(settings: Settings = Depends(get_settings)):
#     return {
#         "app_name": settings.app_name,
#         "instagram_username": settings.instagram_account_username,
#         "instagram_password": settings.instagram_account_password,
#     }


@app.post("/score")
async def asses_users(users: ScoreUsersReq):
    print(users)
    return {"div": "div"}


@app.get("/{username}/score")
async def user_score(username: str):
    # insta = get_instagram_service()
    bot = get_bot_detection_service()

    # print(service.get_data_by_username(username))
    return {"item_id": username, "is_fake": bot.asses_is_fake()}


@app.get("/{username}/info")
async def user_info(username: str):
    service = get_instagram_service()
    user = service.get_data_by_username(username)

    if not user:
        return {"message": "fuck"}
    account_data = user.dict()
    return {"user_media_count": account_data["media_count"],
            "user_follower_count": account_data["follower_count"],
            "user_following_count": account_data["following_count"],
            # "user_has_highlight_reels": account_data["userHasHighlighReels"],
            "user_has_external_url": bool(account_data["external_url"]),
            # "user_tags_count": account_data["userTagsCount"],
            "follower_following_ratio":  account_data["follower_count"]/max(1, account_data["following_count"]),
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
