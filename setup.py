from setuptools import setup


def get_requirements():
    return ["seatable_api"]


setup(
    name="bibtex-formatter",
    description="Format",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Nickydusk/BibTeX-Formatter.git",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    include_package_data=True,
    install_requires=get_requirements(),
    packages=["bfm"],
    entry_points={
        "console_scripts": ["bfm=bfm:main"],
    },
)
