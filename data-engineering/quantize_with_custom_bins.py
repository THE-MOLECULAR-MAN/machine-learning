# Tim H 2023
# https://numpy.org/doc/stable/reference/generated/numpy.digitize.html
# Use Python (Pandas)
"""Custom SageMaker DataWrangler transformation"""
# This version requires you to specify the bins
# pylint: disable=used-before-assignment, import-error

import numpy as np

BIN_VALUES_ARR = np.array([5000, 20000, 40000, 80000, 150000])
BIN_VALUES_REP_TENURE_IN_MONTHS = np.array([3, 6, 12, 18, 24])

# customize these two lines only:
COLUMN_NAME_TO_QUANTIZE = "arr"
BIN_VALUES = BIN_VALUES_ARR


##############################################################################
# DON'T CHANGE ANYTHING BELOW HERE
##############################################################################

df = df.dropna()
column_binned = np.digitize(df[COLUMN_NAME_TO_QUANTIZE], BIN_VALUES)
df[COLUMN_NAME_TO_QUANTIZE] = column_binned
print(BIN_VALUES)
