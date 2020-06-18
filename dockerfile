FROM python:3.7-slim

EXPOSE 8000

WORKDIR /root
RUN apt-get update && apt-get install ffmpeg -y && mkdir temp
COPY start.sh requirements.txt manage.py /root/
RUN chmod +x start.sh
RUN pip install -r requirements.txt
COPY homepage /root/homepage
COPY musicserver /root/musicserver
ENTRYPOINT ["./start.sh"]