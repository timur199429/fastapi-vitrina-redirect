from fastapi import FastAPI
from contextlib import asynccontextmanager
from src import routes
from src.funcs import get_domain, init_scheduler_domain


@asynccontextmanager
async def lifespan(app: FastAPI):    
    print("Server is starting...")
    # db_init()
    get_domain()
    init_scheduler_domain() # каждые 30 минут проверяем домен редиректа
    yield
    print("server is stopping")


app = FastAPI(lifespan=lifespan)
app.include_router(routes.main_router)


@app.get("/")
def read_root():
    return {"message": "ok"}
