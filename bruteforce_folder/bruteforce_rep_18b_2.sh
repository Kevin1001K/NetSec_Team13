#!/bin/bash

# Session cookie (replace if needed)
SESSION_ID="b8cc3976-4f90-45d2-adc1-bbae5c86e86e"

START=1500.0
END=1580.0
STEP=0.1

value=$START

while [ "$(awk "BEGIN {print ($value <= $END)}")" -eq 1 ]; do
  # Format to 1 decimal place
  formatted_value=$(printf "%.1f" "$value")
  filename="response_${formatted_value}.html"

  echo "Sending request with rep18b=$formatted_value -> Saving to $filename"

  curl 'https://www-lab.cn.tuwien.ac.at/ns-tuwel/validation/10' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
    -H 'Accept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' \
    -H 'Cache-Control: max-age=0' \
    -H 'Connection: keep-alive' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -b "session=${SESSION_ID}" \
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
    --data-raw "rep18b=${formatted_value}&validate=validate" \
    -o "$filename"

  echo "Saved response to $filename"
  echo "---"

  # Increment value using awk
  value=$(awk "BEGIN {printf \"%.1f\", $value + $STEP}")
done
