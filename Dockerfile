FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .

RUN chmod +x /usr/src/app/MarkdownToConfluence/convert_all.sh
RUN chmod +x /usr/src/app/MarkdownToConfluence/convert.sh
RUN chmod +x /usr/src/app/MarkdownToConfluence/entrypoint.sh

ENTRYPOINT [ "bash", "/usr/src/app/MarkdownToConfluence/entrypoint.sh" ]