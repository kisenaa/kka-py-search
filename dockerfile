# 
FROM python:3.12

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./main.py /app/
#
COPY ./searchV2.py /app/
#
COPY ./fetch_gmap /app/fetch_gmap
# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
