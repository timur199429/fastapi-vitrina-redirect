from sqlmodel import SQLModel, Field



class Domains(SQLModel, table=True):
    __tablename__ = 'domains'

    category: str = Field(primary_key=True)
    domain: str = Field(unique=True)
