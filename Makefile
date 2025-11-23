# Makefile for OneStep Research Observatory
# ==========================================
# This Makefile provides commands to process data, build documentation,
# and deploy the research observatory website.

.PHONY: help install clean process-all process-groups process-projects process-scholarships \
        aggregate-students aggregate-supervisors analyze-partnerships analyze-networks \
        calculate-recurrence translate-docs build-docs serve-docs deploy test lint

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Directories
SRC_DIR := src
DATA_DIR := data
SOURCE_DIR := source
DOCS_DIR := onestep-static
SITE_DIR := $(DOCS_DIR)/site

# Colors for output
COLOR_RESET := \033[0m
COLOR_BOLD := \033[1m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m

# Help target
help: ## Show this help message
	@echo "$(COLOR_BOLD)OneStep Research Observatory - Makefile Commands$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Usage:$(COLOR_RESET)"
	@echo "  make [target]"
	@echo ""
	@echo "$(COLOR_BLUE)Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-25s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_BLUE)Examples:$(COLOR_RESET)"
	@echo "  make install          # Install dependencies"
	@echo "  make process-all      # Process all data"
	@echo "  make build-docs       # Build documentation"
	@echo "  make serve-docs       # Serve documentation locally"
	@echo ""

# Installation
install: ## Install Python dependencies
	@echo "$(COLOR_BOLD)Installing dependencies...$(COLOR_RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(COLOR_GREEN)✓ Dependencies installed$(COLOR_RESET)"

install-dev: install ## Install development dependencies
	@echo "$(COLOR_BOLD)Installing development dependencies...$(COLOR_RESET)"
	$(PIP) install pytest pytest-cov black flake8 mypy
	@echo "$(COLOR_GREEN)✓ Development dependencies installed$(COLOR_RESET)"

# Cleaning
clean: ## Clean generated files and caches
	@echo "$(COLOR_BOLD)Cleaning generated files...$(COLOR_RESET)"
	rm -rf $(SITE_DIR)
	rm -rf $(DOCS_DIR)/docs/data
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(COLOR_GREEN)✓ Cleaned$(COLOR_RESET)"

clean-data: ## Clean generated data files (WARNING: removes processed data)
	@echo "$(COLOR_YELLOW)⚠ This will remove all processed data files$(COLOR_RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f $(DATA_DIR)/*.json; \
		echo "$(COLOR_GREEN)✓ Data files removed$(COLOR_RESET)"; \
	else \
		echo "Cancelled"; \
	fi

# Data Processing Pipeline
process-all: process-groups process-projects process-scholarships calculate-recurrence aggregate-students aggregate-supervisors analyze-partnerships analyze-networks ## Run complete data processing pipeline
	@echo "$(COLOR_GREEN)✓ All data processing complete$(COLOR_RESET)"

process-groups: ## Process research groups CSV to JSON
	@echo "$(COLOR_BOLD)Processing research groups...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/process_research_groups.py
	@echo "$(COLOR_GREEN)✓ Research groups processed$(COLOR_RESET)"

process-projects: ## Process research projects CSV to JSON
	@echo "$(COLOR_BOLD)Processing research projects...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/process_research_projects.py
	@echo "$(COLOR_GREEN)✓ Research projects processed$(COLOR_RESET)"

process-scholarships: ## Process scholarships CSV to JSON
	@echo "$(COLOR_BOLD)Processing scholarships...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/process_scholarships.py
	@echo "$(COLOR_GREEN)✓ Scholarships processed$(COLOR_RESET)"

calculate-recurrence: ## Calculate student recurrence statistics
	@echo "$(COLOR_BOLD)Calculating student recurrence...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/calculate_student_recurrence.py
	@echo "$(COLOR_GREEN)✓ Student recurrence calculated$(COLOR_RESET)"

aggregate-students: ## Aggregate data by student
	@echo "$(COLOR_BOLD)Aggregating data by student...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/group_by_student.py
	@echo "$(COLOR_GREEN)✓ Student data aggregated$(COLOR_RESET)"

aggregate-supervisors: ## Aggregate data by supervisor
	@echo "$(COLOR_BOLD)Aggregating data by supervisor...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/group_by_supervisor.py
	@echo "$(COLOR_GREEN)✓ Supervisor data aggregated$(COLOR_RESET)"

analyze-partnerships: ## Analyze partnerships and external collaborations
	@echo "$(COLOR_BOLD)Analyzing partnerships...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/analyze_partnerships.py
	@echo "$(COLOR_GREEN)✓ Partnerships analyzed$(COLOR_RESET)"

analyze-networks: ## Generate network statistics for research groups
	@echo "$(COLOR_BOLD)Generating network statistics...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/generate_network_stats.py
	@echo "$(COLOR_GREEN)✓ Network statistics generated$(COLOR_RESET)"

translate-docs: ## Translate documentation to Portuguese
	@echo "$(COLOR_BOLD)Translating documentation...$(COLOR_RESET)"
	$(PYTHON) $(SRC_DIR)/translate_docs.py
	@echo "$(COLOR_GREEN)✓ Documentation translated$(COLOR_RESET)"

# Documentation
copy-data: ## Copy data files to documentation directory
	@echo "$(COLOR_BOLD)Copying data files to docs...$(COLOR_RESET)"
	mkdir -p $(DOCS_DIR)/docs/data
	cp $(DATA_DIR)/*.json $(DOCS_DIR)/docs/data/
	@echo "$(COLOR_GREEN)✓ Data files copied$(COLOR_RESET)"

build-docs: copy-data ## Build MkDocs documentation
	@echo "$(COLOR_BOLD)Building documentation...$(COLOR_RESET)"
	cd $(DOCS_DIR) && mkdocs build --clean --strict
	@echo "$(COLOR_GREEN)✓ Documentation built at $(SITE_DIR)$(COLOR_RESET)"

serve-docs: copy-data ## Serve documentation locally (http://127.0.0.1:8000)
	@echo "$(COLOR_BOLD)Starting documentation server...$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Open http://127.0.0.1:8000 in your browser$(COLOR_RESET)"
	cd $(DOCS_DIR) && mkdocs serve

# Complete workflow
build: process-all build-docs ## Process all data and build documentation
	@echo "$(COLOR_GREEN)✓ Complete build finished$(COLOR_RESET)"

# Development
dev: install serve-docs ## Install dependencies and start development server

# Testing
test: ## Run tests (if available)
	@echo "$(COLOR_BOLD)Running tests...$(COLOR_RESET)"
	@if [ -d "tests" ]; then \
		$(PYTHON) -m pytest tests/ -v; \
	else \
		echo "$(COLOR_YELLOW)No tests directory found$(COLOR_RESET)"; \
	fi

# Code Quality
lint: ## Run code linters
	@echo "$(COLOR_BOLD)Running linters...$(COLOR_RESET)"
	@echo "Checking with flake8..."
	-flake8 $(SRC_DIR) --max-line-length=100 --exclude=__pycache__
	@echo "$(COLOR_GREEN)✓ Linting complete$(COLOR_RESET)"

format: ## Format code with black
	@echo "$(COLOR_BOLD)Formatting code...$(COLOR_RESET)"
	black $(SRC_DIR) --line-length=100
	@echo "$(COLOR_GREEN)✓ Code formatted$(COLOR_RESET)"

type-check: ## Run type checking with mypy
	@echo "$(COLOR_BOLD)Running type checker...$(COLOR_RESET)"
	mypy $(SRC_DIR) --ignore-missing-imports
	@echo "$(COLOR_GREEN)✓ Type checking complete$(COLOR_RESET)"

# Deployment
deploy: build ## Deploy to GitHub Pages (requires git push)
	@echo "$(COLOR_BOLD)Deploying to GitHub Pages...$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Commit and push changes to trigger GitHub Actions deployment$(COLOR_RESET)"
	@echo ""
	@echo "Run these commands:"
	@echo "  git add ."
	@echo "  git commit -m 'Update data and documentation'"
	@echo "  git push origin main"

# Status and Info
status: ## Show status of data files
	@echo "$(COLOR_BOLD)Data Files Status:$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Source Files:$(COLOR_RESET)"
	@ls -lh $(SOURCE_DIR)/research_project/*.csv 2>/dev/null | wc -l | xargs echo "  Research Projects CSV:"
	@ls -lh $(SOURCE_DIR)/scholarships/*.csv 2>/dev/null | wc -l | xargs echo "  Scholarships CSV:"
	@ls -lh $(SOURCE_DIR)/research_groups/*.csv 2>/dev/null | wc -l | xargs echo "  Research Groups CSV:"
	@echo ""
	@echo "$(COLOR_BLUE)Processed Data:$(COLOR_RESET)"
	@if [ -f "$(DATA_DIR)/research_projects.json" ]; then \
		echo "  ✓ research_projects.json ($$(du -h $(DATA_DIR)/research_projects.json | cut -f1))"; \
	else \
		echo "  ✗ research_projects.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/scholarships.json" ]; then \
		echo "  ✓ scholarships.json ($$(du -h $(DATA_DIR)/scholarships.json | cut -f1))"; \
	else \
		echo "  ✗ scholarships.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/research_group.json" ]; then \
		echo "  ✓ research_group.json ($$(du -h $(DATA_DIR)/research_group.json | cut -f1))"; \
	else \
		echo "  ✗ research_group.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/students.json" ]; then \
		echo "  ✓ students.json ($$(du -h $(DATA_DIR)/students.json | cut -f1))"; \
	else \
		echo "  ✗ students.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/supervisors.json" ]; then \
		echo "  ✓ supervisors.json ($$(du -h $(DATA_DIR)/supervisors.json | cut -f1))"; \
	else \
		echo "  ✗ supervisors.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/partnership_analysis.json" ]; then \
		echo "  ✓ partnership_analysis.json ($$(du -h $(DATA_DIR)/partnership_analysis.json | cut -f1))"; \
	else \
		echo "  ✗ partnership_analysis.json (missing)"; \
	fi
	@if [ -f "$(DATA_DIR)/network_stats.json" ]; then \
		echo "  ✓ network_stats.json ($$(du -h $(DATA_DIR)/network_stats.json | cut -f1))"; \
	else \
		echo "  ✗ network_stats.json (missing)"; \
	fi
	@echo ""
	@if [ -d "$(SITE_DIR)" ]; then \
		echo "$(COLOR_BLUE)Documentation:$(COLOR_RESET)"; \
		echo "  ✓ Built at $(SITE_DIR)"; \
	else \
		echo "$(COLOR_YELLOW)Documentation not built yet$(COLOR_RESET)"; \
	fi

info: ## Show project information
	@echo "$(COLOR_BOLD)OneStep Research Observatory$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Project Structure:$(COLOR_RESET)"
	@echo "  Source Data:      $(SOURCE_DIR)/"
	@echo "  Python Scripts:   $(SRC_DIR)/"
	@echo "  Processed Data:   $(DATA_DIR)/"
	@echo "  Documentation:    $(DOCS_DIR)/"
	@echo "  Built Site:       $(SITE_DIR)/"
	@echo ""
	@echo "$(COLOR_BLUE)Python Version:$(COLOR_RESET)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(COLOR_BLUE)Quick Start:$(COLOR_RESET)"
	@echo "  1. make install       # Install dependencies"
	@echo "  2. make process-all   # Process all data"
	@echo "  3. make serve-docs    # View documentation locally"
	@echo ""
