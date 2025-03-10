#!/bin/bash

# Create a release archive for Codeforces Rank Tracker
VERSION="v1.0.0"
ARCHIVE_NAME="codeforces_rank_tracker_${VERSION}.zip"

echo "Creating release archive: ${ARCHIVE_NAME}"

# Create a temporary directory for the release files
mkdir -p release_tmp

# Copy all necessary files to the temporary directory
cp -v cf_tracker.py validate_handles.py add_handles.py export_csv.py release_tmp/
cp -v requirements.txt .env.example README.md LICENSE RELEASE_NOTES.md release_tmp/
cp -v handles.txt release_tmp/

# Create the ZIP archive
cd release_tmp
zip -r "../${ARCHIVE_NAME}" ./*
cd ..

# Clean up
rm -rf release_tmp

echo "Release archive created: ${ARCHIVE_NAME}"
echo "You can now upload this archive to your GitHub release." 