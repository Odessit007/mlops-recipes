* [Intro](#intro)
  * [Features](#features)
  * [Connection](#connection)
  * [Concurrency](#concurrency)
  * [Configuration](#configuration)
* [Parquet](#parquet)
  * [Read](#read)
  * [Write](#write)
  * [Query](#query)



<a id="intro"></a>
# Introduction


<a id="features"></a>
## Features
DuckDB is a relational database management system (RDBMS) that supports SQL queries.

It provides [CLI](https://duckdb.org/docs/api/cli/overview) as well as APIs for C, C++, Go, Java, Julia, Node.js, 
Python, R, Rust, Swift, and Wasm.

Some features:
* Open-source with MIT License
* DuckDB has no external dependencies and thus it's extremely portable
* Can be used on Linux, macOS and Windows
* No DBMS server to install, update and maintain
* DuckDB doesn't run as a separate process, but instead it's completely embedded within a host process
  * this allows a high-speed data transfer to and from the database
  * sometimes DuckDB can process foreign data without copying (for example, DuckDB Python package can run queries
    directly on Pandas data without ever importing or copying any data)
* DuckDB provides transactional guarantees (ACID properties)
* Fast: DuckDB is designed to support analytical query workloads
* Extensible: there is a flexible extension mechanism that allows defining new data types, functions, file formats and
  new SQL syntax
  * Key features, such as support for the Parquet file format, JSON, and S3 protocol are implemented as extensions
  * There are extensions for full text search and for vector similarity search

**N.B.** DuckDB is optimized for bulk operations, so executing many small transactions is not a primary design goal.

Some interesting features of SQL that DuckDB supports are
* [Positional joins](https://duckdb.org/docs/sql/query_syntax/from#positional-joins) that allow joining two tables vertically
* [FILTER clause](https://duckdb.org/docs/sql/query_syntax/filter) in aggregate functions
* there are many more


<a id="connection"></a>
## Connection
To use DuckDB, you must first create a connection to a database. The exact syntax varies between the client APIs,
but it typically involves passing an argument to configure persistence.

DuckDB can operate in both persistent mode, where the data is saved to disk, and in in-memory mode, where the 
entire data set is stored in the main memory.
* Running on a persistent database allows larger-than-memory workloads.
* The files used for persistence can have an arbitrary extension, but `.db` and `.duckdb` are two common choices.
* In in-memory mode, no data is persisted to disk, therefore, all data is lost when the process finishes.
* In most clients, in-memory mode can be activated by passing the special value `:memory:` as the database file or
  omitting the database file argument.

There is a [cheatsheet](https://github.com/tldr-pages/tldr/blob/main/pages/common/duckdb.md) for CLI.


<a id="concurrency"></a>
## Concurrency
DuckDB has two configurable options for concurrency:
1. One process can both read and write to the database.
2. Multiple processes can read from the database, but no processes can write (access_mode = 'READ_ONLY').


<a id="configuration"></a>
## Configuration
Querying current parameter values:
```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'threads'
```

Set value:
```sql
SET threads = 1
```

Reset value to the default:
```sql
RESET threads
```



<a id="parquet"></a>
# Parquet
DuckDB supports **projection pushdown** into the Parquet reader. That is, when querying a Parquet file, only the columns
required for the query are read. This allows you to read only the part of the Parquet file that you are interested in. 
This will be done automatically by DuckDB.

DuckDB also supports **filter pushdown** into the Parquet reader. When you apply a filter to a column that is scanned
from a Parquet file, the filter will be pushed down into the scan, and can even be used to skip parts of the file 
using the built-in zonemaps. Note that this will depend on whether your Parquet file contains zonemaps.

See here for some examples: https://duckdb.org/docs/data/parquet/overview.


<a id="read"></a>
## Read
Read Parquet files:
```sql
-- Read from a single file
SELECT * FROM read_parquet('input.parquet');
-- Create a new table using the result from a query
CREATE TABLE new_tbl AS SELECT * FROM read_parquet('input.parquet');
-- Load data into an existing table from a query,
INSERT INTO tbl SELECT * FROM read_parquet('input.parquet');
```

`read_parquet` function accepts some optional parameters described [here](https://duckdb.org/docs/data/parquet/overview#read_parquet-function).

Multiple files can be read at once by providing a glob or a list of files. Examples:
```sql
-- read all files that match the glob pattern
SELECT * FROM 'test/*.parquet';
-- read 3 Parquet files and treat them as a single table
SELECT * FROM read_parquet(['file1.parquet', 'file2.parquet', 'file3.parquet']);
-- Read all Parquet files from 2 specific folders
SELECT * FROM read_parquet(['folder1/*.parquet', 'folder2/*.parquet']);
-- read all Parquet files that match the glob pattern at any depth
SELECT * FROM read_parquet('dir/**/*.parquet');
```
Read more about multi-file reads and glob syntax [here](https://duckdb.org/docs/data/multiple_files/overview#multi-file-reads-and-globs).


<a id="write"></a>
## Write
Write Parquet files:
```sql
-- Writing a table
COPY tbl TO 'output.parquet' (FORMAT PARQUET);
-- Writing query results
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT PARQUET);
-- Specifying compression and row group size
COPY
    (FROM generate_series(100_000))
    TO 'row-groups-zstd.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100_000);
```


<a id="query"></a>
## Query
Query Parquet files:
```sql
SELECT *
FROM read_parquet('path_to_file.parquet')
```

Query Parquet metadata:
```sql
SELECT *
FROM parquet_metadata('test.parquet');
```

Query Parquet schema:
```sql
-- fetch the column names and column types
DESCRIBE SELECT * FROM 'test.parquet';
-- fetch the internal schema of a Parquet file
SELECT *
FROM parquet_schema('test.parquet');
```

Query Parquet file-level metadata (such as the format version and the encryption algorithm used):
```sql
SELECT *
FROM parquet_file_metadata('test.parquet');
```

Query Parquet key-value metadata (custom metadata defined as key-value pairs):
```sql
SELECT *
FROM parquet_kv_metadata('test.parquet');
```



# Recipes and Tips
## Directly querying Parquet files
DuckDB supports directly querying Parquet files, but there are pros and cons for doing this instead of first loading
them to the database.

Pros:
* Parquet allows projection and filter pushdown so workloads that combine projection, filtering, and aggregation tend to
perform quite well when run on Parquet files.
* Loading the data from Parquet files will require approximately the same amount of space for the DuckDB database file.
Querying Parquet directly allows to save this space.

Cons:
* The DuckDB database format supports statistics that Parquet files do not have. These improve the accuracy of
cardinality estimates, and are especially important if the queries contain a large number of join operators.
* Some Parquet files are compressed using heavyweight compression algorithms such as gzip. In these cases, querying
the Parquet files will necessitate an expensive decompression time every time the file is accessed.

Tips:
* If the available disk space is constrained, it is worth running the queries directly on Parquet files.
* If you find that DuckDB produces a suboptimal join order on Parquet files, try loading the Parquet files to DuckDB
tables. The improved statistics likely help obtain a better join order.
* If you plan to run multiple queries on the same data set, it is worth loading the data into DuckDB. The queries will
always be somewhat faster, which over time amortizes the initial load time. This might be particularly relevant for
compressed files.


## Combining schemas
When reading from multiple files, we have to combine schemas from those files. 
This can be done in two ways:
* by column position (default);
* by column name (this should be used when files have different schemas; for files that do not have certain columns,
NULL values are filled in).

Example:
```
SELECT *
FROM read_csv(['file1.csv', 'file2.csv'], union_by_name = true);
```


## Zonemaps
DuckDB automatically creates **zonemaps** (also known as min-max indexes) for the columns of all general-purpose data 
types. These indexes are used for predicate pushdown into scan operators and computing aggregations. 

This means that if a filter criterion (like WHERE column1 = 123) is in use, DuckDB can skip any row group whose min-max 
range does not contain that filter value (e.g., a block with a min-max range of 1000 to 2000 will be omitted when 
comparing for = 123 or < 400).

The more ordered the data within a column, the more useful the zonemap indexes will be. If specific columns will be 
queried with selective filters, it is best to pre-order data by those columns when inserting it. Even an imperfect 
ordering will still be helpful.

According to [DuckDB microbenchmark](https://duckdb.org/docs/guides/performance/indexing#microbenchmark-the-effect-of-ordering), 
simply keeping the column order allows for improved compression, yielding a 2.5x smaller storage size. It also allows 
the computation to be 1.5x faster.


## ART Indexes
DuckDB allows defining Adaptive Radix Tree (ART) indexes. Such an index is created implicitly for columns with 
PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints. Second, explicitly running the CREATE INDEX statement creates an ART 
index on the target column(s).

The tradeoffs of having an ART index on a column are as follows:
* It enables efficient constraint checking upon changes (inserts, updates, and deletes) for non-bulky changes.
* Having an ART index makes changes to the affected column(s) slower compared to non-indexed performance.
That is because of index maintenance for these operations.

Regarding query performance, an ART index has the following effects:
* It speeds up point queries and other highly selective queries using the indexed column(s), where the filtering 
condition returns approx. 0.1% of all rows or fewer. When in doubt, use EXPLAIN to verify that your query plan uses 
the index scan.
* An ART index has no effect on the performance of join, aggregation, and sorting queries.

Indexes are serialized to disk and deserialized lazily, i.e., when the database is reopened, operations using the index 
will only load the required parts of the index. Therefore, having an index will not cause any slowdowns when opening 
an existing database.


## Summary of best practices
### Parquet-related best practices
If you have the storage space available, and have a join-heavy workload and/or plan to run many queries on the same
dataset, load the Parquet files into the database first. The compression algorithm and the row group sizes in the
Parquet files have a large effect on performance: study these using the `parquet_metadata` function.

DuckDB can parallelize over row groups and across multiple Parquet files.
* DuckDB works best on Parquet files with row groups of 100K-1M rows each. See more details
[here](https://duckdb.org/docs/guides/performance/file_formats#the-effect-of-row-group-sizes)
* It is advisable to have at least as many total row groups across all files as there are CPU threads. For example,
with a machine having 10 threads, both 10 files with 1 row group and 1 file with 10 row groups will achieve full parallelism.

More row groups beyond the thread count would improve the speed of highly selective queries, but slow down queries that 
must scan the whole file like aggregations.

The ideal file size is between 100MB and 10GB per individual Parquet file.

When querying many files with filter conditions, performance can be improved by using a Hive-format folder structure to 
partition the data along the columns used in the filter condition. DuckDB will only need to read the folders and files 
that meet the filter criteria. This can be especially helpful when querying remote files. You can find details 
[here](https://duckdb.org/docs/data/partitioning/hive_partitioning).

See more tips on writing Parquet files [here](https://duckdb.org/docs/data/parquet/tips#tips-for-writing-parquet-files).


### Bulk inserts
Unless your data is small (<100k rows), avoid using inserts in loops. Use bulk operations instead.


### Indexing-related best practices:
* If specific columns will be queried with selective filters, it is best to pre-order data by those columns when
inserting it. This can improve both the computation and the storage size.
* Only use primary keys, foreign keys, or unique constraints, if these are necessary for enforcing constraints
on your data.
* Do not define explicit indexes unless you have highly selective queries.
* If you define an ART index, do so after bulk loading the data to the table. Adding an index prior to loading, either 
explicitly or via primary/foreign keys, is detrimental to load performance.
* ART index speeds up point queries and other highly selective queries using the indexed column(s), where the filtering 
condition returns approximately 0.1% of all rows or fewer. It has no effect on the performance of join, aggregation, 
and sorting queries.


### Environment-related best practices:
* Aim for 5-10 GB memory per thread (with a minimum of 125 MB per thread)
* If you have a limited amount of memory, try to limit the number of threads, e.g., by issuing `SET threads = 4;`.
* Fast disks are important if your workload is larger than memory and/or fast data loading is important. Only use 
network-backed disks if they guarantee high IO.
* Among Linux distributions, DuckDB developers recommended using Ubuntu Linux LTS due to its stability and the fact 
that most of DuckDB’s Linux test suite jobs run on Ubuntu workers.
