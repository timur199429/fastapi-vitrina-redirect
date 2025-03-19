from sqlmodel import SQLModel, Field
import datetime as dt
import pytz


    

class OneprofitClick(SQLModel, table=True):
    __tablename__ = 'oneprofit_click'

    id: int = Field(primary_key=True)
    user_agent: str | None
    user_agent_browser: str | None
    user_agent_browser_version: str | None
    user_agent_os: str | None
    user_agent_os_version: str | None
    user_agent_device: str | None
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
    source_block_id: str | None
    source_device_type: str | None
    source_browser: str | None
    source_language: str | None
    source_platform: str | None
    source_platform_version: str | None
    source_city: str | None
    subid1: str | None
    subid2: str | None
    subid3: str | None
    subid4: str | None
    subid5: str | None
    datetime: dt.datetime = Field(sa_column_kwargs={'server_default': "CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'"})
