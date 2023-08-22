plot:
	@echo ""
	@echo "--[ Plot ]-------------------------------------------------------------"
	@echo ""
	@echo "make plot_anemo                   # Plots anemometers"
	@echo "make plot_veleta                  # Plots veletas"
	@echo "make plot_barometro               # Plots barometros"
	@echo "make plot_a                       # Plots channel A"
	@echo "make plot_c                       # Plots channel C"
	@echo "make plot_d                       # Plots channel D"
	@echo "make plot_i                       # Plots channel I"
	@echo "make plot_v                       # Plots channel V"
	@echo ""
	@echo "make plot_attempt_1               # Plots an isolation forest approach"
	@echo "make plot_attempt_2               # Plots a Super Vector Machine approach (#1)"
	@echo "make plot_attempt_3               # Plots a Super Vector Machine approach (#2)"
	@echo "make plot_attempt_4               # Plots a Random Forest approach"
	@echo "make plot_attempt_4_cimarron"
	@echo "make plot_attempt_5_veleta"
	@echo ""
	@echo "train                  # Trains the model"
	@echo ""

train:
	python3 train.py

plot_anemo:
	python3 plot.py anemo ./data/D214102-2023.csv

plot_veleta:
	python3 plot.py veleta ./data/D214102-2023.csv

plot_barometro:
	python3 plot.py barometro ./data/D214102-2023.csv

plot_a:
	python3 plot.py a ./data/D214102-2023.csv

plot_c:
	python3 plot.py c ./data/D214102-2023.csv

plot_d:
	python3 plot.py d ./data/D214102-2023.csv

plot_i:
	python3 plot.py i ./data/D214102-2023.csv

plot_v:
	python3 plot.py v ./data/D214102-2023.csv

plot_attempt_1:
	python3 attempt_1_isolation_forest.py data/D214102-2023.csv

plot_attempt_2:
	python3 attempt_2_oneclass_svm.py data/D214102-2023.csv

plot_attempt_3:
	python3 attempt_3_oneclass_svm.py data/D214102-2023.csv

plot_attempt_4:
	python3 attempt_4_supervised.py data/D214102-2023.csv

plot_attempt_4_cimarron:
	python3 attempt_4_supervised.py data/D214102-cimarron-torre3.csv

plot_attempt_5_veleta:
	python3 attempt_5_supervised_veleta.py data/D214102-2023.csv
