#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 11-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""
Module docstring

"""

from socket import gethostname
import matplotlib.pyplot as plt

import h5py
from pathlib import Path
import pandas as pd

# sequences = [0, 1]

df1 = pd.read_hdf("Alfred_data.h5", key='dataframe')
df2 = pd.read_csv("weber_data.csv")

df0 = pd.concat([df1, df2], ignore_index=True)


groups = df0.groupby(['hostname', 'run_type'])

fig, ax = plt.subplots()

for name, data in groups:
    ax.loglog(data['lattice'], data['elapsed_time'], 'o', label=name)

ax.legend()
plt.show()
