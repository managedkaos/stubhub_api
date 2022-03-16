FROM python:3.9
ARG TARGET
ENV TARGET_NAME=${TARGET}
COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN echo ${TARGET}
EXPOSE 9000
COPY . /
CMD uvicorn ${TARGET_NAME}:app --host=0.0.0.0 --port=9000 --reload --reload-include=static --reload-include=templates
