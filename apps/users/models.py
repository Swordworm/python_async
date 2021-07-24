from pydantic import BaseModel, EmailStr, validator


class CreateUserParams(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str

    @validator('name')
    def name_must_contain_space(cls, name):
        if ' ' not in name:
            raise ValueError('It must be full name.')
        return name.title()

    @validator('phone')
    def phone_alphanumeric_length(cls, phone):
        if len(phone) < 7:
            raise ValueError('Invalid phone number. Too short.')
        return phone
