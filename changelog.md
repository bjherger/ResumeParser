# ResumeParser Change Log

## 3.0.0 - 2017-10-20

Re-write, mostly from scratch

### Added

 - None

### Modified

Structure

 - Program now follows ETL design principles
 - Program is broken into a driver file, library file and field extraction file

Configuration

 - Skills to look for are now listed in the configuration file
 - Universities to look for are now listed in the configuration file

Output
- Program now provides a set containing skills found, rather than a count for each skill

### Removed

 - Address search. Addresses search was limited to addresses in California.
 - README has been reset to a non-project specific readme. It should be specialized for this project in a future
 version.

## 2.1.0 - 2017-10-20

### Added

 - `candidate_name`: Adding candidate name extractor, using spacy
 - `university`: Code will now check for a list of universities

### Changed

 - Skills search: Now users can provide a list of skills, which will be searched for

### Removed


## 2.0.0 - 2016-10-22

### Added

### Changed
 - `README.md` re-written for clarity, better code example
 - Folder structure refactored for clarify
 - `ResumeChecker.py` refactored to match Python style standards, legibility

### Removed
 - `code/` folder removed. It only contained extraneous code, and outdated `requirements.txt`

## 1.0.0 - 2015-02-25
Core functionality to read in PDF resumes, extract text, output results table