# todo нужен сбор страны и города
import httpx
from sqlmodel import Session

from fastapi import BackgroundTasks, Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from src.db import get_session
from src.models import OneprofitClick


oneprofit_redirect = APIRouter()

@oneprofit_redirect.get('/redirect-oneprofit')
async def redirect_oneprofit(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    # Получаем User-Agent из заголовков запроса
    user_agent_string = request.headers.get('user-agent')
    user_ip = request.headers.get('x-real-ip')
    # print(request.headers)

    # Читаем домен из файла
    with open('src/domain.txt', 'r') as file:
        domain = file.read().strip()

    # Получаем query-параметры из запроса
    query_params = request.query_params
    news_hash=query_params.get('news_hash')
    flow_id=query_params.get('flow_id')
    site_id=query_params.get('site_id')
    teaser_id=query_params.get('teaser_id')
    click_id=query_params.get('click_id')
    campaign_id=query_params.get('campaign_id')
    source_name=query_params.get('source_name')
    source_cpc=query_params.get('source_cpc')
    # utm_campaign=76406&utm_content=00f9eb05-6333-4b6b-932a-130f97a420b7&utm_source=[SID]&utm_medium=2329&sid6=[TID]&sid7=[CAMPAIGN]&subid3=[CPCP]&subid4=[CLICK_ID]&subid5=adprofex&is_visitor=1&adp_click=[CLICK_ID]
    # Формируем URL для редиректа
    url = f'https://{domain}/preview/new?utm_campaign={flow_id}&utm_content={news_hash}&utm_source={site_id}&utm_medium=2329&sid6={teaser_id}&sid7={campaign_id}&subid3={source_cpc}&subid4={click_id}&subid5={source_name}&is_visitor=1'
    if source_name == 'adprofex':
        url += f'&adp_click={click_id}'

    # Добавляем задачу в фоновые задачи
    background_tasks.add_task(add_click_to_db, session, user_agent_string, dict(query_params), user_ip)

    # # Выполняем редирект
    return RedirectResponse(url=url, status_code=302)

async def get_location(ip: str) -> tuple:
    try:
        url = f"https://ipinfo.io/{ip}/json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        
        country_code = data.get("country", "")
        city = data.get("city", "")
        return (country_code, city)
    except:
        return (None, None)

async def add_click_to_db(session: Session, user_agent: str, query_params: dict, user_ip: str):
    country_code, city = get_location(user_ip)
    
    click = OneprofitClick(
        user_agent=user_agent,
        user_ip = user_ip,
        country_code = country_code,
        city = city,
        news_hash=query_params.get('news_hash'),
        flow_id=query_params.get('flow_id'),
        site_id=query_params.get('site_id'),
        teaser_id=query_params.get('teaser_id'),
        click_id=query_params.get('click_id'),
        campaign_id=query_params.get('campaign_id'),
        source_name=query_params.get('source_name'),
        source_cpc=query_params.get('source_cpc'),
        block_id=query_params.get('block_id'),
        device_type=query_params.get('device_type')
    )
    session.add(click)
    session.commit()
    session.refresh(click)

