FROM python:alpine3.7
COPY . /app
COPY templates /app/templates
COPY static /app/static
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

