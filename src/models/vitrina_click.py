from sqlmodel import SQLModel, Field
import datetime as dt
import pytz


    

class OneprofitClick(SQLModel, table=True):
    __tablename__ = 'oneprofit_click'

    id: int = Field(primary_key=True)
    user_agent: str | None
    user_ip: str | None
    country_code: str | None
    city: str | None
    region: str | None
    news_hash: str | None
    flow_id: str | None
    site_id: str | None
    teaser_id: str | None
    click_id: str | None
    campaign_id: str | None
    source_name: str | None
    source_cpc: str | None
    block_id: str | None
    device_type: str | None
    datetime: dt.datetime = Field(default=dt.datetime.now(pytz.timezone("Europe/Moscow")))
