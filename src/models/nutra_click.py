import pytz
import datetime as dt
from sqlmodel import SQLModel, Field


class NutraClick(SQLModel, table=True):
    __tablename__ = 'nutra_click'
    id: int = Field(primary_key=True)
    user_agent: str | None
    user_ip: str | None
    url : str | None
    site_id : str | None
    teaser_id: str | None
    campaign_id: str | None
    click_id: str | None
    source_name: str | None
    source_cpc: str | None
    block_id: str | None
    device_type: str | None
    datetime: dt.datetime = Field(default=dt.datetime.now(pytz.timezone("Europe/Moscow")))

