#!/bin/bash

ID="$1"
PERMUTATIONS=${2:-800}
REPEATS=${3:-0}

if [ -z "$ID" ]; then
  echo "Usage: $0 <experiment_id> [permutations] [repeats]"
  exit 1
fi

~/wayfinder/dist/wfctl --server localhost:6000 start --isol-level full --isol-split both -l "$PERMUTATIONS" -r "$REPEATS" -s random "$ID"
