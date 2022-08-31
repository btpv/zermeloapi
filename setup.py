from os import read
import setuptools
from datetime import datetime
version = str(datetime.today()).split('.')[0].replace(
    '-', '.').replace(':', '.').replace(' ', '.')


def get_date():
    year, week = datetime.today().strftime("%Y %W").split(" ")
    return year, week


with open("src\zermeloapi\__init__.py", "r", encoding="utf-8") as fh:
    initpy = fh.read()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read().replace("this_week", get_date()[1]).replace(
        "this_year", get_date()[0]).replace("__init__.py", initpy).replace('__version__', version)
setuptools.setup(
    name="zermeloapi",
    version=version,
    author="b.vill",
    author_email="villeriusborro@gmail.com",
    description="zermelo api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'datetime',
        'requests'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)
