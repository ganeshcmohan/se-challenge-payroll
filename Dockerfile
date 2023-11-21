FROM python:3.9

COPY requirements.txt /src/requirements.txt
WORKDIR /src/

RUN pip install -r requirements.txt
COPY . /src
EXPOSE 5000
RUN chmod +x /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]