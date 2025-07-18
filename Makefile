# Makefile for building and testing check_k8s

# Extract version from Python module
version := $(shell python3 -c 'from k8s import __version__; print(__version__)')
name := monitor-plugin-check_k8s
python_ver ?= 3.9

help:
	@echo "\n%% check_aws dev tools %%"
	@echo "Usage: make <target> [python_ver=X.Y]"
	@echo ""
	@echo "Available targets:"
	@echo "- deps:      install build dependencies"
	@echo "- build:     create venv and install dependencies"
	@echo "- test:      run tests (calls build)"
	@echo "- lint:      check code formatting (calls build)"
	@echo "- update:    update dependencies through Poetry"
	@echo "- rpm:       create RPM package for Enterprise Linux 8"
	@echo "- clean:     remove cache and bytecode files"
	@echo ""

# Install build dependencies
.deps-stamp:
	# Install RPM build tools and m4 macro processor
	dnf install rpm-build m4
	touch .deps-stamp

deps: .deps-stamp  

# Build target - sets up Python environment and dependencies
.build-stamp: pyproject.toml poetry.lock
	# Create a virtual environment
	python$(python_ver) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install poetry wheel

	# Install including dependencies
	.venv/bin/poetry env info
	.venv/bin/poetry install --no-interaction --no-root
	touch .build-stamp

build: .build-stamp

# Test and lint codes
test: .build-stamp
	.venv/bin/poetry run python -m pytest -v

lint: .build-stamp
	.venv/bin/poetry run flake8 check_k8s.py k8s
	.venv/bin/poetry run black --check check_k8s.py k8s

# Build Python wheels
.wheels-stamp: .build-stamp $(shell find . -name "*.py" -not -path "./.venv/*" -not -path "./RPM/*")
	.venv/bin/poetry build -f wheel  # writes to dist/
	.venv/bin/pip wheel pip -w dist/
	touch .wheels-stamp

wheels: .wheels-stamp

# Update dependencies using Poetry
.poetry-update-stamp: pyproject.toml
	python$(python_ver) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install poetry
	.venv/bin/poetry update
	touch .poetry-update-stamp

update: .poetry-update-stamp

# Clean up build artifacts and temporary files
clean:
	rm -rf RPM/{BUILD,RPMS,SOURCES,SRPMS}                          # Remove RPM build directories
	find . -type d -name __pycache__ -exec rm -rf {} +             # Remove Python cache directories
	find . -type f -name "*.py[co]" -delete                        # Remove compiled Python files
	rm -rf .venv                                                   # Remove virtual environments
	rm -f .*-stamp
