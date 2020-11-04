#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
import h5py
from pathlib import Path


def autosequence(run_dir, fmt="{:04d}"):
    sequence_index = 0
    run_dir = Path(run_dir)
    while True:
        seq_dir = run_dir / fmt.format(sequence_index)
        if seq_dir.exists():
            sequence_index += 1
        else:
            break
    return sequence_index


def mkpath(h5filepath, conf):
    print(h5filepath)
    h5filepath.parent.mkdir(parents=True, exist_ok=True)
    copy_attrs(h5filepath, conf)


def save_data(filename, data, group):
    with h5py.File(filename, 'a') as h5file:
        g = h5file.require_group(group)
        for key, value in data.items():
            # print(key)
            if isinstance(value, dict):
                _group = f"{group}/{key}"
                save_data(filename, data=value, group=_group)
            elif hasattr(value, '__iter__') and not isinstance(value, str):
                try:
                    g.create_dataset(key, data=value, maxshape=(None,))
                except RuntimeError:
                    del g[key]
                    g.create_dataset(key, data=value, maxshape=(None,))
            else:
                g.attrs[key] = value


def copy_attrs(h5file, data, group='configure'):
    with h5py.File(h5file, 'a') as fd:
        g = fd.require_group(group)
        for key, value in data.items():
            # print(key)
            if isinstance(value, dict):
                _group = f"{group}/{key}"
                copy_attrs(h5file, data=value, group=_group)
            else:
                g.attrs[key] = value


def copy_group(source, dest, group):
    with h5py.File(source, 'r') as fs:
        with h5py.File(dest, 'a') as fd:
            g = fd.require_group(group)
            script = source.parent / f"{group}.xmds"
            with open(script, 'r') as f:
                script = f.read()
            try:
                g['xmds_script'] = script
            except RuntimeError:
                del g['xmds_script']
                g['xmds_script'] = script
            for k in fs.keys():
                try:
                    fs.copy(k, g)
                except RuntimeError:
                    del g[k]
                    fs.copy(k, g)
