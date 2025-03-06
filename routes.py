import requests
from sqlmodel import Session
from models import OneprofitClick, OneprofitClickback
from fastapi import BackgroundTasks, Depends, Request, APIRouter
from fastapi.responses import RedirectResponse
from db import get_session


router = APIRouter()

@router.get('/redirect-oneprofit')
async def redirect_oneprofit(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    # Получаем User-Agent из заголовков запроса
    user_agent_string = request.headers.get('user-agent')
    try:
        user_ip = request.client.host  # Если заголовка нет, используем client.host
    except:
        user_ip = '0.0.0.0'

    # Читаем домен из файла
    with open('domain.txt', 'r') as file:
        domain = file.read().strip()

    # Получаем query-параметры из запроса
    query_params = request.query_params

    # Формируем URL для редиректа
    url = f'https://{domain}/preview/new'
    if query_params:
        url += '?is_visitor=1' + '&'.join([f'{key}={value}' for key, value in query_params.items()])

    # Добавляем задачу в фоновые задачи
    background_tasks.add_task(add_click_to_db, session, user_agent_string, dict(query_params), user_ip)

    # # Выполняем редирект
    return RedirectResponse(url=url, status_code=302)

async def add_click_to_db(session: Session, user_agent: str, query_params: dict, user_ip: str):
    click = OneprofitClick(
        user_agent=user_agent,
        user_ip = user_ip,
        news_hash=query_params.get('utm_content'),
        flow_id=query_params.get('utm_campaign'),
        source_site_id=query_params.get('utm_source'),
        source_teaser_id=query_params.get('sid6'),
        source_click_id=query_params.get('subid4'),
        source_campaign_id=query_params.get('sid7'),
        source_name=query_params.get('subid5'),
        source_cpc=query_params.get('subid3'),
    )
    session.add(click)
    session.commit()
    session.refresh(click)

@router.get('/clickback')
async def clickback(amount: str = None, 
                    stream: str = None, 
                    subid1: str = None, 
                    subid2: str = None,
                    subid3: str = None, 
                    subid4: str = None,
                    subid5: str = None, 
                    created_at: str = None, 
                    order_id: str = None, session: Session = Depends(get_session)):
    click = OneprofitClickback(amount=amount, stream=stream, subid1=subid1, subid2=subid2, subid3=subid3, subid4=subid4, subid5=subid5, created_at=created_at, order_id=order_id)
    session.add(click)
    session.commit()
    session.refresh(click)
    # if subid5 == 'adprofex' & amount == float(amount) > 0:
    #     requests.get(f'https://postback.ads2.bid/api/postback/?tracker_id=3&event_id=1751&click_id={subid4}&cpa={cost}&status={status}&goal_category_id=1&user_id=215')
    return {'message':'ok'}