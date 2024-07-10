import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


requirements = [
    # use environment.yml
]


setup(
    name="local_rag_chunkenizer",
    version="0.0.1",
    url="https://github.com/TIC-13/RAG",
    author="LuxAI",
    author_email="cinsoftextic13@gmail.com",
    description="Chunkenize documents",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    entry_points={
        "console_scripts": [
            "local_rag_chunkenizer=local_rag_chunkenizer.cli:cli"
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
    ],
)
