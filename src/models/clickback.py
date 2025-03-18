from sqlmodel import SQLModel, Field

class OneprofitClickback(SQLModel, table=True):
    __tablename__ = 'oneprofit_clickback'
    id: int = Field(default=None, primary_key=True)
    amount: str | None
    stream: str | None
    subid1: str | None
    subid2: str | None
    subid3: str | None
    subid4: str | None
    subid5: str | None
    created_at: str | None
    order_id: str | None