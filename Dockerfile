FROM python:3

WORKDIR /usr/src/app

COPY setup.py /setup.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./MarkdownToConfluence /MarkdownToConfluence
RUN pip install -e .

RUN chmod +x /MarkdownToConfluence/convert_all.sh
RUN chmod +x /MarkdownToConfluence/convert.sh
RUN chmod +x /MarkdownToConfluence/entrypoint.sh

ENTRYPOINT [ "bash", "/MarkdownToConfluence/entrypoint.sh" ]