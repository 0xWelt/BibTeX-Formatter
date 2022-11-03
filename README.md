# BibTeX Formatter

![GitHub repo size](https://img.shields.io/github/repo-size/Nickydusk/bibtex-formatter) ![PyPI](https://img.shields.io/pypi/v/bibtex-formatter) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bibtex-formatter) ![GitHub](https://img.shields.io/github/license/Nickydusk/BibTex-Formatter)

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

## Features
- [x] Remove duplicate entries, log what is removed
- [x] Simplify keys according to citation type (e.g., `@inproceedings -> [author, title, booktitle, pages, year]`)
- [x] Standardize conference / journal names (e.g., `Advances in Neural Information Processing Systems (NeurIPS)`)

## Welcome to PR

You can make contribution to the project by filling more standard conference / journal names in `refactor/STANDARD_NAMES`. Please use pull requests to submit your changes.
