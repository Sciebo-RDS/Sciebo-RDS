FROM python:3.8-alpine
EXPOSE 8080

# set the base installation, requirements are not changed often
RUN apk update && apk add --no-cache --virtual .build-deps build-base g++ python3-dev libffi-dev openssl-dev git libxml2-dev libxslt-dev

WORKDIR /app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

ENV OPENAPI_MULTIPLE_FILES      "interface_port_metadata.yml;interface_port_token_storage.yml"

ADD "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle2_use_cases/interface_port_metadata.yml" ./
ADD "https://raw.githubusercontent.com/Sciebo-RDS/Sciebo-RDS/master/RDS/circle3_central_services/interface_port_token_storage.yml" ./

# now add everything else, which changes often
ADD src ./

ENTRYPOINT [ "python", "server.py" ]