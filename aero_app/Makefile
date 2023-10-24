plot:
	@echo ""
	@echo "--[ Plot ]-------------------------------------------------------------"
	@echo ""
	@echo "make plot_anemo             # Plots anemometers"
	@echo "make plot_veleta            # Plots veletas"
	@echo "make plot_barometro         # Plots barometros"
	@echo "make plot_a                 # Plots channel A"
	@echo "make plot_c                 # Plots channel C"
	@echo "make plot_d                 # Plots channel D"
	@echo "make plot_i                 # Plots channel I"
	@echo "make plot_v                 # Plots channel V"
	@echo ""
	@echo "plot_attempt_1              # Plots an isolation forest approach"
	@echo "plot_attempt_2              # Plots a Super Vector Machine approach (#1)"
	@echo "plot_attempt_3              # Plots a Super Vector Machine approach (#2)"
	@echo "plot_attempt_4              # Plots a Random Forest approach"
	@echo "plot_attempt_6              # Plots a K-means approach"
	@echo "plot_attempt_6_cimarron     # Plots a K-means approach for cimarron"
	@echo "plot_attempt_7              # Plots a Mean Shift approach"
	@echo ""
	@echo "train                       # Trains the model"
	@echo ""

ifndef $(DATA)
DATA=./data/D214102-2023.csv
endif

train:
	python3 train.py

plot_anemo:
	python3 plot.py anemo $(DATA)

plot_veleta:
	python3 plot.py veleta $(DATA)

plot_barometro:
	python3 plot.py barometro $(DATA)

plot_a:
	python3 plot.py a $(DATA)

plot_c:
	python3 plot.py c $(DATA)

plot_d:
	python3 plot.py d $(DATA)

plot_i:
	python3 plot.py i $(DATA)

plot_v:
	python3 plot.py v $(DATA)

plot_attempt_1:
	python3 attempt_1_isolation_forest.py $(DATA)

plot_attempt_2:
	python3 attempt_2_oneclass_svm.py $(DATA)

plot_attempt_3:
	python3 attempt_3_oneclass_svm.py $(DATA)

plot_attempt_4:
	python3 attempt_4_supervised.py $(DATA)

plot_attempt_6:
	python3 attempt_6_kmeans.py $(DATA)

# make DATA=data/D214102-cimarron-torre3.csv attempt_6_kmeans
plot_attempt_6_cimarron:
	python3 DATA=data/D214102-cimarron-torre3.csv attempt_6_kmeans.py

plot_attempt_7:
	python3 attempt_7_mean_shift.py $(DATA)
