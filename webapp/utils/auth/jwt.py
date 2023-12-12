import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, Any, Dict

from fastapi import Header, HTTPException
from jose import JWTError, jwt
from starlette import status

from conf.config import settings

JwtTokenT = Dict[str, Any]


@dataclass
class JwtAuth:
    secret: str

    def create_token(self, user_id: int) -> str:
        access_token = {
            'uid': uuid.uuid4().hex,
            'exp': datetime.utcnow() + timedelta(seconds=60),
            'user_id': user_id,
        }
        return jwt.encode(access_token, self.secret)

    def validate_token(self, authorization: Annotated[str, Header()]) -> JwtTokenT:
        _, token = authorization.split()

        try:
            return jwt.decode(token, self.secret)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)