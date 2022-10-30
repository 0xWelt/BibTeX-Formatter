import os

from setuptools import setup


def get_version() -> str:
    # https://packaging.python.org/guides/single-sourcing-package-version/
    init = open(os.path.join("bfm", "__init__.py"), "r").read().split()
    return init[init.index("__version__") + 2][1:-1]


setup(
    name='bibtex-formatter',
    version=get_version(),
    description="Format",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Nickydusk/BibTeX-Formatter.git",
    setup_requires=['setuptools_scm'],
    use_scm_version=False,
    include_package_data=True,
    packages=['bfm'],
    entry_points={
        'console_scripts': ['bfm=bfm:main'],
    }
)
