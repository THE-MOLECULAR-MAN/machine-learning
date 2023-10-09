# Tim H 2023
# https://aws.amazon.com/blogs/machine-learning/authoring-custom-transformations-in-amazon-sagemaker-data-wrangler-using-nltk-and-scipy/
"""x"""
# pylint: disable=used-before-assignment, import-error

# Use Python (Pandas)
# This version always auto-creates the BINS, you can't specify them

# Table is available as variable `df`
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np

COLUMN_TO_BIN = "arr"
MAX_NUMBER_OF_BINS_TO_CREATE = 10

df = df.dropna()
kbins = KBinsDiscretizer(n_bins=MAX_NUMBER_OF_BINS_TO_CREATE, encode='ordinal',
                         strategy='uniform')
new_vals = np.array(df[COLUMN_TO_BIN]).reshape(-1, 1)
df[COLUMN_TO_BIN] = kbins.fit_transform(new_vals)
print(kbins.bin_edges_)
