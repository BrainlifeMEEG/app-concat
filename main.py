"""
Concatenate multiple MNE raw data files.

This app concatenates multiple MNE-compatible raw data files (.fif format) into
a single unified raw data file using mne.concatenate_raws(). This is useful for
combining data from multiple recording sessions or files into a single dataset
for unified processing.

Input:
    - raw: List of paths to MNE raw data files (.fif format) to concatenate

Output:
    - out_dir/raw.fif: Concatenated MNE raw data file
    - out_report/report.html: QC report with concatenation details and channel information
    - product.json: Metadata with concatenated data information
"""

# Copyright (c) 2026 brainlife.io
#
# This app concatenates multiple MNE raw data files.
#
# Authors:
# - Kamilya Salibayeva (https://github.com/KSalibay)
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
    get_inputs_names,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_raw_info_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_report')

# Load configuration
config = load_config()

# == LOAD DATA ==
raws = config['raw']

# Load all raw files
raw_list = []
for i, raw_path in enumerate(raws):
    raw = mne.io.read_raw_fif(raw_path, preload=True)
    raw_list.append(raw)
    print(f"Loaded raw file {i+1}/{len(raws)}: {os.path.basename(raw_path)}")

# mne.concatenate_raws() requires identical channel order *and* identical
# info['bads'] order across raws, but both can differ per run even when the
# underlying sets are the same (e.g. bad channels are marked per run from
# separate QC files, in whatever order that file happens to list them in).
# Normalize both to a canonical order; fail loudly if the sets themselves
# actually differ, since that would be a genuine data mismatch.
ref_ch_names = raw_list[0].ch_names
ref_bads = set(raw_list[0].info['bads'])
for i, raw in enumerate(raw_list[1:], start=2):
    if set(raw.ch_names) != set(ref_ch_names):
        raise ValueError(
            f"Raw file {i}/{len(raw_list)} has a different channel set than "
            f"file 1: {set(raw.ch_names) ^ set(ref_ch_names)}"
        )
    if set(raw.info['bads']) != ref_bads:
        raise ValueError(
            f"Raw file {i}/{len(raw_list)} has different bad channels than "
            f"file 1: {set(raw.info['bads']) ^ ref_bads}"
        )
for raw in raw_list:
    if raw.ch_names != ref_ch_names:
        raw.reorder_channels(ref_ch_names)
    raw.info['bads'] = sorted(raw.info['bads'])

# == CONCATENATE RAWS ==
raw_final = mne.concatenate_raws(raw_list)

# == CREATE REPORT ==
report = mne.Report(title='Concatenate Raw Files Report')

# Get input names from config metadata
inputs_info = get_inputs_names()

# Create summary table of input files
input_summary_html = '<p><b>Summary of Input Raw Files</b></p>'
input_summary_html += '<table style="border-collapse: collapse; width: 100%;">'
input_summary_html += '<tr style="border-bottom: 2px solid black;"><th style="text-align: left; padding: 8px; border: 1px solid gray;">File #</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Filename</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Duration (s)</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">n_channels</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">sfreq (Hz)</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Tags</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Datatype Tags</th></tr>'

for i, raw in enumerate(raw_list):
    duration = raw.n_times / raw.info['sfreq']
    filename = os.path.basename(raws[i])
    
    # Get input identifiers if available
    tags = ""
    datatype_tags = ""
    if i < len(inputs_info):
        input_info = inputs_info[i]
        tags = ", ".join(input_info.get('tags', []))
        datatype_tags = ", ".join(input_info.get('datatype_tags', []))
    
    input_summary_html += f'<tr style="border-bottom: 1px solid gray;"><td style="padding: 8px; border: 1px solid gray;">{i+1}</td><td style="padding: 8px; border: 1px solid gray;">{filename}</td><td style="padding: 8px; border: 1px solid gray;">{duration:.2f}</td><td style="padding: 8px; border: 1px solid gray;">{raw.info["nchan"]}</td><td style="padding: 8px; border: 1px solid gray;">{raw.info["sfreq"]:.1f}</td><td style="padding: 8px; border: 1px solid gray;">{tags}</td><td style="padding: 8px; border: 1px solid gray;">{datatype_tags}</td></tr>'

input_summary_html += '</table>'
report.add_html(title='Input Files Summary', html=input_summary_html)

report.add_raw(raw=raw_final, title='Concatenated Raw Data')

# Add channel information to report
channel_info_html = '<p><b>Channels in concatenated file:</b></p>' + ', '.join(raw_final.ch_names)
report.add_html(title='Channels', html=channel_info_html)

# == SAVE DATA ==
raw_final.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == CREATE PRODUCT JSON ==
product_items = []

# Add structured raw info messages
add_raw_info_to_product(product_items, raw_final)

# Add concatenation summary
concat_msg = f"Concatenated {len(raws)} raw files into single dataset"
add_info_to_product(product_items, concat_msg)

# Create the product.json file
create_product_json(product_items)

