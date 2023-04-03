# pythonのバージョン指定
FROM python:3

# Linuxに必要なソフトインストール
RUN apt-get update
RUN apt-get -y install tree locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

# 日本語対応、日本のタイムゾーンへ変更
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt