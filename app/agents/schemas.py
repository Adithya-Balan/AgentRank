from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=80)
    framework: str | None = Field(default=None, max_length=80)
    endpoint: str = Field(..., min_length=1, max_length=500)
    wallet_address: str | None = Field(default=None, max_length=120)
    pricing_model: str | None = Field(default="free", max_length=80)
    price_per_call: float = Field(default=0.0, ge=0)
    capabilities: list[str] = Field(default_factory=list)


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    category: str | None = Field(default=None, max_length=80)
    framework: str | None = Field(default=None, max_length=80)
    endpoint: str | None = Field(default=None, min_length=1, max_length=500)
    wallet_address: str | None = Field(default=None, max_length=120)
    pricing_model: str | None = Field(default=None, max_length=80)
    price_per_call: float | None = Field(default=None, ge=0)
    capabilities: list[str] | None = None
    is_active: bool | None = None
    health_status: str | None = Field(default=None, max_length=40)
    trust_score: float | None = Field(default=None, ge=0, le=100)


class AgentRead(AgentBase):
    id: int
    is_active: bool
    health_status: str
    trust_score: float

    model_config = {"from_attributes": True}
