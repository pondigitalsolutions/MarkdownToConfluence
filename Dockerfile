FROM python:3.11-alpine3.17

WORKDIR /

RUN apk add --no-cache jq bash git
COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .

RUN chmod +x MarkdownToConfluence/convert_all.sh
RUN chmod +x MarkdownToConfluence/convert.sh
RUN chmod +x MarkdownToConfluence/entrypoint.sh

ENTRYPOINT [ "bash", "/MarkdownToConfluence/entrypoint.sh" ]