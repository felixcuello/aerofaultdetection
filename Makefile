plot:
	@echo ""
	@echo "-------------------------------------------------------------------------------"
	@echo "  💡 Analyzer  🧠"
	@echo "-------------------------------------------------------------------------------"
	@echo ""
	@echo " Options: "
	@echo "   make install_python_libraries  # No parameters"
	@echo "   make analyze   # No parameters"
	@echo "   make DATA=[\"FILE_NAME\"] COLUMN_NAME=[\"COLUMN_NAME\"] analyze    # w/parameters"
	@echo ""
	@echo ""
	@echo " If parameters are not set, they will be defaulted to:"
	@echo ""
	@echo " FILE_NAME=\"./data/D214102-2023.csv\""
	@echo " COLUMN_NAME=[\"ANEMOMETRO {};wind_speed;Avg (m/s)\"]"
	@echo ""
	@echo " Note: The '{}' is a placeholder for the column number when you have multiple devices."
	@echo ""

ifndef $(DATA)
FILE_NAME := ./data/D214102-2023.csv
COLUMN_NAME := ANEMOMETRO {};wind_speed;Avg (m/s)
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
