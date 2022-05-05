MAINTAINER otchlan <raf.szuwalski@gmail.com>

#WORKDIR /home/ubuntu/users/root/serwer/gpt_web_pl

ADD app.py .
ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "./app.py"]
