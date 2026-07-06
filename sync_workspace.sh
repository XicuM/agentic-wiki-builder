#!/bin/bash

# Define the target directories
DIRS=("wiki" "sources" "user")

echo "Starting workspace synchronization..."

for DIR in "${DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        echo "Directory '$DIR' does not exist."
        read -p "Please paste the Git repository URL for '$DIR': " REPO_URL
        if [ -n "$REPO_URL" ]; then
            git clone "$REPO_URL" "$DIR"
        else
            echo "Skipping '$DIR' because no URL was provided."
        fi
    else
        echo "Directory '$DIR' exists. Pulling latest changes..."
        (cd "$DIR" && git pull)
    fi
done

echo "Synchronization complete!"
