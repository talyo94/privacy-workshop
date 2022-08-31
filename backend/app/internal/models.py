from pydantic import BaseModel, conlist


class UserScore(BaseModel):
    username: str
    score_is_fake: float
    score_is_not_fake: float


class ScoreUsersReq(BaseModel):
    users: conlist(min_items=1, max_items=30, item_type=str)


class ScoreUserRes(BaseModel):
    users: conlist(min_items=1, item_type=UserScore)
