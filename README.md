# parse_app

1) git clone https://github.com/alisher1989/parse_app.git
2) cd parse_app/
3) virtualenv -p python3 venv
4) source venv/bin/activate
5) pip install --upgrade pip
6) pip install -r req.txt
7) uvicorn main:app --reload

На главной странице выводятся данные с сайта, а на API view url ( http://localhost:8000/page_view/) выводятся данные с базы данных
