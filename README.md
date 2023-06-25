# BibTeX Formatter

![GitHub repo size](https://img.shields.io/github/repo-size/Nickydusk/bibtex-formatter) ![PyPI](https://img.shields.io/pypi/v/bibtex-formatter) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bibtex-formatter) ![GitHub](https://img.shields.io/github/license/Nickydusk/BibTex-Formatter)

Help generate citations that meet the requirements for conference and journal submissions.

## Call for Contributions

Completing standardized names can make matching more precise. We would greatly appreciate it if you can fill more standard conference / journal names or correct wrong names in `bfm/data/others.txt`. Please use pull requests to submit your changes.

## Quick Installation

Install from [PyPi](https://pypi.org/project/bibtex-formatter/):

```bash
pip install -U bibtex-formatter
```

Alternatively, you can also install the latest version (not stable) from github:

```bash
pip install -U git+https://github.com/Nickydusk/BibTeX-Formatter.git@main
```

## Usage

```bash
bfm IN_FILE
```

Positional args:

- `IN_FILE`: Choose the input .bib file

Options (Please see `bfm --help` for more details):

- `-o OUTPUT`,`--output OUTPUT`: Choose the output .bib file, default to `out.bib`
- `-l LOG`,`--log LOG`: Choose the output log file, default to `logs.txt`
<!-- - `-d`, `--use_database`: Do online check with NJU database, default to False (The feature may override correct entries, use with caution!) -->

## Features

- [x] Remove duplicate citations (keep the first occurrence), log what is removed
- [x] Simplify keys according to citation type (e.g., `@inproceedings -> [author, title, booktitle, pages, year]`)
- [x] Standardize conference / journal names (e.g., `Advances in Neural Information Processing Systems`)
- [x] Standardize "pages" to `pages = {start-end}`, alert if more or less timestamps.
- [x] Standardize arXiv citations to **google scholar style**
  - [x] arXiv export bibtex -> google scholar style
  - [x] dblp bibtex -> google scholar style
- [ ] Online check contents, make sure they are up to date
