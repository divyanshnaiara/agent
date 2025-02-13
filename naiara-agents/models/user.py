from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Provider:
    provider: str
    uid: str
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    password: Optional[str] = None


@dataclass
class User:
    id: str
    email: str
    language: str
    nickname: Optional[str] = None
    providers: List[Provider] = field(default_factory=list)
    phoneNumber: Optional[str] = None
    fullName: Optional[str] = None
    imageUrl: Optional[str] = None
    threadIds: List[str] = field(default_factory=list)
    platform: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        providers = [Provider(**p) for p in data.get("providers", [])]
        return cls(
            id=data["id"],
            email=data["email"],
            language=data.get("language", "en"),
            nickname=data.get("nickname"),
            providers=providers,
            phoneNumber=data.get("phoneNumber"),
            fullName=data.get("fullName"),
            imageUrl=data.get("imageUrl"),
            threadIds=data.get("threadIds", []),
            platform=data.get("platform"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
        )