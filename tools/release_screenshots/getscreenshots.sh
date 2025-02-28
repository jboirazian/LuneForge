#/bin/bash

CMD="webscreenshot/webscreenshot.py -r chrome -t 60 -q 100 --window-size '1920,1080'"
BASE_URL="http://127.0.0.1:5000"

# List of paths to append to the base URL
URLS=(
    ""
    "/builds"
    "/docs"
    "/render?model_uuid=0c7843ad-d284-4151-a77f-782127ef152e"
)

# Loop through the URLs and run the command
for path in "${URLS[@]}"
do
    python3 $CMD "$BASE_URL$path"
done