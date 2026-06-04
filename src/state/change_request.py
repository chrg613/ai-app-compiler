from pydantic import BaseModel


class ChangeRequest(BaseModel):

    action: str

    target: str

    value: str