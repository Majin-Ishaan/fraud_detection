from pydantic import BaseModel, Field , field_validator

class TransactionRequest(BaseModel):
    transaction_amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    transaction_hour: int = Field(..., ge=0, le=23, description="Hour of transaction (0–23)")
    customer_age: float = Field(..., ge=18, le=100, description="Customer age (18–100)")
    is_international: int = Field(..., ge=0, le=1, description="1 if international, 0 otherwise")
    past_failed_transactions: int = Field(..., ge=0, description="Past failed transactions (non-negative)")

    @field_validator("is_international")
    @classmethod
    def must_be_binary(cls,v:int)->int:
        if v not in (0,1):
            raise ValueError("is_international must be 0 or 1")
        return v
        