# app-concat

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.444-blue.svg)](https://doi.org/10.25663/bl.app.444)

## Description

Concatenates multiple MNE raw data files (.fif format) into a single unified raw data file using `mne.concatenate_raws()`. This app is useful for combining data from multiple recording sessions, runs, or files into a single dataset for unified downstream processing.

## Inputs

- **raw**: List of paths to MNE raw data files (.fif format) to concatenate. Files should be in the same format and ideally have compatible channel configurations.

## Outputs

- **out_dir/raw.fif**: Concatenated raw data file in MNE format
- **out_report/report.html**: QC report containing concatenation details, source file information, and channel details
- **product.json**: Metadata with information about the concatenated data

## Configuration Parameters

### Required

- `raw`: A list/array of paths to the input MNE raw data files (.fif format) to be concatenated

Example configuration:
```json
{
    "raw": [
        "path/to/raw1.fif",
        "path/to/raw2.fif",
        "path/to/raw3.fif"
    ]
}
```

## Usage

The app reads multiple raw MNE data files, loads them with preload enabled, concatenates them into a single raw file, and outputs the result.

## Technical Details

- **Execution**: Python with MNE-Python and shared brainlife_utils library
- **Data format**: MNE `.fif` format (compatible with all downstream Brainlife.io apps)
- **Concatenation**: Uses `mne.concatenate_raws()` for proper handling of channel information and metadata
- **Preloading**: All files are preloaded into memory before concatenation
- **Report generation**: Automatic HTML report with concatenation details and channel visualization

## Authors

- [Kamilya Salibayeva](https://github.com/KSalibay) (Indiana University)
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

**brainlife.io: A decentralized and open source cloud platform to support neuroscience research**. Hayashi, S., Caron, B. A., et al. & Pestilli, F. (2023). ArXiv. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10274934/

**MEG and EEG data analysis with MNE-Python**. Gramfort A, et al. & Hämäläinen MS. (2013). Frontiers in Neuroscience, 7(267):1–13. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

#### MIT Copyright (c) 2026 brainlife.io The University of Texas at Austin and Indiana University
```

### Sample Datasets

If you don't have your own input file, you can download sample datasets from Brainlife.io, or you can use [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 && mv 5a0f0fad2c214c9ba8624376#5a050966eec2b300611abff2 .
```

## Output

All output file (a concatenated MNE/FIFF (.fif) file) will be generated inside the current working directory (pwd), inside a specifc directory called:

```
out_dir
```

### Dependencies

This App requires MNE/Python to run.

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
