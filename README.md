# Resume Parser

A utility to make handling many resumes easier by automatically pulling contact information, required skills and 
custom text fields, and surfacing these results in a tabular format. 

## Getting started

### Running Code 

To run code:
 - Confirm that appropriate Python modules are installed (See [Python Environment](#python-environment))
 - Rune the following commands:
 ```bash
cd bin
python ResumeChecker.py --data_path ../data/input/example_resumes --output_path ../data/output/resumes_output.csv
  ```

### Repo structure
 - Driving code is at `bin/ResumeChecker.py`
 - Changelog is at `docs/changelog.md`
 - Example resumes to test the parser with are at `data/input/example_resumes`
 - Results are output to `data/output` by default

### Python Environment
Python code in this repo utilizes packages that are not part of the common library. To make sure you have all of the 
appropriate packages, please install [Anaconda](https://www.continuum.io/downloads), and install the environment 
described in environment.yml (Instructions [here](http://conda.pydata.org/docs/using/envs.html), under *Use 
environment from file*, and *Change environments (activate/deactivate)*). 

### To run code
  
To run the Python code, complete the following:
```bash
# Install anaconda environment
conda env create -f environment.yml 
# Make a note of the environent name (e.g. source activate environment_name)

# Activate environment
source activate environment_name

# Run script
cd bin/
python file_name.py
```


## Contact
Feel free to contact me at 13herger <at> gmail <dot> com
