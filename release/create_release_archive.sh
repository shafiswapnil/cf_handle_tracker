#!/bin/bash

# Set version
VERSION="1.1.0"
ARCHIVE_NAME="codeforces_rank_tracker_v${VERSION}.zip"

# Create a list of files to include
FILES=(
    "*.py"
    "*.txt"
    "*.md"
    ".env.example"
    "LICENSE"
    "requirements.txt"
)

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/codeforces_rank_tracker_v${VERSION}"

# Copy files to the temporary directory
for pattern in "${FILES[@]}"; do
    find . -maxdepth 1 -name "$pattern" -type f -not -path "*/\.*" | xargs -I{} cp {} "$TEMP_DIR/codeforces_rank_tracker_v${VERSION}/"
done

# Create the archive
(cd "$TEMP_DIR" && zip -r "$ARCHIVE_NAME" "codeforces_rank_tracker_v${VERSION}")
mv "$TEMP_DIR/$ARCHIVE_NAME" .

# Clean up
rm -rf "$TEMP_DIR"

echo "Created release archive: $ARCHIVE_NAME" 