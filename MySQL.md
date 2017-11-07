# 10.9.2017

## find all the tables in MYSQL with specific column names in them
To get all tables with columns columnA or ColumnB in the database YourDatabase:
```MySQL
SELECT DISTINCT TABLE_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME IN ('columnA','ColumnB')
        AND TABLE_SCHEMA='YourDatabase';
```  

## caution to insert null when importing csv to db   
Handling of NULL values varies according to the FIELDS and LINES options in use:

For the default FIELDS and LINES values, NULL is written as a field value of \N for output, and a field value of \N is read as NULL for input (assuming that the ESCAPED BY character is \).

If FIELDS ENCLOSED BY is not empty, a field containing the literal word NULL as its value is read as a NULL value. This differs from the word NULL enclosed within FIELDS ENCLOSED BY characters, which is read as the string 'NULL'.

If FIELDS ESCAPED BY is empty, NULL is written as the word NULL.

With fixed-row format (which is used when FIELDS TERMINATED BY and FIELDS ENCLOSED BY are both empty), NULL is written as an empty string. This causes both NULL values and empty strings in the table to be indistinguishable when written to the file because both are written as empty strings. If you need to be able to tell the two apart when reading the file back in, you should not use fixed-row format.

An attempt to load NULL into a NOT NULL column causes assignment of the implicit default value for the column's data type and a warning, or an error in strict SQL mode. Implicit default values are discussed in Section 11.7, “Data Type Default Values”.

## optimum varchar sizes for MySQL
 on disk MySql uses 1 + the size that is used in the field to store the data (so if the column was declared varchar(45), and the field was "FooBar" it would use 7 bytes on disk, unless of course you where using a multibyte character set, where it would be using 14 bytes). So, however you declare your columns, it wont make a difference on the storage end (you stated you are worried about disk optimization for a massive table). However, it does make a difference in queries, as VARCHAR's are converted to CHAR's when MySql makes a temporary table (SORT, ORDER, etc) and the more records you can fit into a single page, the less memory and faster your table scans will be.
 
 The statement on multibyte is very misleading. UTF-8 is a multibyte character encoding and yet for ASCII and Latin1 characters (the first 256 characters of UTF8) you will have a one byte-one character correspondence. UTF-16 will use, only for code points in the Basic Multilingual Plane, 2 bytes per code point.
 
 ## extended reading Best Practices for SQL varchar column length
 
 No DBMS I know of has any "optimization" that will make a VARCHAR with a 2^n length perform better than one with a max length that is not a power of 2.

I think early SQL Server versions actually treated a VARCHAR with length 255 differently than one with a higher maximum length. I don't know if this is still the case.

For almost all DBMS, the actual storage that is required is only determined by the number of characters you put into it, not the max length you define. So from a storage point of view (and most probably a performance one as well), it does not make any difference whether you declare a column as VARCHAR(100) or VARCHAR(500).

You should see the max length provided for a VARCHAR column as a kind of constraint (or business rule) rather than a technical/physical thing.

For PostgreSQL the best setup is to use text without a length restriction and a CHECK CONSTRAINT that limits the number of characters to whatever your business requires.

If that requirement changes, altering the check constraint is much faster than altering the table (because the table does not need to be re-written)

The same can be applied for Oracle and others - in Oracle it would be VARCHAR(4000) instead of text though.

I don't know if there is a physical storage difference between VARCHAR(max) and e.g. VARCHAR(500) in SQL Server. But apparently there is a performance impact when using varchar(max) as compared to varchar(8000).

See this link (posted by Erwin Brandstetter as a comment)

Edit 2013-09-22

Regarding bigown's comment:

In Postgres versions before 9.2 (which was not available when I wrote the initial answer) a change to the column definition did rewrite the whole table, see e.g. here. Since 9.2 this is no longer the case and a quick test confirmed that increasing the column size for a table with 1.2 million rows indeed only took 0.5 seconds.

For Oracle this seems to be true as well, judging by the time it takes to alter a big table's varchar column. But I could not find any reference for that.

For MySQL the manual says "In most cases, ALTER TABLE makes a temporary copy of the original table". And my own tests confirm that: running an ALTER TABLE on a table with 1.2 million rows (the same as in my test with Postgres) to increase the size of a column took 1.5 minutes. In MySQL however you can not use the "workaround" to use a check constraint to limit the number of characters in a column.

For SQL Server I could not find a clear statement on this but the execution time to increase the size of a varchar column (again the 1.2 million rows table from above) indicates that no rewrite takes place.

Edit 2017-01-24

Seems I was (at least partially) wrong about SQL Server. See this answer from Aaron Bertrand that shows that the declared length of a nvarchar or varchar columns makes a huge difference for the performance.
 	
If the size is more than 255, the total space required should be size * N + 2.


Actually, there is a difference between VARCHAR(255) and VARCHAR(500), even if you put 1 character inside such column. The value appended at the end of the row will be an integer that stores what the actual length of stored data is. In case of VARCHAR(255) it will be 1 byte integer. In case of VARCHAR(500) it will be 2 bytes. it's a small difference, but one should be aware of it. I don't have any data on hand how it can affect performance, but I assume it's so small that it's not worth researching. 

Change varchar length does not rewrite the table. It just check the constraint length against the entire table exactly as CHECK CONSTRAINT. If you increase length there is nothing to do, just next insert or updates will accept bigger length. If you decrease length and all rows pass the new smaller constraint, Pg doesn't take any further action besides to allow next inserts or updates to write just the new length.


## Replace substring in string

[StackOverflow](https://stackoverflow.com/questions/10177208/update-a-column-value-replacing-part-of-a-string)
```python
UPDATE urls
SET url = REPLACE(url, 'domain1.com/images/', 'domain2.com/otherfolder/')
```

## Some tips for bulkloading

[StackOverflow](https://stackoverflow.com/questions/2463602/mysql-load-data-infile-acceleration)

if you're using innodb and bulk loading here are a few tips:

sort your csv file into the primary key order of the target table : remember innodb uses clustered primary keys so it will load faster if it's sorted !

typical load data infile i use:
```
truncate <table>;

set autocommit = 0;

load data infile <path> into table <table>...

commit;
```
other optimisations you can use to boost load times:
```
set unique_checks = 0;
set foreign_key_checks = 0;
set sql_log_bin=0;
split the csv file into smaller chunks
```
typical import stats i have observed during bulk loads:
```
3.5 - 6.5 million rows imported per min
210 - 400 million rows per hour 
```
