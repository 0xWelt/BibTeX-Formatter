# BibTeX Formatter

![PyPI](https://img.shields.io/pypi/v/bibtex-formatter) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bibtex-formatter) ![APM](https://img.shields.io/apm/l/bibtex-formatter) 

Help generate citations that meet the requirements for conference and journal submissions.

## Quick Installation
Install from [PyPi](https://pypi.org/project/bibtex-formatter/):

```bash
pip install bibtex-formatter
```

Alternatively, you can also install the latest version (not stable) from github:

```bash
pip install git+https://github.com/Nickydusk/BibTeX-Formatter.git@main
```

## Usage

`$ bfm`

Options (Please see `bfm --help` for more details):

- `-i INPUT`,`--input INPUT`: Choose the input .bib file, default to `in.bib`
- `-o OUTPUT`,`--output OUTPUT`: Choose the output .bib file, default to `out.bib`
- `-l LOG`,`--log LOG`: Choose the output log file, default to `logs.txt`

## Welcome to PR

You can make contribution to the project by filling more standard conference citation names in `refactor/brief_to_full`. Please use pull requests to submit your changes.
