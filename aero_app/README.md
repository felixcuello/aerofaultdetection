# README to the aero_app

## Introduction

This directory contains things specifically related to the application and the scripts created for this purpose.

## Makefile

To make things easier we have created a `Makefile` that will help us to script and tag things that can be
executed.

## Data Visualization

In order to make the data visualization you can choose to any of the available plot options:

```
make plot_anemo        # Plots anemometers
make plot_veleta       # Plots veletas
make plot_barometro    # Plots barometros
make plot_a            # Plots channel A
make plot_c            # Plots channel C
make plot_d            # Plots channel D
make plot_i            # Plots channel I
make plot_v            # Plots channel V
make plot attempt_1    # Plots an isolation forest approach"
make plot attempt_2    # Plots a Super Vector Machine approach (#1)"
make plot attempt_3    # Plots a Super Vector Machine approach (#2)"
make plot attempt_4    # Plots a Random Forest approach"
```

## Machine Learning Model

### Training Data

To perform some tests and create the model we have used the `D214102-2023.csv` file where we already knew
there was a problem in the anemometer #1.

The file can be divided like this:

```
------------+-------------+------------------------------------------------------------
FROM LINE   | TO LINE     | Description
------------+-------------+------------------------------------------------------------
0           | 0           | Headers
1           | 2281        | All anemometers are working as expected
2282        | 4616        | Anemometer #1 shows a problem
4617        | 7584        | All anemometers are working as expected
7585        | 8967        | Anemometer #1 shows a problem
8968        | 10513       | All anemometers are working as expected
------------+-------------+------------------------------------------------------------
```


## Links

https://towardsdatascience.com/using-lstm-autoencoders-on-multidimensional-time-series-data-f5a7a51b29a1
