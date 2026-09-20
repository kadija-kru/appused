from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=10, max_length=128)

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    model_config = {"from_attributes": True}
