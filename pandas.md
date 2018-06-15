# Sea in Pandas

## group
`df.groupby('l_customer_id_i').agg(lambda x: ','.join(x))` does already return a dataframe, so you cannot loop over the groups anymore.

In general:

`df.groupby(...)` returns a GroupBy object (a DataFrameGroupBy or SeriesGroupBy), and with this, you can iterate through the groups (as explained in the docs here). You can do something like:
```
grouped = df.groupby('A')

for name, group in grouped:
    ...
```    
When you apply a function on the groupby, in your example `df.groupby(...).agg(...)` (but this can also be `transform, 
apply, mean, ...`), you **combine** the result of **applying** the function to the different groups together in one dataframe
 (the apply and combine step of the 'split-apply-combine' paradigm of groupby). So the result of this will always be again
  a DataFrame (or a Series depending on the applied function).