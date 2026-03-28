#!/bin/bash
# Endpoint URLs for load testing
# Fill in after deploying with the URLs printed by each deploy script
export LAMBDA_ZIP_URL="https://7jciym7w5cwgw6lnyyahurwwlu0hbnhv.lambda-url.us-east-1.on.aws/"        # e.g. https://<id>.lambda-url.us-east-1.on.aws
export LAMBDA_CONTAINER_URL="https://2hp2rbcoywmiy3zlqzvsbgrfjq0itdgi.lambda-url.us-east-1.on.aws/"  # e.g. https://<id>.lambda-url.us-east-1.on.aws
export FARGATE_URL="http://lsc-knn-alb-275240368.us-east-1.elb.amazonaws.com"           # e.g. http://<alb-dns>.us-east-1.elb.amazonaws.com
export EC2_URL="http://3.236.242.105:8080"               # e.g. http://<public-ip>:8080
