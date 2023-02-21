FROM python:3

WORKDIR /usr/src/app

RUN apt-get install jq -y
COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .

RUN chmod +x MarkdownToConfluence/convert_all.sh
RUN chmod +x MarkdownToConfluence/convert.sh
RUN chmod +x MarkdownToConfluence/entrypoint.sh

ENTRYPOINT [ "bash", "/usr/src/app/MarkdownToConfluence/entrypoint.sh" ]