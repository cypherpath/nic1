.PHONY=mypy

ABS_DIR=$(shell pwd)
MYPY_DIR=$(ABS_DIR)/:$(ABS_DIR)/stubs

MYPYPATH := $(MYPY_DIR)
export MYPYPATH

mypy:
	@echo "Running check..."
	@mypy $$(git ls-files -- "*.py")
