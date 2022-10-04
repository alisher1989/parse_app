from typing import Union
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Depends
import requests
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

SessionLocal.configure(bind=engine)
session = SessionLocal()


templates = Jinja2Templates(directory="templates")

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


@app.get("/")
def read_index(request: Request, q: Union[int, None] = None):
    if q:
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{q}/c37l1700273".format(q=q)
    else:
        url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('div', class_='search-item')
    data = []
    for i in lists:
        data.append({"img": i.find('img')['src'], 'price': " ".join(i.find('div', class_='price').getText().split()),
                     'date': i.find('span', class_='date-posted').text},)
    context = {'request': request, 'data': data, 'url': url}
    for i in data:
        get_or_create(session, models.Record, img=i['img'], price=i['price'], date=i['date'])
    return templates.TemplateResponse('index.html', context=context)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/page_view/')
def page_view(request: Request, page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    start = (page_num - 1) * page_size
    end = start + page_size
    records = db.query(models.Record).all()
    response = {
        'total': len(records),
        'count': page_size,
        'pagination': {},
        'data': records[start:end],
    }

    if end >= len(records):
        response['pagination']['next'] = None

        if page_num > 1:
            response['pagination']['previous'] = f"{request.base_url}page_view/?page_num={page_num-1}&page_size={page_size}"
        else:
            response['pagination']['previous'] = None
    else:
        if page_num > 1:
            response['pagination']['previous'] = f"{request.base_url}page_view/?page_num={page_num-1}&page_size={page_size}"
        else:
            response['pagination']['previous'] = None
        response['pagination']['next'] = f"{request.base_url}page_view/?page_num={page_num+1}&page_size={page_size}"
    return response



