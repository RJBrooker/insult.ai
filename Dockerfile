FROM python:3.5

MAINTAINER Richard Brooker "richjbrooker@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \ 
	 pip install --upgrade pip 

COPY . /app
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt 

RUN git clone https://github.com/huggingface/torchMoji.git
WORKDIR /app/torchMoji
RUN pip3 install -e .

WORKDIR /app/torchMoji/model/
RUN wget https://www.dropbox.com/s/nxw5pcogyzqdgdo/insults_model_chain-thaw_1.bin?dl=0 -O insults_model_chain-thaw_1.bin
RUN python3 -c "import nltk ; nltk.download('punkt')"

EXPOSE 8000
WORKDIR /app
CMD gunicorn --reload --bind=0.0.0.0:8000 insultAI:__hug_wsgi__


