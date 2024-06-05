FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y git && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y python3.8 && \
    apt-get install -y pip
RUN mkdir /home/Work && \
    cd /home/Work && \
    git clone https://github.com/EverGreen1253/hbnb_evolution_01.git
RUN pip install flask && \
    pip install gunicorn

WORKDIR /home/Work/hbnb_evolution_01

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]