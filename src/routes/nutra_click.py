import os
import httpx
import requests
from sqlmodel import Session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from src.models import NutraClick
from src.db import get_session

nutra_router = APIRouter()




# Serve the index.html for each landing page
@nutra_router.get("/{hypert}/{landing_name}/")
async def serve_landing(hypert: str, landing_name: str, request: Request, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    # Construct the path to the index.html file
    index_path = os.path.join("landings", hypert, landing_name, "index.html")
    user_agent_string = request.headers.get('user-agent')
    user_ip = request.headers.get('x-real-ip')
    query_params = request.query_params
    # Check if the file exists
    if os.path.exists(index_path):
        with open(index_path, 'rb') as file:
            background_tasks.add_task(add_click_to_db, session, user_agent_string, query_params, user_ip, offer_category=hypert,landing_name=landing_name)
            return HTMLResponse(content=file.read())
    
    # If the file doesn't exist, return a 404 error
    raise HTTPException(status_code=404, detail="Landing page not found")

# Serve static files (CSS, JS, images) for each landing page
@nutra_router.get("/{hypert}/{landing_name}/{file_type}/{file_name}")
async def serve_static(hypert: str, landing_name: str, file_type: str, file_name: str):
    # Construct the path to the static file
    static_path = os.path.join("landings", hypert, landing_name, file_type, file_name)

    # Check if the file exists
    if os.path.exists(static_path):
        return FileResponse(static_path)
    
    # If the file doesn't exist, return a 404 error
    raise HTTPException(status_code=404, detail="File not found")

def send_telegram_message(message: str):
    """
    Отправляет сообщение в Telegram через бота (синхронно).
    """
    url = f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}/sendMessage"
    payload = {
        "chat_id": os.getenv('TG_CHAT_ID'),
        "text": message,
    }
    response = requests.post(url, json=payload)
    return response.json()

@nutra_router.post("/submit-form/")
async def submit_form(request: Request):
    # Получаем все данные формы, включая скрытые поля
    form_data = await request.form()
    
    # Извлекаем имя и телефон
    name = form_data.get("name")
    phone = form_data.get("phone")
    
    # Формируем сообщение для Telegram
    message = f"Новый лид!\nИмя: {name}\nТелефон: {phone}"
    
    # Добавляем query-параметры (скрытые поля) в сообщение
    for key, value in form_data.items():
        if key not in ["name", "phone"]:  # Исключаем поля name и phone
            message += f"\n{key}: {value}"
    
    # Отправляем сообщение в Telegram
    telegram_response = send_telegram_message(message)
    # print("Telegram response:", telegram_response)
    
    # Редирект на страницу успеха
    return RedirectResponse(url="/success", status_code=303)

async def get_location(ip: str) -> tuple:
    try:
        url = f"https://ipinfo.io/{ip}/json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        
        country_code = data.get("country", "")
        city = data.get("city", "")
        region = data.get("region", "")
        return (country_code, city, region)
    except:
        return (None, None, None)

async def add_click_to_db(session: Session, user_agent: str, query_params: dict, user_ip: str, offer_category: str, landing_name: str):
    country_code, city, region = await get_location(user_ip)
    click = NutraClick(
        user_agent=user_agent,
        user_ip = user_ip,
        country_code = country_code,
        city = city,
        region = region,
        offer_category = offer_category,
        landing_name = landing_name,
        site_id = query_params.get('site_id'),
        teaser_id=query_params.get('teaser_id'),
        campaign_id=query_params.get('campaign_id'),
        click_id=query_params.get('click_id'),
        source_name=query_params.get('source_name'),
        source_cpc= query_params.get('source_cpc'),
        block_id=query_params.get('block_id'),
        device_type=query_params.get('device_type'),
    )
    session.add(click)
    session.commit()
    session.refresh(click)