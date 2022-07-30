from functools import lru_cache
from internal.settings import get_settings
from instagrapi import Client
from loguru import logger


class InstagramService:

    def __init__(self) -> None:
        settings = get_settings()
        logger.debug("Initiating instagram client")

        cl = Client()

        cl.login(
            settings.instagram_account_username,
            settings.instagram_account_password
        )

        self.client = cl

    def get_data_by_username(self, username: str):
        # user_id = self.client.user_id_from_username(username)
        # user = self.client.user_info(user_id)
        logger.debug(f"Fetching user info for: {username}")
        user = self.client.user_info_by_username(username)
        return user.dict()


@lru_cache()
def get_instagram_service():
    return InstagramService()
