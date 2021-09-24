from pydantic import BaseModel


class BaseForm(BaseModel):
    name: str