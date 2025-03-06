import atexit
import requests
from fastapi import FastAPI
from urllib.parse import urlparse
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


from routes import router
from db import db_init


@asynccontextmanager
async def lifespan(app: FastAPI):    
    print("Server is starting...")
    db_init()
    get_domain()
    yield
    print("server is stopping")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "ok"}


def get_domain(domain='red.skipnews.space'):
    url = 'https://' + domain + '?utm_campaign=999999&utm_content=56814b1d-40cf-40e7-8f49-d35685b2889e'
    try:
        response = requests.get(url, allow_redirects=True)
        parsed_url = urlparse(response.url)
        with open('domain.txt', 'w') as file:
            file.write(parsed_url.netloc)
        print('Domain updated')
    except requests.RequestException as e:
        print(f"Error processing URL: {e}")
        return None


# Инициализация планировщика
scheduler = BackgroundScheduler()
scheduler.start()

# Добавляем задачу в планировщик
scheduler.add_job(
    func=get_domain,  # Функция, которую нужно выполнять
    trigger=IntervalTrigger(minutes=30),  # Интервал выполнения (каждые 10 минут)
    id="get_domain_job",  # Идентификатор задачи
    name="Update domain every 10 minutes",  # Имя задачи
    replace_existing=True,  # Заменить существующую задачу, если она уже есть
)

# Остановка планировщика при завершении приложения
atexit.register(lambda: scheduler.shutdown())
    



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app)