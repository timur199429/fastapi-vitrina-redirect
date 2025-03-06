from sqlmodel import SQLModel, Field
import datetime as dt
import pytz

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

class OneprofitClick(SQLModel, table=True):
    __tablename__ = 'oneprofit_click'

    id: int = Field(primary_key=True)
    user_agent: str
    user_ip: str
    news_hash: str
    flow_id: str
    source_site_id: str | None
    source_teaser_id: str | None
    source_click_id: str | None
    source_campaign_id: str | None
    source_name: str | None
    source_cpc: str | None
    datetime: dt.datetime = Field(default=dt.datetime.now(pytz.timezone("Europe/Moscow")))
