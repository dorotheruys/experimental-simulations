# experimental-simulations

How the sorting works in the randomization stuff:

df.groupby('Elevator').apply(lambda x: x.sample(frac=1)).reset_index(drop=True)

The `lambda` function is defined as `lambda x: x.sample(frac=1)`. Here's what it does:

- `lambda x:`: This part of the function defines the argument `x`. In this context, `x` represents a group of rows in the DataFrame that all have the same `Elevator` value.

- `x.sample(frac=1)`: This is the expression that the lambda function evaluates. The `sample(frac=1)` method is called on `x`, which, as mentioned above, is a group of rows in the DataFrame. The `frac=1` argument means that `sample()` should return all rows in the group, but in a random order.

So, in essence, the lambda function takes a group of rows as input and returns a new DataFrame that contains all the same rows, but in a random order.

The `apply()` method then applies this lambda function to each group of rows in the DataFrame (where each group has the same `Elevator` value), effectively shuffling the rows within each group.

Finally, `reset_index(drop=True)` is called on the result to reset the DataFrame's index and drop the old index.

