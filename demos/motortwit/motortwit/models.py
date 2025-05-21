from typing import Optional, Annotated, Any
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator: Any, _field_schema: JsonSchemaValue) -> None:
        _field_schema.update(type="string")


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v


class UserCreate(UserBase):
    password2: str = Field(..., min_length=1)

    @field_validator('password2')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v


class UserInDB(UserBase):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    pw_hash: str

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=140)


class MessageInDB(MessageCreate):
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    author_id: PyObjectId
    username: str
    pub_date: str

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    ) 