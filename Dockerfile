FROM python:3.9
COPY requirements.txt backend.py /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "9000"]
