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

# Copyright (c) 2020 brainlife.io
#
# This app concatenates multiple MNE raw data files.
#
# Author: Kamilya Salibayeva
# Indiana University

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
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

# == CONCATENATE RAWS ==
raw_final = mne.concatenate_raws(raw_list)

# == CREATE REPORT ==
report = mne.Report(title='Concatenate Raw Files Report')

# Create summary table of input files
input_summary_html = '<p><b>Summary of Input Raw Files</b></p>'
input_summary_html += '<table style="border-collapse: collapse; width: 100%;">'
input_summary_html += '<tr style="border-bottom: 2px solid black;"><th style="text-align: left; padding: 8px; border: 1px solid gray;">File #</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Filename</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">Duration (s)</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">n_channels</th><th style="text-align: left; padding: 8px; border: 1px solid gray;">sfreq (Hz)</th></tr>'

for i, raw in enumerate(raw_list):
    duration = raw.n_times / raw.info['sfreq']
    filename = os.path.basename(raws[i])
    input_summary_html += f'<tr style="border-bottom: 1px solid gray;"><td style="padding: 8px; border: 1px solid gray;">{i+1}</td><td style="padding: 8px; border: 1px solid gray;">{filename}</td><td style="padding: 8px; border: 1px solid gray;">{duration:.2f}</td><td style="padding: 8px; border: 1px solid gray;">{raw.n_channels}</td><td style="padding: 8px; border: 1px solid gray;">{raw.info["sfreq"]:.1f}</td></tr>'

input_summary_html += '</table>'
report.add_html(title='Input Files Summary', html=input_summary_html)

report.add_raw(raw=raw_final, title='Concatenated Raw Data')

# Add information about concatenation
concat_info_html = f'<p><b>Concatenated {len(raws)} raw files</b></p>'
concat_info_html += '<p><b>Source files:</b><br>'
for i, raw_path in enumerate(raws):
    concat_info_html += f'{i+1}. {os.path.basename(raw_path)}<br>'
concat_info_html += '</p>'
report.add_html(title='Concatenation Details', html=concat_info_html)

# Add channel information to report
channel_info_html = '<p><b>Channels in concatenated file:</b></p>' + ', '.join(raw_final.ch_names)
report.add_html(title='Channels', html=channel_info_html)

# == SAVE DATA ==
raw_final.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)
report.save(os.path.join('out_report', 'report.html'), overwrite=True)

# == CREATE PRODUCT JSON ==
product_items = []

# Add structured raw info messages
add_raw_info_to_product(product_items, raw_final)

# Add concatenation summary
concat_msg = f"Concatenated {len(raws)} raw files into single dataset"
add_info_to_product(product_items, concat_msg)

# Create the product.json file
create_product_json(product_items)

