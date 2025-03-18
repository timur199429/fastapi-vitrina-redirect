import atexit
import requests
from urllib.parse import urlparse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


def get_domain(domain='red.skipnews.space'):
    url = 'https://' + domain + '?utm_campaign=999999&utm_content=56814b1d-40cf-40e7-8f49-d35685b2889e'
    try:
        response = requests.get(url, allow_redirects=True)
        parsed_url = urlparse(response.url)
        with open('src/domain.txt', 'w') as file:
            file.write(parsed_url.netloc)
        print('Domain updated')
    except requests.RequestException as e:
        print(f"Error processing URL: {e}")
        return None



def init_scheduler_domain(minutes:int=30):
    """Инициализация планировщика"""
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Добавляем задачу в планировщик
    scheduler.add_job(
        func=get_domain,  # Функция, которую нужно выполнять
        trigger=IntervalTrigger(minutes=minutes),  # Интервал выполнения (каждые 30 минут)
        id="get_domain_job",  # Идентификатор задачи
        name="Update domain every 30 minutes",  # Имя задачи
        replace_existing=True,  # Заменить существующую задачу, если она уже есть
    )

    # Остановка планировщика при завершении приложения
    atexit.register(lambda: scheduler.shutdown())