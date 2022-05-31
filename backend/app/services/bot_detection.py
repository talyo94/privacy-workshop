from functools import lru_cache
from loguru import logger
import pickle
import pandas as pd


class BotDetection:

    def __init__(self):
        logger.debug("Initiating Bot detection ML")

        logger.debug("Loading pre-trained model")
        self.model = pickle.load(
            open(
                "../model_training/trained_models/DecisionTreeClassifier_finalized_model.sav",
                "rb",
            )
        )

    def asses_is_fake(self):
        v = pd.DataFrame([pd.Series(
            {
                "userFollowerCount": 433,
                "userFollowingCount": 238,
                "userBiographyLength": 0,
                "userHasProfilPic": True,
                "userMediaCount": 33,
                "userIsPrivate": True,
                "usernameDigitCount": 0,
                "usernameLength": 10,
            }
        )])
        print(self.model.predict_proba(v))
        return bool(self.model.predict(v)[0])


@lru_cache()
def get_bot_detection_service():
    return BotDetection()
