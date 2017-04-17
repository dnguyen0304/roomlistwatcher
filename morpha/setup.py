#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'morpha'

    description = ''

    with open('./README.md', 'r') as file:
        long_description = file.read()

    install_requires = ['pandas==0.19.2']

    setuptools.setup(name=package_name,
                     version='0.1.0',
                     description=description,
                     long_description=long_description,
                     url='https://github.com/dnguyen0304/morpha.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 2.7'],
                     packages=setuptools.find_packages(exclude=['*.tests']),
                     install_requires=install_requires,
                     test_suite='nose.collector',
                     tests_require=['mock', 'nose'],
                     include_package_data=True)
