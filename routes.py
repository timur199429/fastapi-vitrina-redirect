import logging
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

    # Читаем домен из файла
    with open('domain.txt', 'r') as file:
        domain = file.read().strip()

    # Получаем query-параметры из запроса
    query_params = request.query_params
    # utm_campaign=76406&utm_content=00f9eb05-6333-4b6b-932a-130f97a420b7&utm_source=[SID]&utm_medium=2329&sid6=[TID]&sid7=[CAMPAIGN]&subid3=[CPCP]&subid4=[CLICK_ID]&subid5=adprofex&is_visitor=1&adp_click=[CLICK_ID]
    # Формируем URL для редиректа
    url = f'https://{domain}/preview/new?'
    if query_params:
        url += '&'.join([f'{key}={value}' for key, value in query_params.items()])

    # Добавляем задачу в фоновые задачи
    background_tasks.add_task(add_click_to_db, session, user_agent_string, dict(query_params), request=request)

    # # Выполняем редирект
    return RedirectResponse(url=url, status_code=302)

async def add_click_to_db(session: Session, user_agent: str, query_params: dict, request: Request):
    client_host = request.headers.get("x-forwarded-for")
    if client_host:
        print(client_host)
        user_ip = client_host.split(",")[0]  # Берем первый IP из цепочки
    else:
        user_ip = request.client.host
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
async def clickback(
    amount: str | None = None,
    stream: str | None = None,
    subid1: str | None = None,
    subid2: str | None = None,
    subid3: str | None = None,
    subid4: str | None = None,
    subid5: str | None = None,
    created_at: str | None = None,
    order_id: str | None = None,
    session: Session = Depends(get_session)
):
    # Очищаем пробелы и преобразуем пустые строки в None
    subid3 = subid3.strip() if subid3 else None
    subid4 = subid4.strip() if subid4 else None
    subid5 = subid5.strip() if subid5 else None

    # Если после очистки строка пустая, преобразуем в None
    subid3 = subid3 if subid3 else None
    subid4 = subid4 if subid4 else None
    subid5 = subid5 if subid5 else None

    # Логируем параметры для отладки
    logging.info(f"Received clickback request with parameters: amount={amount}, stream={stream}, subid1={subid1}, subid2={subid2}, subid3={subid3}, subid4={subid4}, subid5={subid5}, created_at={created_at}, order_id={order_id}")

    # Создаем объект и сохраняем в базу данных
    click = OneprofitClickback(
        amount=amount,
        stream=stream,
        subid1=subid1,
        subid2=subid2,
        subid3=subid3,
        subid4=subid4,
        subid5=subid5,
        created_at=created_at,
        order_id=order_id
    )
    session.add(click)
    session.commit()
    session.refresh(click)
    if subid5 == 'adprofex':
        requests.get(f'https://postback.ads2.bid/api/postback/?tracker_id=3&event_id=1751&click_id={subid4}&cpa={amount}&status=confirmed&goal_category_id=1&user_id=215')

    return {'message': 'ok'}