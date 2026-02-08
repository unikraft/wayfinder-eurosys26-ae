#!/bin/bash

ID="$1"

if [ -z "$ID" ]; then
  echo "Usage: $0 <experiment_id> [output_file] (default: results.csv)"
  exit 1
fi

OUTPUT="$2"

if [ -z "$OUTPUT" ]; then
  OUTPUT="results.csv"
fi

export PGPASSWORD="wayfinder"

psql -h localhost -U wayfinder -d wayfinder -p 5432 <<EOF
\copy (select permutation_id,value_float from results inner join (select id from permutations where job_id=$ID) as perm on perm.id=results.permutation_id order by value_float desc) to '$OUTPUT' with csv header;
EOF
