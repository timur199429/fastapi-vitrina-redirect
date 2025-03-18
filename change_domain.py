import os
import requests
import psycopg2
from urllib.parse import urlparse

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_domain(domain='red.skipnews.space'):
    url = 'https://' + domain + '?utm_campaign=999999&utm_content=56814b1d-40cf-40e7-8f49-d35685b2889e'
    try:
        response = requests.get(url, allow_redirects=True)
        parsed_url = urlparse(response.url).netloc
        return parsed_url
    except requests.RequestException as e:
        print(f"Error processing URL: {e}")
        return None


category_value = 'oneprofit_domain'
domain_value = get_domain()

sql = f'''
INSERT INTO domains (category, domain)
VALUES ('{category_value}', '{domain_value}')
ON CONFLICT (category) DO UPDATE SET domain = EXCLUDED.domain;
'''

# print(sql)

with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()