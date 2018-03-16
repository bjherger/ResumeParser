# ResumeParser

A utility to make handling many resumes easier by automatically pulling contact information, required skills and custom text fields. These results are then surfaced as a convenient summary CSV.

## Quick Start Guide

This assumes you've installed Anaconda (as discussed in [Python Environment](#python-environment))

```bash
# Create Python virtual enviornment
conda env create -f environment.yml

# Activate Python virtual environment
source activate resume

#Retrieve language model from spacy
python -m spacy download en

# Run code (with default configurations)
cd bin/
python main.py

# Review output
open ../data/output/resume_summary.csv

```

## Getting started

### Repo structure

 - `bin/main.py`: Code entry point
 - `confs/confs.yaml.template`: Configuration file template
 - `data/input/example_resumes`: Example resumes, which are parsed w/ default configurations
 - `data/output/resume_summary.csv`: Results from parsing example resumes

### Python Environment

Python code in this repo utilizes packages that are not part of the common library. To make sure you have all of the appropriate packages, please install [Anaconda, Python 2.7 Version](https://www.continuum.io/downloads), and install the environment described in `environment.yml` (Instructions [here](http://conda.pydata.org/docs/using/envs.html), under *Creating an environment from an environment.yml file*, and *Activating an environment*).

Once Anaconda is installed, you can follow the steps described in the [Quick Start Guide](quick-start-guide)

### Configuration file

This program utilizes a configuration file to set program parameters. You can run this program with the default
parameters view sample output, but you'll probably want to create a config file and modify it to get the most value
from this program.

```bash

# Create configuration file from template
scp confs/confs.yaml.template confs/confs.yaml

# Modify confs to match your needs
open confs/confs.yaml
```

The configuration file has a few parameters you can tweak:
 - `resume_directory`: A directory containing resumes you'd like to parse
 - `summary_output_directory`: Where to place the .csv file, summarizing your resumes
 - `data_schema_dir`: The directory to store table schema. This is mostly for development purposes
 - `skills`: A YAML list of skills. Each element in this list can either be a string (e.g. `skill1` or
 `machine learning`), or a list aliases for the same skill (e.g. `[skill2_alias_A, skill2_alias_B]` or `[ml,
 machine learning, machine-learning]`)
 - `universities`: A YAML list of universities you'd like to search for

## Contact
Feel free to contact me at `13herger <at> gmail <dot> com`
