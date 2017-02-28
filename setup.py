# coding: utf-8
# Author: Allen Zou
# 2017/2/28 上午9:42
from setuptools import setup, find_packages

setup(name="etcd_yaml",
      version="1.0.0",
      py_modules=["etcd_yaml"],
      packages=find_packages(),
      install_requires=["pyyaml>=3.11"])
