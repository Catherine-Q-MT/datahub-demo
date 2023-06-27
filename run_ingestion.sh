#!/usr/bin/env bash

cd ingestion

for f in *; do
    if [ -d "$f" ]; then
        echo "$f"
        for x in $f/*.yaml; do
            datahub ingest run -c $x
        done
    fi
done