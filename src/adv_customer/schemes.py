from pydantic import BaseModel, Field

class ResponseFormatter(BaseModel):
    message: str = Field(description="El contenido del mensaje")
    closed: bool = Field(description="Determina si la conversación ha finalizado")
    
class CustomerAttributes(BaseModel):
    attributes: list[str] = Field(description="Atributos de información pertenecientes al cliente")