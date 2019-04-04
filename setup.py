#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('./README.rst') as readme_file:
    readme = readme_file.read()

with open('./HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'paho-mqtt',
    'asyncio',
    'gmqtt',
    'influxdb',
    'cloudant',
    'ibmiotf',
    'pytest',
    'fastecdsa',
    'ecdsa',
    'pycrypto',
    'jaeger-client',
    'pytest-asyncio',
    'falcon',
    # 'iotl',
]

# dependency_links = [
#     'git+ssh://git@gitlab.com/chariot-h2020/iot-modeling-language.git#egg=iotl-0.106'
# ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="George Theofilis",
    author_email='g.theofilis@clmsuk.com',
    classifiers=[
        'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    description="Chariot base micro-service",
    install_requires=requirements,
    # dependency_links=dependency_links,
    license="EPL-1.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chariot_base',
    name='chariot_base',
    packages=find_packages(include=[
        'chariot_base',
        'chariot_base.*'
    ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/chariot-h2020/chariot_base',
    version='0.9.2',
    zip_safe=False,
)
