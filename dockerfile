FROM python:3.7-slim

WORKDIR /root
COPY . /root
RUN chmod +x start.sh
RUN pip install -r requirements.txt
ENTRYPOINT ["./start.sh"]