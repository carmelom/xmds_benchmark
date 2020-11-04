#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 11-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""
Module docstring

"""


def read_log(filepath):
    with open(filepath, 'r') as f:
        L = f.readlines()
        L = [l.strip('\n ') for l in L]

    timesteps = []
    sampling_times = []

    for j, line in enumerate(L):
        # print(line)
        if line.startswith('Current timestep'):
            ts = float(line.split(' ')[-1])
            timesteps.append(ts)
            l1 = L[j - 1]
            t = float(l1.split(' ')[-1]) if l1.startswith('Sampled field') else 0
            sampling_times.append(t)
        elif line.startswith('Segment'):
            line = line.split(' ')
            timestep_min = float(line[4])
            timestep_max = float(line[7])
        elif line.startswith('Attempted'):
            line = line.split(' ')
            nsteps = int(line[1])
            failed = float(line[3][:-1]) / 100
        elif line.startswith('Time elapsed'):
            line = line.split(' ')
            elapsed_time = float(line[5])
    results = {}
    to_save = [
        'timesteps', 'sampling_times',
        'timestep_min', 'timestep_max',
        'nsteps', 'failed', 'elapsed_time'
    ]
    for var in to_save:
        exec(f"results['{var}'] = {var}")
    return results


if __name__ == '__main__':
    import sys
    read_log(sys.argv[1])
