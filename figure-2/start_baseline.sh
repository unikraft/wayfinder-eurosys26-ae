#!/bin/bash

ID="$1"

if [ -z "$ID" ]; then
  echo "Usage: $0 <experiment_id>"
  exit 1
fi

~/wayfinder/dist/wfctl --server localhost:6000 start --isol-level full --isol-split both -l 1 -r 30 -s grid "$ID"
