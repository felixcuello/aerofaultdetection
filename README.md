# Introduction

The following code is the implementation of I paper I wrote in December 2023,
where we were trying to identify anomalies in a time series CSV get from a
SCADA.

The idea is to identify automatically errors in timeseries.

The steps are written as comments in the code, but the investigation and
justification about this is writen in a separate paper that was delivered
along with this software.

# SetUp

You need to have `make` and `python` installed in your computer.

After running `make` you will see the options like this:

```
-------------------------------------------------------------------------------
  💡 Analyzer  🧠
-------------------------------------------------------------------------------

 Options:
   make analyze                   # Analyze the data [local]
   make build                     # Build the container
   make install_python_libraries  # Install python libraries [local]
   make run                       # Analyze the data [container]
   make shell                     # Run the container in shell mode
   make clean                     # Remove PNG files
```

## Installing Libraries

All python libraries can be installed by running `make install_python_libraries`.

## Docker

This is in my TO-DO list. It's not very complex to set up, but I haven't finished that yet.

There's a `Dockerfile` already but I don't remember how good that works

# Running the code

You can run the code by running `make analyze`. The `analyzer.py` receives the file name and
column name you want to analyze, for example :

analyzer.py file.csv "ANEMOMETRO {};wind_speed;Avg (m/s)"

And will analyze that particular column. The reason why we have two curly braces in the column
name is because that's going to be replaced by the device's numbers, so for example in some file
you can have:

ANEMOMETRO 1;wind_speed;Avg (m/s)
ANEMOMETRO 2;wind_speed;Avg (m/s)
ANEMOMETRO 3;wind_speed;Avg (m/s)
ANEMOMETRO 4;wind_speed;Avg (m/s)

And the `analyzer.py` will automatically detect how many they are and replace the `{}` accordingly.

