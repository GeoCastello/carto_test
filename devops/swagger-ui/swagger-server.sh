#!/bin/bash

echo "Running Swagger at http://localhost:9001..."
docker run -p 9001:8080 \
    -e SWAGGER_JSON=/mnt/swagger/swagger-template.yaml \
    -v $(pwd)/devops/swagger/:/mnt/swagger \
    swaggerapi/swagger-ui \
    /bin/sh -c "ln -s /mnt/swagger/models /usr/share/nginx/html/models && /usr/share/nginx/run.sh"
