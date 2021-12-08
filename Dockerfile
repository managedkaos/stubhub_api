FROM python:3.9
COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY backend.py /
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "9000"]
