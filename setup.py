#!/usr/bin/env python
from setuptools import setup, find_packages
from hanashiai.core import library_details

setup(
    name=library_details['name'],
    version=library_details['version'],
    description='Reddit API interface for Hanashiai',
    license='MIT',

    install_requires=[
        'praw==5.0.1'
    ],
    packages=find_packages(exclude=['docs', 'tests']),

    author='Trevalyan Stevens',
    author_email='etstevens60@gmail.com',
    url='http://www.kerneweksoftware.com/software.html',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    )
