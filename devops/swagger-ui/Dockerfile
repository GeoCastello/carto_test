FROM gcr.io/m-itg-213307/swagger-ui-base:latest

ARG WEB_PATH='swagger-ui'
ARG TITLE='API Documentation'

COPY devops/swagger-ui/nginx.conf /etc/nginx/conf.d/default.conf
RUN cp -r /swagger-ui /usr/share/nginx/html/$WEB_PATH && mkdir /usr/share/nginx/html/$WEB_PATH/spec
COPY devops/swagger /usr/share/nginx/html/$WEB_PATH/spec

RUN cd /usr/share/nginx/html/$WEB_PATH/ && \
    sed -i.bak 's#https://petstore.swagger.io/v2/swagger.json#spec/swagger.yaml#g' index.html && \
    sed -i.bak 's#<title>Swagger UI</title>#<title>'"$TITLE"'</title>#g' index.html && \
    rm index.html.bak
