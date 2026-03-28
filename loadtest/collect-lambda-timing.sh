#!/bin/bash
# Collects server-side Lambda timing via aws lambda invoke (bypasses Function URL auth).
# Runs N sequential invocations per function and prints Duration from CloudWatch REPORT lines.
set -euo pipefail

N=${1:-20}  # number of invocations, default 20
PAYLOAD=$(python3 -c "import json; q=json.load(open('loadtest/query.json')); print(json.dumps({'body': json.dumps(q)}))")
OUTFILE="results/lambda-invoke-timing.txt"
mkdir -p results

echo "=== Lambda server-side timing ($N invocations each) ===" | tee "$OUTFILE"
echo "Collecting at $(date)" | tee -a "$OUTFILE"
echo "" | tee -a "$OUTFILE"

for FUNC in lsc-knn-zip lsc-knn-container; do
    echo "--- $FUNC ---" | tee -a "$OUTFILE"
    DURATIONS=()
    for i in $(seq 1 "$N"); do
        REPORT=$(aws lambda invoke \
            --function-name "$FUNC" \
            --cli-binary-format raw-in-base64-out \
            --payload "$PAYLOAD" \
            --log-type Tail \
            --query 'LogResult' --output text \
            /tmp/lambda-out.json | base64 -d 2>/dev/null | grep "^REPORT" || true)

        if [ -n "$REPORT" ]; then
            echo "  [$i] $REPORT" | tee -a "$OUTFILE"
            DUR=$(echo "$REPORT" | grep -oE 'Duration: [0-9.]+' | head -1 | awk '{print $2}')
            DURATIONS+=("$DUR")
        else
            echo "  [$i] (no REPORT line)" | tee -a "$OUTFILE"
        fi
        sleep 0.5
    done

    # Compute average duration
    if [ ${#DURATIONS[@]} -gt 0 ]; then
        AVG=$(python3 -c "
vals = [$(IFS=,; echo "${DURATIONS[*]}")]
print(f'  avg={sum(vals)/len(vals):.1f}ms  min={min(vals):.1f}ms  max={max(vals):.1f}ms  n={len(vals)}')
")
        echo "$AVG" | tee -a "$OUTFILE"
    fi
    echo "" | tee -a "$OUTFILE"
done

echo "=== Done. Results saved to $OUTFILE ===" | tee -a "$OUTFILE"
