FROM python:3.7-slim

EXPOSE 8000

WORKDIR /root
COPY start.sh requirements.txt manage.py /root/
COPY homepage /root/homepage
COPY musicserver /root/musicserver
RUN chmod +x start.sh
RUN pip install -r requirements.txt
ENTRYPOINT ["./start.sh"]