# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "python-box",
    version = "0.1.0",
    author = "Ross Crawford-d'Heureuse",
    author_email = "ross@lawpal.com",
    description = ("python lib for integrating with Box.com"),
    license = "MIT",
    keywords = "python box oauth2",
    url = "https://github.com/rosscdh/python-box",
    packages=['box'],
    install_requires = [
        'requests',  # must refer to package version explicitly **required**
    ]
)
