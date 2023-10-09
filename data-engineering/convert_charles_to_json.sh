#!/bin/bash
# Tim H 2023

# Convert a single Charles proxy traffic file to HAR traffic file
# https://www.charlesproxy.com/
# https://jqplay.org
# https://docs.proxyman.io/advanced-features/charles-proxy-converter
# https://www.charlesproxy.com/documentation/tools/command-line-tools/
# https://portswigger.net/bappstore/67c8a830b8de492b91f41b4eac5ab021

# Pre-reqs
# brew install --cask charles postman

# retest: 

# more ssl stuff: \u0000\u0000\u0000\u0003\u0000\u00
# and look out for non-http sockets, "wss://"
# $.log.entries.[14].request.headers.[5].value has "wss://"
# $.log.entries.[14].request.headers.[2].value has "websocket"

set -e

# BASE_PATH="$1"
BASE_PATH="/Volumes/tim_carrie_shared/data_sets/charles_proxy_mobile_traffic/"

cd "$BASE_PATH" || exit 1

while IFS= read -r -d '' filename
do    
    CHARLES_RECORDING_TO_CONVERT="$filename"
    OUTPUT_FILE_HAR=${CHARLES_RECORDING_TO_CONVERT%.chlsj}.har
    OUTPUT_FILE_JSON=${CHARLES_RECORDING_TO_CONVERT%.chlsj}.json
    INPUT_FILE_SANITIZED=${CHARLES_RECORDING_TO_CONVERT%.chlsj}_sanitized.chlsj

    if [[ -f "$OUTPUT_FILE_JSON" ]] || [[ -f "$INPUT_FILE_SANITIZED" ]]; then
        # echo "Output file already converted. Skipping."
        continue
    fi

    chmod -wx "$CHARLES_RECORDING_TO_CONVERT"

    # check to see if the file has encrypted data, Postman won't be able to
    # import it.
    if grep -q "SSL Proxying not enabled for this host" "$CHARLES_RECORDING_TO_CONVERT" ; then
        # echo "Encrypted traffic detected, removing it..."
        
        # jq '.[10].notes' test.json
        
        OUTPUT_FILE_HAR=${INPUT_FILE_SANITIZED%.chlsj}.har
        OUTPUT_FILE_JSON=${INPUT_FILE_SANITIZED%.chlsj}.json

        jq 'del(.[] | select(.notes == "SSL Proxying not enabled for this host: enable in Proxy Settings, SSL locations") )' "$CHARLES_RECORDING_TO_CONVERT" > "$INPUT_FILE_SANITIZED"

        CHARLES_RECORDING_TO_CONVERT="$INPUT_FILE_SANITIZED"
    fi

    # echo "Converting $CHARLES_RECORDING_TO_CONVERT to HAR..."
    /Applications/Charles.app/Contents/MacOS/Charles convert "$CHARLES_RECORDING_TO_CONVERT" "$OUTPUT_FILE_HAR"

    # for some reason you have to Lint it first, then JQ it before Postman will
    # import it?
    jsonlint "$OUTPUT_FILE_HAR" | jq .  > "$OUTPUT_FILE_JSON"

    echo "$OUTPUT_FILE_JSON"

done < <(find . -type f -name '*.chlsj' ! -name '*_sanitized*' -print0)

echo "convert_charles_to_json.sh finished successfully"
