#! /usr/bin/python
# -*- coding:utf-8 -*-
# @author: weaponhsu
# @File:   setup
# @Time:   2019/11/27 6:24 PM
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youliPyLib-hsu0203",
    version="0.0.1",
    author="hsu0203",
    author_email="huangxu4328@gmail.com",
    description="py3 common package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weaponhsu/youliPyLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
