from pydantic import BaseModel, Field


class CloudSwitchRequest(BaseModel):
    target_cloud: str = Field(
        ...,
        description="Cloud destino. Valores permitidos: aws o azure.",
        examples=["azure"],
    )


class CloudSwitchResponse(BaseModel):
    previous_cloud: str
    active_cloud: str
    status: str
    message: str