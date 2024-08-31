#!/bin/bash

# Infinite loop
while true; do
    echo "Running..."
    python3 camera.py
    python3 Base64.py captured_image.jpg
    python3 execute_comman.py captured_image.jpg_curl_command.txt
    sleep 1
done
