from pydantic import BaseModel
from typing import Literal


class Operation(BaseModel):
    operationType: Literal["DEPOSIT", "WITHDRAW"]
    amount: float
