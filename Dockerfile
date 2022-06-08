FROM python:3.9.5
WORKDIR /src
RUN apt update
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src
RUN cp -r media /usr/local/lib/python3.9/site-packages/aiogram_dialog/widgets
RUN rm -r media
CMD ["python3.9", "-m", "bot"]
