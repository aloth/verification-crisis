#!/bin/sh
# Fetch the two open files this check reads, from the Harvard Dataverse deposit
# doi:10.7910/DVN/BXO2QA (CC0 1.0). Numeric file ids are stable for version 1.0.
set -e
cd "$(dirname "$0")/data"
curl -sSL -o survey_responses_deidentified.tab \
  "https://dataverse.harvard.edu/api/access/datafile/14092357"
curl -sSL -o table_item_means_sd.tab \
  "https://dataverse.harvard.edu/api/access/datafile/14092361"
echo "Fetched into $(pwd)"
