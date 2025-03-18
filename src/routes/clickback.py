import logging
import requests
from sqlmodel import Session
from fastapi import Depends, APIRouter
from src.db import get_session
from src.models import OneprofitClickback

clickback_router = APIRouter()


@clickback_router.get('/clickback')
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