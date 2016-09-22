__author__ = 'jgevirtz'

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='transactional',
    version='1.0.0',
    description='An experiment with transactional data structures',
    url='https://github.com/joshgev/transactional',
    author='Joshua Gevirtz',
    author_email='joshgev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='example mysql orm',
    packages=find_packages(),
    install_requires=['nose'])