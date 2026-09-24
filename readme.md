# Partitioning and the small-files problem

Partitioning by day made the same query slower. This demo shows why, using Delta Lake and Spark on MeteoSwiss daily data (Sion station, 2023 onwards).

The same data is written twice, partitioned by day and by year. Two queries then run on both layouts (a single day and three years). For each of the four cases it reports the median time of 5 runs and the number of files read.

## Setup

Requires Python 3 and Java (for Spark).

pip install pandas pyarrow pyspark delta-spark

## Run

python demo/partitioning.py && python demo/request.py

## Data

[MeteoSwiss OGD-NBCN, Sion, daily historical](https://data.geo.admin.ch/ch.meteoschweiz.ogd-nbcn/sio/ogd-nbcn_sio_d_historical.csv)
