#!/bin/bash
aws dynamodb create-table \
    --cli-input-json file://dynamodb-table-config.json \
    --endpoint-url http://localhost:8000 || echo "All good! table is likely already there."

for i in $(seq 100 110)
do
    echo "#####################"
    echo "## Create item ${i}"
    echo "#####################"
    curl --location --request POST "http://127.0.0.1:9000/event/${i}" && echo
    echo "#####################"
    echo "## Read item ${i}"
    echo "#####################"
    curl --location "http://127.0.0.1:9000/event/${i}" && echo
done
