FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install eventlet
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

