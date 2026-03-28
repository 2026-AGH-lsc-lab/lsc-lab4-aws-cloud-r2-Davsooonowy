#!/bin/bash
set -euo pipefail
OUTFILE="$(dirname "$0")/../results/assignment-1-endpoints.txt"
mkdir -p "$(dirname "$OUTFILE")"

PAYLOAD=$(python3 -c "import json; q=json.load(open('loadtest/query.json')); print(json.dumps({'body': json.dumps(q)}))")

echo "=== Lambda Zip ===" | tee "$OUTFILE"
aws lambda invoke \
    --function-name lsc-knn-zip \
    --cli-binary-format raw-in-base64-out \
    --payload "$PAYLOAD" \
    /tmp/out.json --output text | tee -a "$OUTFILE"
cat /tmp/out.json | tee -a "$OUTFILE"
echo | tee -a "$OUTFILE"

echo "=== Lambda Container ===" | tee -a "$OUTFILE"
aws lambda invoke \
    --function-name lsc-knn-container \
    --cli-binary-format raw-in-base64-out \
    --payload "$PAYLOAD" \
    /tmp/out.json --output text | tee -a "$OUTFILE"
cat /tmp/out.json | tee -a "$OUTFILE"
echo | tee -a "$OUTFILE"

echo "=== Fargate ===" | tee -a "$OUTFILE"
curl -s -X POST -H "Content-Type: application/json" \
    -d @loadtest/query.json \
    http://lsc-knn-alb-275240368.us-east-1.elb.amazonaws.com/search | tee -a "$OUTFILE"
echo | tee -a "$OUTFILE"

echo "=== EC2 ===" | tee -a "$OUTFILE"
curl -s -X POST -H "Content-Type: application/json" \
    -d @loadtest/query.json \
    http://3.236.242.105:8080/search | tee -a "$OUTFILE"
echo | tee -a "$OUTFILE"

echo "=== Done. Results saved to $OUTFILE ===" | tee -a "$OUTFILE"
