plot:
	@echo ""
	@echo "-------------------------------------------------------------------------------"
	@echo "  💡 Analyzer  🧠"
	@echo "-------------------------------------------------------------------------------"
	@echo ""
	@echo " Options: "
	@echo "   make analyze                   # Analyze the data [local]"
	@echo "   make build                     # Build the container"
	@echo "   make install_python_libraries  # Install python libraries [local]"
	@echo "   make run                       # Analyze the data [container]"
	@echo "   make shell                     # Run the container in shell mode"
	@echo "   make clean                     # Remove PNG files"
	@echo ""
	@echo ""

APP_DIR := $(shell pwd)
ifndef $(DATA)
#  If parameters are not set, they will be defaulted to:
#
#  FILE_NAME=\./data/D214102-2023.csv\
#  COLUMN_NAME=[\ANEMOMETRO {};wind_speed;Avg (m/s)\]
#
#  Note: The '{}' is a placeholder for the column number when you have multiple devices.
#
FILE_NAME := ./data/D214102-2023.csv
COLUMN_NAME := ANEMOMETRO {};wind_speed;Avg (m/s)
# COLUMN_NAME := VELETA {};wind_direction;Avg (°)
# COLUMN_NAME := A{};channel;Avg (V)
# COLUMN_NAME := C{};channel;Avg (I)
# COLUMN_NAME := D{};channel;Avg ()
endif

install_python_libraries:
	@echo ""
	@echo "Installing python libraries..."
	@echo ""
	@pip3 install -r requirements.txt

analyze:
	@echo ""
	@echo "Analyzing \"$(FILE_NAME)\"   /   with column \"$(COLUMN_NAME)\""
	@echo ""
	@python3 analyzer.py '$(FILE_NAME)' '$(COLUMN_NAME)'

build:
	@echo ""
	@echo "Building container..."
	@echo ""
	@docker build -t analyzer .

run:
	@echo ""
	@echo "Analyzing \"$(FILE_NAME)\"   /   with column \"$(COLUMN_NAME)\""
	@echo ""
	@docker -v $(APP_DIR):/app run

shell:
	@echo ""
	@echo "Running container in shell mode..."
	@echo ""
	@docker run -it -v $(APP_DIR):/app analyzer /bin/bash
