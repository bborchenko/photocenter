FROM python:3.8-alpine3.14
ENV PATH="/scripts:${PATH}"

COPY ./docker_files .

RUN apk add --update --no-cache libpq libstdc++ \
 && apk add --update --no-cache --virtual .tmp g++ postgresql-dev linux-headers \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .tmp

RUN rm /requirements.txt \
 && chmod +x /scripts/*
 
COPY ./code_files .

RUN adduser -D user
RUN chown -R user:user /core
RUN chown -R user:user /logic
USER user

CMD ["entrypoint.sh"]
