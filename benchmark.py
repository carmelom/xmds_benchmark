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

root = Path('run')
fig, ax = plt.subplots()

filepaths = list(root.glob('**/*.h5'))
# print(filepaths)


def get_benchmark_data(filepath):
    data = {}
    with h5py.File(filepath, 'r') as f:
        data.update(f['configure'].attrs)
        data.update(f['log'].attrs)
    data['filepath'] = filepath
    data['hostname'] = gethostname()
    return pd.DataFrame(data, columns=pd.Index(data.keys()), index=[0])


df0 = pd.concat([get_benchmark_data(fp) for fp in filepaths], ignore_index=True)
df0['run_type'] = [('openmp', 'mpi')[t] for t in df0['run_mpi']]

df0.to_hdf(f"{gethostname()}_data.h5", key='dataframe')

# print(data)

groups = df0.groupby(['hostname', 'run_type'])

for name, data in groups:
    ax.loglog(data['lattice'], data['elapsed_time'], 'o', label=name)

ax.legend()
# plt.show()
