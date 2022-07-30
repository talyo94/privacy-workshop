from functools import lru_cache
from loguru import logger
import pickle
import pandas as pd

from typing import List


class BotDetection:

    def __init__(self):
        logger.debug("Initiating Bot detection ML")

        logger.debug("Loading pre-trained model")
        self.model = pickle.load(
            open(
                "../model_training/trained_models/RandomForestClassifier_finalized_model.sav",
                "rb",
            )
        )

    @staticmethod
    def format_instagram_response(data):
        return {
            "userFollowerCount": data["follower_count"],
            "userFollowingCount": data["following_count"],
            "userBiographyLength": len(data["biography"]),
            "userMediaCount": data["media_count"],
            "userHasProfilPic": int(data["profile_pic_url"] is not None),
            "userIsPrivate": int(data["is_private"]),
            "usernameDigitCount": sum(c.isdigit() for c in data["username"]),
            "usernameLength": len(data["username"])
        }

    def score_users(self, datoms: List[dict]):
        v = pd.DataFrame([pd.Series(data, index=[
            "userFollowerCount",
            "userFollowingCount",
            "userBiographyLength",
            "userMediaCount",
            "userHasProfilPic",
            "userIsPrivate",
            "usernameDigitCount",
            "usernameLength",
        ]) for data in datoms])
        return self.model.predict_proba(v)


@lru_cache()
def get_bot_detection_service():
    return BotDetection()
