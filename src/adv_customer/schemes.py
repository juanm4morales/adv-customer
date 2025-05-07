from pydantic import BaseModel, Field

class ResponseFormatter(BaseModel):
    message: str = Field(description="El contenido del mensaje")
    closed: bool = Field(description="Determina si la conversación ha finalizado")

class CustomerAttribute(BaseModel):
    attribute_name: str = Field(description="Nombre del atributo del cliente.")  # Eliminado el valor predeterminado
    is_required: bool = Field(description="Determina si el atributo es obligatorio o no.")  # Ajustada la descripción
        
class CustomerAttributes(BaseModel):
    #attributes: list[CustomerAttribute] = Field(description="Atributos de información pertenecientes al cliente")
    attributes: list[str] = Field(description="Atributos de información pertenecientes al cliente")