# Resume Parser

A utility to make handling many resumes easier by automatically pulling contact information, required skills and
custom text fields. These results are then surfaced as a convenient summary CSV.

## Getting started

### Running Code 

To run code:

 - Confirm that appropriate Python modules are installed (See [Python Environment](#python-environment))
 - Run the following commands:

 ```bash
# Activate python environment
source activate resume

# Run program
cd ResumeParser/bin
python ResumeChecker.py --data_path ../data/input/example_resumes --output_path ../data/output/resumes_output.csv
  ```

### Repo structure

Here are pointers to a important files:

 - Driving code is at `bin/ResumeChecker.py`
 - Changelog is at `docs/changelog.md`
 - Example resumes to test the parser with are at `data/input/example_resumes`
 - Results are output to `data/output` by default

### Python Environment

Python code in this repo utilizes packages that are not part of the common library. To make sure you have all of the 
appropriate packages, please install [Anaconda](https://www.continuum.io/downloads), and install the environment 
described in environment.yml (Instructions [here](http://conda.pydata.org/docs/using/envs.html), under *Use 
environment from file*, and *Change environments (activate/deactivate)*). 
  
To create and activate the Python environment, call:
```bash
# Install anaconda environment
conda env create -f environment.yml 

# Activate environment
source activate resume
```


## Contact
Feel free to contact me at `13herger <at> gmail <dot> com`
