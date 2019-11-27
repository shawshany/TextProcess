#!/usr/bin/python3
# -*-coding:utf-8 -*-
#Reference:**********************************************
# @Time     : 2019-09-30 14:24
# @Author   : 病虎
# @E-mail   : victor.xsyang@gmail.com
# @File     : setup.py
# @User     : ora
# @Software: PyCharm
# @Description: 
#Reference:**********************************************
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TextProcess_Ora",
    version="0.0.3",
    author="Ora",
    author_email="victor.xsyang@gmail.com",
    description="compute similar scores of two text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shawshany/TextProcess",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)