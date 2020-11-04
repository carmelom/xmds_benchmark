#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
import itertools
from copy import deepcopy
from src.h5tools import autosequence

from random import shuffle

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'dep_file': '.doit_scan.db',
}


with open('configure.yaml', 'r') as f:
    conf = yaml.safe_load(f)

run_dir = Path(conf['run_dir'])
run_dir.mkdir(parents=True, exist_ok=True)
sequence_index = autosequence(run_dir)

scan = {
    'lattice': [64, 1024, ]  # [32, 256, 2048]
    # 'lattice': [2**k for k in range(5, 12)],
    # 'repeat': list(range(3))
}

keys, values = list(zip(*scan.items()))

shots = []
for item in itertools.product(*values):
    conf.update(dict(zip(keys, item)))
    shots.append(deepcopy(conf))

shuffle(shots)


def task_run_sequence():
    def _write_conf(_conf, filename):
        with open(filename, 'w') as f:
            f.write(yaml.safe_dump(_conf))

    for j, conf in enumerate(shots):
        conf_name = '_config.yaml'
        yield {
            'name': j,
            'actions': [
                (_write_conf, [conf, conf_name]),
                f"doit config_file={conf_name} sequence_index={sequence_index} run_number={j}"
            ]
        }


# def task_clear():
#     return {
#         'actions': ['doit -f dodo1.py clear']
#     }
