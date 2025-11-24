#!/bin/bash

# Verification script for MkDocs build
# This script checks if the project is ready to build and deploy

set -e  # Exit on error

echo "=========================================="
echo "MkDocs Build Verification Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${GREEN}ℹ${NC} $1"
}

# Check Python version
echo "1. Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status 0 "Python found: $PYTHON_VERSION"
else
    print_status 1 "Python 3 not found"
    exit 1
fi
echo ""

# Check if requirements.txt exists
echo "2. Checking requirements.txt..."
if [ -f "requirements.txt" ]; then
    print_status 0 "requirements.txt found"
else
    print_status 1 "requirements.txt not found"
    exit 1
fi
echo ""

# Check if data directory exists
echo "3. Checking data directory..."
if [ -d "data" ]; then
    print_status 0 "data/ directory found"
    
    # Check for required data files
    DATA_FILES=("papers.json" "research_lines.json" "scholarships.json" "students.json" "supervisors.json" "partnership_analysis.json")
    
    for file in "${DATA_FILES[@]}"; do
        if [ -f "data/$file" ]; then
            print_status 0 "  - data/$file exists"
        else
            print_warning "  - data/$file not found (may cause build issues)"
        fi
    done
else
    print_status 1 "data/ directory not found"
    exit 1
fi
echo ""

# Check if onestep-static directory exists
echo "4. Checking onestep-static directory..."
if [ -d "onestep-static" ]; then
    print_status 0 "onestep-static/ directory found"
else
    print_status 1 "onestep-static/ directory not found"
    exit 1
fi
echo ""

# Check if mkdocs.yml exists
echo "5. Checking mkdocs.yml..."
if [ -f "onestep-static/mkdocs.yml" ]; then
    print_status 0 "onestep-static/mkdocs.yml found"
else
    print_status 1 "onestep-static/mkdocs.yml not found"
    exit 1
fi
echo ""

# Check if main.py exists
echo "6. Checking main.py (custom macros)..."
if [ -f "onestep-static/main.py" ]; then
    print_status 0 "onestep-static/main.py found"
else
    print_status 1 "onestep-static/main.py not found"
    exit 1
fi
echo ""

# Check if docs directory exists
echo "7. Checking docs directory..."
if [ -d "onestep-static/docs" ]; then
    print_status 0 "onestep-static/docs/ directory found"
    
    # Count markdown files
    MD_COUNT=$(find onestep-static/docs -name "*.md" | wc -l)
    print_info "  Found $MD_COUNT markdown files"
else
    print_status 1 "onestep-static/docs/ directory not found"
    exit 1
fi
echo ""

# Check if virtual environment exists
echo "8. Checking virtual environment..."
if [ -d "venv" ]; then
    print_status 0 "Virtual environment found"
    VENV_EXISTS=1
else
    print_warning "Virtual environment not found (will create one)"
    VENV_EXISTS=0
fi
echo ""

# Create virtual environment if needed
if [ $VENV_EXISTS -eq 0 ]; then
    echo "9. Creating virtual environment..."
    python3 -m venv venv
    print_status $? "Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "10. Activating virtual environment..."
source venv/bin/activate
print_status $? "Virtual environment activated"
echo ""

# Install dependencies
echo "11. Installing dependencies..."
pip install -q -r requirements.txt
print_status $? "Dependencies installed"
echo ""

# Validate JSON files
echo "12. Validating JSON files..."
JSON_VALID=1
for file in data/*.json; do
    if [ -f "$file" ]; then
        if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
            print_status 0 "  - $(basename $file) is valid JSON"
        else
            print_status 1 "  - $(basename $file) is INVALID JSON"
            JSON_VALID=0
        fi
    fi
done

if [ $JSON_VALID -eq 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Some JSON files are invalid. Please fix them before building.${NC}"
    exit 1
fi
echo ""

# Test build
echo "13. Testing MkDocs build..."
cd onestep-static
if mkdocs build --strict --verbose > /tmp/mkdocs_build.log 2>&1; then
    print_status 0 "MkDocs build successful"
    
    # Check if site directory was created
    if [ -d "site" ]; then
        SITE_SIZE=$(du -sh site | cut -f1)
        print_info "  Site directory created (size: $SITE_SIZE)"
        
        # Count generated HTML files
        HTML_COUNT=$(find site -name "*.html" | wc -l)
        print_info "  Generated $HTML_COUNT HTML files"
    fi
else
    print_status 1 "MkDocs build failed"
    echo ""
    echo "Build log:"
    cat /tmp/mkdocs_build.log
    exit 1
fi
cd ..
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}✓ All checks passed!${NC}"
echo "=========================================="
echo ""
echo "Your project is ready to build and deploy."
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Commit changes: git add . && git commit -m 'Your message'"
echo "  3. Push to GitLab: git push"
echo "  4. Check pipeline: Visit your GitLab project → CI/CD → Pipelines"
echo ""
echo "To serve locally:"
echo "  cd onestep-static && mkdocs serve"
echo ""
