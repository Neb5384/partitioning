#imports-----------------
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds


#loading csv as df------------------
df = pd.read_csv("demo/data/ogd-nbcn_sio_d_historical.csv", sep = ";")
print(df.info())

#formatting date time correctly and giving day and year their own columns----------
df["reference_timestamp"] = pd.to_datetime(
    df["reference_timestamp"], format="%d.%m.%Y %H:%M"
).astype("datetime64[us]")
df["year"] = df["reference_timestamp"].dt.year.astype("int16")
df["date"] = df["reference_timestamp"].dt.strftime("%Y-%m-%d")

#only keeping last 3 years--------------------
df = df[df["year"] >= 2023]

#df to pyarrow table------
table = pa.Table.from_pandas(df, preserve_index=False)

#partitioning table into multiple parquet files------
def write_partitioned(table, path, col):
    ds.write_dataset(
        table,
        path,
        format="parquet",
        partitioning=ds.partitioning(table.select([col]).schema, flavor="hive"),
        max_partitions=366*3,   #for pc to not explode if oopsie
    )

write_partitioned(table, "demo/data/parquet/by_year", "year")  
write_partitioned(table, "demo/data/parquet/by_day", "date") 