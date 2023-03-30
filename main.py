# Copyright (c) 2020 brainlife.io
#
# This file is the main script for applying baseline correction to MEG/EEG Epochs files.
#
# Author: Kamilya Salibayeva
# Indiana University

# set up environment
import os
import json
import mne

# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Populate mne_config.py file with brainlife config.json
with open(__location__+'/config.json') as config_json:
    config = json.load(config_json)


fname1 = config['raw1']
fname2 = config['raw2']
fname3 = config['raw3']
fname4 = config['raw4']
fname5 = config['raw5']

raw1 = mne.io.read_raw_fif(fname1)
raw2 = mne.io.read_raw_fif(fname2)
raw3 = mne.io.read_raw_fif(fname3)
raw4 = mne.io.read_raw_fif(fname4)
raw5 = mne.io.read_raw_fif(fname5)

list = [x for x in [raw1,raw2,raw3,raw4,raw5] if len(x) != 0]

raw_final = mne.concatenate_raws([list])

# save mne/raw
raw_final.save(os.path.join('out_dir','concat-raw.fif'))

