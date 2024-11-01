#!/usr/bin/env python
from setuptools import setup

setup(  name='RAMEN',
        version='1.0',
        description='Random walk and genetic Algorithm based network inference',
        author='Xiong Yiwei, Wang Jingtao',
        author_email='yiwei.xiong@mail.mcgill.ca',
        url="https://github.com/mcgilldinglab/RAMEN",
        license='MIT',
        packages=['ramen', 'ramen.random_walk', 'ramen.genetic_algorithm'],
        install_requires=['networkx>=2.8.6','numpy>=1.22.4','scikit-network>=0.26.0','matplotlib>=3.4.3', 'pandas>=1.3.3', 'igraph>=0.9.11', 'scipy>=1.7.1'],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        )