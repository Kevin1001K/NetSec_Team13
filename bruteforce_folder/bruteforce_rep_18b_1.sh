#!/bin/bash

# Input file with rep18b values (one per line)
INPUT_FILE="bytes_list.txt"

# Base URL
URL='https://www-lab.cn.tuwien.ac.at/ns-tuwel/validation/10'

# Session cookie (update if needed)
SESSION_COOKIE='session=b8cc3976-4f90-45d2-adc1-bbae5c86e86e'

# Counter for output files
COUNTER=1

# Read each rep18b value from the input file
while IFS= read -r rep18b_value; do
  if [[ -z "$rep18b_value" ]]; then
    continue  # skip empty lines
  fi

  echo "Sending request for rep18b = $rep18b_value..."

  curl "$URL" \
    -X POST \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
    -H 'Accept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' \
    -H 'Cache-Control: max-age=0' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -b "$SESSION_COOKIE" \
    -H 'Origin: https://www-lab.cn.tuwien.ac.at' \
    -H 'Referer: https://www-lab.cn.tuwien.ac.at/ns-tuwel/validation/10' \
    -H 'Sec-Fetch-Dest: iframe' \
    -H 'Sec-Fetch-Mode: navigate' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-User: ?1' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' \
    -H 'sec-ch-ua: "Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'sec-ch-ua-platform: "Windows"' \
    --data-raw "rep18b=$rep18b_value&validate=validate" \
    -o "response_${COUNTER}.html"

  echo "Saved response to response_${COUNTER}.html"
  ((COUNTER++))

done < "$INPUT_FILE"

echo "All requests completed."