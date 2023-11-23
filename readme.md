## Installation
```shell
python -m venv venv
pip install -r requirements.txt
```

## Running
```shell
.\venv\scripts\activate
uvicorn sever:app --reload
```

After that visit http://127.0.0.1:8000/api/{ENDPOINT_HERE}
