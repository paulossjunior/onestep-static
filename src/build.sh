#!/bin/bash
# Build script for OneStep documentation
# This script runs all necessary data processing and builds the documentation

set -e  # Exit on error

echo "========================================"
echo "OneStep Documentation Build"
echo "========================================"
echo ""

# Step 1: Process scholarships
echo "Step 1: Processing scholarship data..."
python3 scripts/process_scholarships.py
echo ""

# Step 2: Analyze partnerships
echo "Step 2: Analyzing partnerships and external collaborations..."
python3 scripts/analyze_partnerships.py
echo ""

# Step 3: Build documentation (if using mkdocs)
if [ -f "onestep-static/mkdocs.yml" ]; then
    echo "Step 3: Building MkDocs documentation..."
    cd onestep-static
    mkdocs build
    cd ..
    echo ""
fi

echo "========================================"
echo "Build Complete!"
echo "========================================"
