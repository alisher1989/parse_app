# parse_app

git clone https://github.com/alisher1989/parse_app.git
cd parse_app/
virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r req.txt
uvicorn main:app --reload
