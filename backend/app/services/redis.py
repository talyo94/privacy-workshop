from functools import lru_cache
from loguru import logger
import redis


class RedisClient:

    def __init__(self, host: str, password: str, port: int):
        logger.debug("Initiating redis client")

        self.client = redis.Redis(
            host=host,
            port=str(port),
            password=password,
            ssl=True,
            decode_responses=True
        )

    @staticmethod
    def _get_user_key(username: str):
        return f"user.raw:{username}"

    @staticmethod
    def _get_user_score_key(username: str):
        return f"user.score:{username}"

    def store_user(self, username: str, data: dict):
        key = self._get_user_key(username)
        self.client.hmset(key, data)
        self.client.expire(key, 60 * 60 * 24)  # Data is good for 2 days

    def get_user_data(self, username: str) -> dict:
        return {k: int(v) for k, v in self.client.hgetall(self._get_user_key(username)).items()}

    def has_user_data(self, username: str) -> bool:
        return bool(self.client.exists(self._get_user_key(username)))


@lru_cache()
def get_redis(host: str, password: str, port: int):
    return RedisClient(host, password, port)
