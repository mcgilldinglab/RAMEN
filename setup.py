#!/usr/bin/env python
from setuptools import setup

setup(  name='RAMEN',
        version='1.0',
        description='Random walk and genetic Algorithm based network inference',
        author='Xiong Yiwei, Wang Jingtao',
        author_email='yiwei.xiong@mail.mcgill.ca',
        url="https://github.com/mcgilldinglab/RAMEN",
        license='MIT',
        packages=['ramen'],
        install_requires=['pyitlib>=0.2.2','networkx>=2.8.6','numpy>=1.22.4','scikit-learn>=0.20,<0.23','matplotlib>=3.4.3', 'pandas>=1.3.3', 'igraph>=0.9.11'],
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        )