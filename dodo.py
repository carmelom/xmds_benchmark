#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from src import tasks
from src import h5tools
from src.read_log import read_log
from doit import get_var

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    # 'default_tasks': [
    #     'groundstate',
    #     'realtime',
    #     'collect'
    # ],
    'dep_file': '.doit.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)


build_dir = Path(conf['build_dir'])
build_dir.mkdir(parents=True, exist_ok=True)

run_dir = Path(conf['run_dir'])

sequence_index = int(get_var('sequence_index', h5tools.autosequence(run_dir)))
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)

dt = conf['dt']
runtime = conf['groundstate']['runtime']
dx = 40 / conf['lattice']

if dt is None:
    dt = 0.1 * dx**2
    conf['dt'] = dt
    print(f"For dx = {dx:.2e} -- calculating dt = {dt:.2e}")


def task_groundstate():
    name = 'groundstate'
    _conf = conf.copy()
    _conf['exec_filename'] = name
    _conf.update(_conf[name])
    return tasks.xmds_run(build_dir, _conf)


def task_collect():
    name = 'groundstate'
    target_file = build_dir / conf[name]['output_filename']

    def _log():
        log_results = read_log(build_dir / f"{name}.log")
        h5tools.save_data(h5filepath, log_results, group='log')

    return {
        'actions': [
            (h5tools.mkpath, [h5filepath, conf]),
            (h5tools.copy_group, [target_file, h5filepath, name]),
            _log
        ],
        'file_dep': [target_file]
    }
